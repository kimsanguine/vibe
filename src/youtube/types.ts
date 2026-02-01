/**
 * YouTube 자동저장 타입 정의
 */

// 비디오 품질 옵션
export type VideoQuality = 'highest' | 'lowest' | '1080p' | '720p' | '480p' | '360p' | '144p';

// 오디오 품질 옵션
export type AudioQuality = 'highestaudio' | 'lowestaudio';

// 다운로드 포맷
export type DownloadFormat = 'mp4' | 'webm' | 'mp3' | 'audio';

// 자동저장 설정
export interface AutosaveConfig {
  // 저장 경로
  outputDir: string;

  // 파일명 템플릿 (예: "{title}_{videoId}")
  filenameTemplate: string;

  // 비디오 품질
  quality: VideoQuality;

  // 포맷
  format: DownloadFormat;

  // 동시 다운로드 수
  maxConcurrent: number;

  // 자동 재시도 횟수
  retryCount: number;

  // 재시도 대기 시간 (ms)
  retryDelay: number;

  // 중복 다운로드 스킵
  skipExisting: boolean;

  // 메타데이터 저장
  saveMetadata: boolean;

  // 썸네일 저장
  saveThumbnail: boolean;

  // 진행률 업데이트 간격 (ms)
  progressInterval: number;
}

// 다운로드 상태
export type DownloadStatus =
  | 'pending'
  | 'downloading'
  | 'processing'
  | 'saving'
  | 'completed'
  | 'failed'
  | 'cancelled';

// 다운로드 작업
export interface DownloadJob {
  id: string;
  videoId: string;
  url: string;
  status: DownloadStatus;
  progress: number;
  error?: Error;
  startedAt?: Date;
  completedAt?: Date;
  filePath?: string;
}

// 감시 대상 타입
export type WatchTarget =
  | { type: 'channel'; channelId: string }
  | { type: 'playlist'; playlistId: string }
  | { type: 'search'; query: string };

// 감시 설정
export interface WatchConfig {
  target: WatchTarget;
  checkInterval: number; // ms
  maxVideos: number;
  filterByDate?: Date;
}
