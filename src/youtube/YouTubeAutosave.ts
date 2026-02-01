/**
 * YouTube 자동저장 클래스
 */

import * as fs from 'fs-extra';
import * as path from 'path';
import ytdl from 'ytdl-core';
import { EventEmitter } from 'events';

import { HookManager, VideoInfo, DownloadProgress, SaveInfo, ErrorInfo } from '../hooks';
import {
  AutosaveConfig,
  DownloadJob,
  DownloadStatus,
  VideoQuality,
} from './types';

const DEFAULT_CONFIG: AutosaveConfig = {
  outputDir: './downloads',
  filenameTemplate: '{title}_{videoId}',
  quality: 'highest',
  format: 'mp4',
  maxConcurrent: 3,
  retryCount: 3,
  retryDelay: 1000,
  skipExisting: true,
  saveMetadata: true,
  saveThumbnail: false,
  progressInterval: 500,
};

export class YouTubeAutosave extends EventEmitter {
  private config: AutosaveConfig;
  private hookManager: HookManager;
  private activeJobs: Map<string, DownloadJob> = new Map();
  private queue: DownloadJob[] = [];
  private isProcessing: boolean = false;

  constructor(config?: Partial<AutosaveConfig>, hookManager?: HookManager) {
    super();
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.hookManager = hookManager || new HookManager();
  }

  /**
   * Hook Manager 가져오기
   */
  getHookManager(): HookManager {
    return this.hookManager;
  }

  /**
   * 설정 업데이트
   */
  updateConfig(config: Partial<AutosaveConfig>): void {
    this.config = { ...this.config, ...config };
  }

  /**
   * 현재 설정 조회
   */
  getConfig(): AutosaveConfig {
    return { ...this.config };
  }

  /**
   * YouTube URL에서 비디오 ID 추출
   */
  extractVideoId(url: string): string | null {
    const patterns = [
      /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)/,
      /^([a-zA-Z0-9_-]{11})$/,
    ];

