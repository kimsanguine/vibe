/**
 * Hook 시스템 타입 정의
 */

// YouTube 비디오 정보
export interface VideoInfo {
  videoId: string;
  title: string;
  author: string;
  lengthSeconds: number;
  viewCount: number;
  thumbnailUrl?: string;
  description?: string;
}

// 다운로드 진행 정보
export interface DownloadProgress {
  videoId: string;
  downloaded: number;
  total: number;
  percent: number;
  speed?: number; // bytes per second
  eta?: number; // seconds
}

// 저장 정보
export interface SaveInfo {
  videoId: string;
  filePath: string;
  fileSize: number;
  format: string;
  quality: string;
}

// 에러 정보
export interface ErrorInfo {
  videoId?: string;
  error: Error;
  context: string;
  timestamp: Date;
}

// Hook 이벤트 타입
export type HookEventType =
  | 'beforeDownload'
  | 'afterDownload'
  | 'progress'
  | 'beforeSave'
  | 'afterSave'
  | 'error'
  | 'cancel';

// Hook 콜백 타입들
export type BeforeDownloadHook = (videoInfo: VideoInfo) => Promise<boolean | void>;
export type AfterDownloadHook = (videoInfo: VideoInfo, data: Buffer) => Promise<void>;
export type ProgressHook = (progress: DownloadProgress) => void;
export type BeforeSaveHook = (saveInfo: SaveInfo) => Promise<boolean | void>;
export type AfterSaveHook = (saveInfo: SaveInfo) => Promise<void>;
export type ErrorHook = (errorInfo: ErrorInfo) => Promise<void>;
export type CancelHook = (videoId: string, reason: string) => Promise<void>;

// Hook 콜백 유니온 타입
export type HookCallback =
  | BeforeDownloadHook
  | AfterDownloadHook
  | ProgressHook
  | BeforeSaveHook
  | AfterSaveHook
  | ErrorHook
  | CancelHook;

// Hook 등록 정보
export interface HookRegistration {
  id: string;
  event: HookEventType;
  callback: HookCallback;
  priority: number;
  once: boolean;
}

// Hook 설정
export interface HookConfig {
  enabled: boolean;
  timeout: number; // ms
  maxRetries: number;
  continueOnError: boolean;
}
