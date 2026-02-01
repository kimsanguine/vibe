/**
 * Hook 관리자 - Hook 등록, 해제, 실행을 관리
 */

import {
  HookEventType,
  HookCallback,
  HookRegistration,
  HookConfig,
  VideoInfo,
  DownloadProgress,
  SaveInfo,
  ErrorInfo,
} from './types';

export class HookManager {
  private hooks: Map<HookEventType, HookRegistration[]> = new Map();
  private config: HookConfig;
  private idCounter: number = 0;

  constructor(config?: Partial<HookConfig>) {
    this.config = {
      enabled: true,
      timeout: 30000,
      maxRetries: 3,
      continueOnError: true,
      ...config,
    };

    // 모든 이벤트 타입에 대해 빈 배열 초기화
    const eventTypes: HookEventType[] = [
      'beforeDownload',
      'afterDownload',
      'progress',
      'beforeSave',
      'afterSave',
      'error',
      'cancel',
    ];
    eventTypes.forEach(event => this.hooks.set(event, []));
  }

  /**
   * Hook 등록
   */
  register(
    event: HookEventType,
    callback: HookCallback,
    options?: { priority?: number; once?: boolean }
  ): string {
    const id = `hook_${++this.idCounter}`;
    const registration: HookRegistration = {
      id,
      event,
      callback,
      priority: options?.priority ?? 10,
      once: options?.once ?? false,
    };

    const hooks = this.hooks.get(event) || [];
    hooks.push(registration);
    // 우선순위 순으로 정렬 (낮은 숫자가 먼저 실행)
    hooks.sort((a, b) => a.priority - b.priority);
    this.hooks.set(event, hooks);

    return id;
  }

  /**
   * Hook 해제
   */
  unregister(hookId: string): boolean {
    for (const [event, hooks] of this.hooks.entries()) {
      const index = hooks.findIndex(h => h.id === hookId);
      if (index !== -1) {
        hooks.splice(index, 1);
        this.hooks.set(event, hooks);
        return true;
      }
    }
    return false;
  }

  /**
   * 이벤트의 모든 Hook 해제
   */
  unregisterAll(event?: HookEventType): void {
    if (event) {
      this.hooks.set(event, []);
    } else {
      for (const key of this.hooks.keys()) {
        this.hooks.set(key, []);
      }
    }
  }

  /**
   * beforeDownload Hook 실행
   * @returns false면 다운로드 취소
   */
  async executeBeforeDownload(videoInfo: VideoInfo): Promise<boolean> {
    if (!this.config.enabled) return true;

    const hooks = this.hooks.get('beforeDownload') || [];
    for (const hook of hooks) {
      try {
        const result = await this.executeWithTimeout(
          (hook.callback as (info: VideoInfo) => Promise<boolean | void>)(videoInfo)
        );
        if (result === false) {
          return false;
        }
        this.removeIfOnce(hook);
      } catch (error) {
        await this.handleHookError(error as Error, 'beforeDownload', videoInfo.videoId);
        if (!this.config.continueOnError) {
          return false;
        }
      }
    }
    return true;
  }

  /**
   * afterDownload Hook 실행
   */
  async executeAfterDownload(videoInfo: VideoInfo, data: Buffer): Promise<void> {
    if (!this.config.enabled) return;

    const hooks = this.hooks.get('afterDownload') || [];
    for (const hook of hooks) {
      try {
        await this.executeWithTimeout(
          (hook.callback as (info: VideoInfo, data: Buffer) => Promise<void>)(videoInfo, data)
        );
        this.removeIfOnce(hook);
      } catch (error) {
        await this.handleHookError(error as Error, 'afterDownload', videoInfo.videoId);
        if (!this.config.continueOnError) throw error;
      }
    }
  }

