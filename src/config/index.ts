/**
 * 설정 관리
 */

import * as fs from 'fs-extra';
import * as path from 'path';
import { AutosaveConfig } from '../youtube/types';
import { HookConfig } from '../hooks/types';

export interface VibeConfig {
  autosave: Partial<AutosaveConfig>;
  hooks: Partial<HookConfig>;
}

const DEFAULT_CONFIG: VibeConfig = {
  autosave: {
    outputDir: './downloads',
    filenameTemplate: '{title}_{videoId}',
    quality: 'highest',
    format: 'mp4',
    maxConcurrent: 3,
    retryCount: 3,
    skipExisting: true,
    saveMetadata: true,
  },
  hooks: {
    enabled: true,
    timeout: 30000,
    continueOnError: true,
  },
};

const CONFIG_FILENAME = 'vibe.config.json';

/**
 * 설정 파일 로드
 */
export async function loadConfig(configPath?: string): Promise<VibeConfig> {
  const filePath = configPath || path.join(process.cwd(), CONFIG_FILENAME);

  try {
    if (await fs.pathExists(filePath)) {
      const userConfig = await fs.readJson(filePath);
      return mergeConfig(DEFAULT_CONFIG, userConfig);
    }
  } catch (error) {
    console.warn(`Failed to load config from ${filePath}:`, error);
  }

  return DEFAULT_CONFIG;
}

/**
 * 설정 파일 저장
 */
export async function saveConfig(config: VibeConfig, configPath?: string): Promise<void> {
  const filePath = configPath || path.join(process.cwd(), CONFIG_FILENAME);
  await fs.writeJson(filePath, config, { spaces: 2 });
}

/**
 * 기본 설정 파일 생성
 */
export async function initConfig(configPath?: string): Promise<void> {
  const filePath = configPath || path.join(process.cwd(), CONFIG_FILENAME);

  if (await fs.pathExists(filePath)) {
    throw new Error(`Config file already exists: ${filePath}`);
  }

  await saveConfig(DEFAULT_CONFIG, filePath);
}

/**
 * 설정 병합
 */
function mergeConfig(base: VibeConfig, override: Partial<VibeConfig>): VibeConfig {
  return {
    autosave: { ...base.autosave, ...override.autosave },
    hooks: { ...base.hooks, ...override.hooks },
  };
}

export { DEFAULT_CONFIG };
