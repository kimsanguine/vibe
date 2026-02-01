/**
 * 커스텀 Hook 예제
 *
 * 다양한 Hook 활용 방법을 보여줍니다.
 */

import { HookManager, VideoInfo, DownloadProgress, SaveInfo, ErrorInfo } from '../src';
import * as fs from 'fs-extra';
import * as path from 'path';

// 다운로드 통계 추적
interface DownloadStats {
  totalDownloads: number;
  successCount: number;
  failCount: number;
  totalBytes: number;
  videos: string[];
}

const stats: DownloadStats = {
  totalDownloads: 0,
  successCount: 0,
  failCount: 0,
  totalBytes: 0,
  videos: [],
};

export function setupCustomHooks(hookManager: HookManager): void {
  // 1. 로깅 Hook - 모든 다운로드 기록
  hookManager.register(
    'beforeDownload',
    async (videoInfo: VideoInfo) => {
      const logEntry = {
        timestamp: new Date().toISOString(),
        videoId: videoInfo.videoId,
        title: videoInfo.title,
        author: videoInfo.author,
      };

      await fs.appendFile(
        'download-log.jsonl',
        JSON.stringify(logEntry) + '\n'
      );

      stats.totalDownloads++;
      return true;
    },
    { priority: 1 } // 가장 먼저 실행
  );

  // 2. 필터링 Hook - 특정 조건 영상만 허용
  hookManager.register(
    'beforeDownload',
    async (videoInfo: VideoInfo) => {
      // 예: 조회수 1000 미만 영상 스킵
      if (videoInfo.viewCount < 1000) {
        console.log(`[필터] 조회수 부족으로 스킵: ${videoInfo.title}`);
        return false;
      }

      // 예: 특정 키워드 포함 영상만 허용
      const allowedKeywords = ['tutorial', '강좌', 'how to'];
      const titleLower = videoInfo.title.toLowerCase();
      const hasKeyword = allowedKeywords.some(kw =>
        titleLower.includes(kw.toLowerCase())
      );

      if (!hasKeyword) {
        console.log(`[필터] 키워드 미포함으로 스킵: ${videoInfo.title}`);
        return false;
      }

      return true;
    },
    { priority: 5 }
  );

  // 3. 진행률 표시 Hook - 프로그레스 바
  let lastLine = '';
  hookManager.register('progress', (progress: DownloadProgress) => {
    const width = 30;
    const filled = Math.round((progress.percent / 100) * width);
    const empty = width - filled;
    const bar = '█'.repeat(filled) + '░'.repeat(empty);
    const line = `[${bar}] ${progress.percent.toFixed(1)}%`;

    if (line !== lastLine) {
      process.stdout.write(`\r${line}`);
      lastLine = line;
    }
  });

  // 4. 후처리 Hook - 다운로드 후 파일 정리
  hookManager.register(
    'afterSave',
    async (saveInfo: SaveInfo) => {
      stats.successCount++;
      stats.totalBytes += saveInfo.fileSize;
      stats.videos.push(saveInfo.videoId);

      // 디렉토리별 정리
      const dateDir = new Date().toISOString().split('T')[0];
      const targetDir = path.join(path.dirname(saveInfo.filePath), dateDir);
      await fs.ensureDir(targetDir);

      const newPath = path.join(targetDir, path.basename(saveInfo.filePath));
      await fs.move(saveInfo.filePath, newPath, { overwrite: true });

      console.log(`\n[정리] 파일 이동: ${newPath}`);
    },
    { priority: 10 }
  );

  // 5. 에러 처리 Hook - 에러 로깅 및 알림
  hookManager.register('error', async (errorInfo: ErrorInfo) => {
    stats.failCount++;

    const errorLog = {
      timestamp: errorInfo.timestamp.toISOString(),
      videoId: errorInfo.videoId,
      error: errorInfo.error.message,
      context: errorInfo.context,
      stack: errorInfo.error.stack,
    };

    await fs.appendFile('error-log.jsonl', JSON.stringify(errorLog) + '\n');

    // 여기에 알림 로직 추가 가능 (Slack, Discord, Email 등)
    console.error(`[에러] ${errorInfo.videoId}: ${errorInfo.error.message}`);
  });

  // 6. 취소 Hook - 취소 사유 기록
  hookManager.register('cancel', async (videoId: string, reason: string) => {
    console.log(`[취소] ${videoId}: ${reason}`);
  });

  // 7. 일회성 Hook - 첫 번째 다운로드에만 실행
  hookManager.register(
    'afterSave',
    async () => {
      console.log('\n🎉 첫 번째 다운로드 완료! (이 메시지는 한 번만 표시됩니다)');
    },
    { once: true, priority: 0 }
  );
}

// 통계 조회 함수
export function getStats(): DownloadStats {
  return { ...stats };
}

// 통계 리셋 함수
export function resetStats(): void {
  stats.totalDownloads = 0;
  stats.successCount = 0;
  stats.failCount = 0;
  stats.totalBytes = 0;
  stats.videos = [];
}