  /**
   * progress Hook 실행 (동기)
   */
  executeProgress(progress: DownloadProgress): void {
    if (!this.config.enabled) return;

    const hooks = this.hooks.get('progress') || [];
    for (const hook of hooks) {
      try {
        (hook.callback as (p: DownloadProgress) => void)(progress);
        this.removeIfOnce(hook);
      } catch (error) {
        console.error('Progress hook error:', error);
      }
    }
  }

  /**
   * beforeSave Hook 실행
   * @returns false면 저장 취소
   */
  async executeBeforeSave(saveInfo: SaveInfo): Promise<boolean> {
    if (!this.config.enabled) return true;

    const hooks = this.hooks.get('beforeSave') || [];
    for (const hook of hooks) {
      try {
        const result = await this.executeWithTimeout(
          (hook.callback as (info: SaveInfo) => Promise<boolean | void>)(saveInfo)
        );
        if (result === false) {
          return false;
        }
        this.removeIfOnce(hook);
      } catch (error) {
        await this.handleHookError(error as Error, 'beforeSave', saveInfo.videoId);
        if (!this.config.continueOnError) {
          return false;
        }
      }
    }
    return true;
  }

  /**
   * afterSave Hook 실행
   */
  async executeAfterSave(saveInfo: SaveInfo): Promise<void> {
    if (!this.config.enabled) return;

    const hooks = this.hooks.get('afterSave') || [];
    for (const hook of hooks) {
      try {
        await this.executeWithTimeout(
          (hook.callback as (info: SaveInfo) => Promise<void>)(saveInfo)
        );
        this.removeIfOnce(hook);
      } catch (error) {
        await this.handleHookError(error as Error, 'afterSave', saveInfo.videoId);
        if (!this.config.continueOnError) throw error;
      }
    }
  }

  /**
   * error Hook 실행
   */
  async executeError(errorInfo: ErrorInfo): Promise<void> {
    const hooks = this.hooks.get('error') || [];
    for (const hook of hooks) {
      try {
        await (hook.callback as (info: ErrorInfo) => Promise<void>)(errorInfo);
        this.removeIfOnce(hook);
      } catch (error) {
        console.error('Error hook failed:', error);
      }
    }
  }

  /**
   * cancel Hook 실행
   */
  async executeCancel(videoId: string, reason: string): Promise<void> {
    if (!this.config.enabled) return;

    const hooks = this.hooks.get('cancel') || [];
    for (const hook of hooks) {
      try {
        await (hook.callback as (id: string, r: string) => Promise<void>)(videoId, reason);
        this.removeIfOnce(hook);
      } catch (error) {
        console.error('Cancel hook error:', error);
      }
    }
  }

  /**
   * 등록된 Hook 목록 조회
   */
  getHooks(event?: HookEventType): HookRegistration[] {
    if (event) {
      return [...(this.hooks.get(event) || [])];
    }
    const allHooks: HookRegistration[] = [];
    for (const hooks of this.hooks.values()) {
      allHooks.push(...hooks);
    }
    return allHooks;
  }

  /**
   * 설정 업데이트
   */
  updateConfig(config: Partial<HookConfig>): void {
    this.config = { ...this.config, ...config };
  }

  /**
   * 현재 설정 조회
   */
  getConfig(): HookConfig {
    return { ...this.config };
  }

  // Private 메서드들

  private async executeWithTimeout<T>(promise: Promise<T>): Promise<T> {
    return Promise.race([
      promise,
      new Promise<T>((_, reject) =>
        setTimeout(() => reject(new Error('Hook timeout')), this.config.timeout)
      ),
    ]);
  }

  private removeIfOnce(hook: HookRegistration): void {
    if (hook.once) {
      this.unregister(hook.id);
    }
  }

  private async handleHookError(
    error: Error,
    context: string,
    videoId?: string
  ): Promise<void> {
    const errorInfo: ErrorInfo = {
      videoId,
      error,
      context: `Hook execution failed in ${context}`,
      timestamp: new Date(),
    };
    await this.executeError(errorInfo);
  }
}

// 기본 인스턴스 export
export const defaultHookManager = new HookManager();