    for (const pattern of patterns) {
      const match = url.match(pattern);
      if (match) {
        return match[1];
      }
    }
    return null;
  }

  /**
   * 비디오 정보 가져오기
   */
  async getVideoInfo(urlOrId: string): Promise<VideoInfo> {
    const videoId = this.extractVideoId(urlOrId) || urlOrId;
    const url = `https://www.youtube.com/watch?v=${videoId}`;

    const info = await ytdl.getInfo(url);

    return {
      videoId: info.videoDetails.videoId,
      title: info.videoDetails.title,
      author: info.videoDetails.author.name,
      lengthSeconds: parseInt(info.videoDetails.lengthSeconds),
      viewCount: parseInt(info.videoDetails.viewCount),
      thumbnailUrl: info.videoDetails.thumbnails[0]?.url,
      description: info.videoDetails.description || undefined,
    };
  }

  /**
   * 단일 비디오 다운로드
   */
  async download(urlOrId: string): Promise<DownloadJob> {
    const videoId = this.extractVideoId(urlOrId);
    if (!videoId) {
      throw new Error(`Invalid YouTube URL or ID: ${urlOrId}`);
    }

    const jobId = `job_${Date.now()}_${videoId}`;
    const job: DownloadJob = {
      id: jobId,
      videoId,
      url: `https://www.youtube.com/watch?v=${videoId}`,
      status: 'pending',
      progress: 0,
    };

    this.queue.push(job);
    this.emit('queued', job);

    this.processQueue();

    return job;
  }

  /**
   * 여러 비디오 일괄 다운로드
   */
  async downloadBatch(urls: string[]): Promise<DownloadJob[]> {
    const jobs = await Promise.all(urls.map(url => this.download(url)));
    return jobs;
  }

  /**
   * 다운로드 취소
   */
  async cancel(jobId: string): Promise<boolean> {
    const job = this.activeJobs.get(jobId);
    if (job) {
      job.status = 'cancelled';
      await this.hookManager.executeCancel(job.videoId, 'User cancelled');
      this.activeJobs.delete(jobId);
      this.emit('cancelled', job);
      return true;
    }

    const queueIndex = this.queue.findIndex(j => j.id === jobId);
    if (queueIndex !== -1) {
      const [removed] = this.queue.splice(queueIndex, 1);
      removed.status = 'cancelled';
      await this.hookManager.executeCancel(removed.videoId, 'User cancelled');
      this.emit('cancelled', removed);
      return true;
    }

    return false;
  }

  /**
   * 모든 다운로드 취소
   */
  async cancelAll(): Promise<void> {
    for (const job of this.activeJobs.values()) {
      await this.cancel(job.id);
    }
    for (const job of this.queue) {
      await this.cancel(job.id);
    }
  }

  /**
   * 작업 상태 조회
   */
  getJob(jobId: string): DownloadJob | undefined {
    return this.activeJobs.get(jobId) || this.queue.find(j => j.id === jobId);
  }

  /**
   * 모든 작업 조회
   */
  getAllJobs(): DownloadJob[] {
    return [...this.activeJobs.values(), ...this.queue];
  }

  /**
   * 큐 처리
   */
  private async processQueue(): Promise<void> {
    if (this.isProcessing) return;
    this.isProcessing = true;

    while (this.queue.length > 0 && this.activeJobs.size < this.config.maxConcurrent) {
      const job = this.queue.shift();
      if (job) {
        this.activeJobs.set(job.id, job);
        this.processJob(job).catch(error => {
          console.error(`Job ${job.id} failed:`, error);
        });
      }
    }

    this.isProcessing = false;
  }

  /**
   * 단일 작업 처리
   */
  private async processJob(job: DownloadJob): Promise<void> {
    let retries = 0;

    while (retries <= this.config.retryCount) {
      try {
        await this.executeDownload(job);
        return;
      } catch (error) {
        retries++;
        if (retries > this.config.retryCount) {
          job.status = 'failed';
          job.error = error as Error;

          const errorInfo: ErrorInfo = {
            videoId: job.videoId,
            error: error as Error,
            context: 'Download failed after retries',
            timestamp: new Date(),
          };
          await this.hookManager.executeError(errorInfo);
          this.emit('failed', job, error);
        } else {
          await this.delay(this.config.retryDelay * retries);
        }
      }
    }

    this.activeJobs.delete(job.id);
    this.processQueue();
  }

  /**
   * 실제 다운로드 실행
   */
  private async executeDownload(job: DownloadJob): Promise<void> {
    // 비디오 정보 가져오기
    const videoInfo = await this.getVideoInfo(job.videoId);

    // beforeDownload hook 실행
    const shouldProceed = await this.hookManager.executeBeforeDownload(videoInfo);
    if (!shouldProceed) {
      job.status = 'cancelled';
      await this.hookManager.executeCancel(job.videoId, 'Cancelled by beforeDownload hook');
      this.emit('cancelled', job);
      return;
    }

    // 출력 경로 생성
    await fs.ensureDir(this.config.outputDir);
    const filename = this.generateFilename(videoInfo);
    const filePath = path.join(this.config.outputDir, filename);

    // 중복 체크
    if (this.config.skipExisting && await fs.pathExists(filePath)) {
      job.status = 'completed';
      job.filePath = filePath;
      job.progress = 100;
      this.emit('skipped', job, 'File already exists');
      return;
    }

    // 다운로드 시작
    job.status = 'downloading';
    job.startedAt = new Date();
    this.emit('started', job);

    const chunks: Buffer[] = [];
    let downloadedBytes = 0;
    let totalBytes = 0;
    let lastProgressUpdate = 0;

    const stream = ytdl(job.url, {
      quality: this.mapQuality(this.config.quality),
    });

    await new Promise<void>((resolve, reject) => {
      stream.on('response', (response) => {
        totalBytes = parseInt(response.headers['content-length'] || '0');
      });

      stream.on('data', (chunk: Buffer) => {
        chunks.push(chunk);
        downloadedBytes += chunk.length;

        const now = Date.now();
        if (now - lastProgressUpdate >= this.config.progressInterval) {
          const progress: DownloadProgress = {
            videoId: job.videoId,
            downloaded: downloadedBytes,
            total: totalBytes,
            percent: totalBytes > 0 ? (downloadedBytes / totalBytes) * 100 : 0,
          };
          job.progress = progress.percent;
          this.hookManager.executeProgress(progress);
          this.emit('progress', job, progress);
          lastProgressUpdate = now;
        }
      });

      stream.on('end', () => resolve());
      stream.on('error', (error) => reject(error));
    });

    const data = Buffer.concat(chunks);

    // afterDownload hook 실행
    await this.hookManager.executeAfterDownload(videoInfo, data);

    // 저장 정보
    const saveInfo: SaveInfo = {
      videoId: job.videoId,
      filePath,
      fileSize: data.length,
      format: this.config.format,
      quality: this.config.quality,
    };

    // beforeSave hook 실행
    job.status = 'saving';
    const shouldSave = await this.hookManager.executeBeforeSave(saveInfo);
    if (!shouldSave) {
      job.status = 'cancelled';
      await this.hookManager.executeCancel(job.videoId, 'Cancelled by beforeSave hook');
      this.emit('cancelled', job);
      return;
    }

    // 파일 저장
    await fs.writeFile(filePath, data);

    // 메타데이터 저장
    if (this.config.saveMetadata) {
      const metadataPath = filePath.replace(/\.[^.]+$/, '.json');
      await fs.writeJson(metadataPath, {
        videoInfo,
        downloadedAt: new Date().toISOString(),
        config: this.config,
      }, { spaces: 2 });
    }

    // afterSave hook 실행
    await this.hookManager.executeAfterSave(saveInfo);

    // 완료
    job.status = 'completed';
    job.progress = 100;
    job.filePath = filePath;
    job.completedAt = new Date();

    this.emit('completed', job);
    this.activeJobs.delete(job.id);
    this.processQueue();
  }

  /**
   * 파일명 생성
   */
  private generateFilename(videoInfo: VideoInfo): string {
    const sanitize = (str: string) => str.replace(/[<>:"/\\|?*]/g, '_').substring(0, 100);

    let filename = this.config.filenameTemplate
      .replace('{title}', sanitize(videoInfo.title))
      .replace('{videoId}', videoInfo.videoId)
      .replace('{author}', sanitize(videoInfo.author))
      .replace('{date}', new Date().toISOString().split('T')[0]);

    const extension = this.config.format === 'audio' ? 'mp3' : this.config.format;
    return `${filename}.${extension}`;
  }

  /**
   * 품질 매핑
   */
  private mapQuality(quality: VideoQuality): string {
    const qualityMap: Record<VideoQuality, string> = {
      'highest': 'highestvideo',
      'lowest': 'lowestvideo',
      '1080p': '137',
      '720p': '136',
      '480p': '135',
      '360p': '134',
      '144p': '160',
    };
    return qualityMap[quality] || 'highestvideo';
  }

  /**
   * 지연
   */
  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
