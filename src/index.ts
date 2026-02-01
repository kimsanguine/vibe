/**
 * Vibe - YouTube 자동저장 with Hooks
 *
 * 메인 진입점
 */

// Hooks 모듈
export {
  HookManager,
  defaultHookManager,
  HookEventType,
  HookCallback,
  HookRegistration,
  HookConfig,
  VideoInfo,
  DownloadProgress,
  SaveInfo,
  ErrorInfo,
  BeforeDownloadHook,
  AfterDownloadHook,
  ProgressHook,
  BeforeSaveHook,
  AfterSaveHook,
  ErrorHook,
  CancelHook,
} from './hooks';

// YouTube 모듈
export {
  YouTubeAutosave,
  AutosaveConfig,
  DownloadJob,
  DownloadStatus,
  VideoQuality,
  AudioQuality,
  DownloadFormat,
  WatchTarget,
  WatchConfig,
} from './youtube';

// Config 모듈
export {
  VibeConfig,
  loadConfig,
  saveConfig,
  initConfig,
  DEFAULT_CONFIG,
} from './config';

// 편의를 위한 기본 인스턴스 생성 함수
import { YouTubeAutosave } from './youtube';
import { loadConfig } from './config';

/**
 * 설정 파일을 로드하여 YouTubeAutosave 인스턴스 생성
 */
export async function createAutosave(configPath?: string): Promise<YouTubeAutosave> {
  const config = await loadConfig(configPath);
  return new YouTubeAutosave(config.autosave);
}
