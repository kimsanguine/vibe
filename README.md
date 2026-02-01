# Vibe

YouTube 자동저장 with Hooks 시스템

## Features

- YouTube 비디오 자동 다운로드
- 유연한 Hook 시스템 (다운로드 전/후, 저장 전/후, 진행률, 에러 처리)
- 일괄 다운로드 지원
- 재시도 로직
- 메타데이터 저장
- 설정 파일 지원

## Installation

```bash
npm install
```

### OpenClaw

To install OpenClaw, run the following command:

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

## Quick Start

```typescript
import { YouTubeAutosave, HookManager } from 'vibe';

// Hook Manager 생성
const hookManager = new HookManager();

// 다운로드 전 Hook 등록
hookManager.register('beforeDownload', async (videoInfo) => {
  console.log(`다운로드 시작: ${videoInfo.title}`);
  return true; // false 반환 시 다운로드 취소
});

// 진행률 Hook 등록
hookManager.register('progress', (progress) => {
  console.log(`진행률: ${progress.percent.toFixed(1)}%`);
});

// YouTubeAutosave 인스턴스 생성
const autosave = new YouTubeAutosave(
  {
    outputDir: './downloads',
    quality: 'highest',
    format: 'mp4',
  },
  hookManager
);

// 다운로드 실행
await autosave.download('https://www.youtube.com/watch?v=VIDEO_ID');
```

## Hook Events

| Event | Description | Return |
|-------|-------------|--------|
| `beforeDownload` | 다운로드 시작 전 | `boolean` - false 시 취소 |
| `afterDownload` | 다운로드 완료 후 | `void` |
| `progress` | 다운로드 진행 중 | `void` |
| `beforeSave` | 파일 저장 전 | `boolean` - false 시 취소 |
| `afterSave` | 파일 저장 후 | `void` |
| `error` | 에러 발생 시 | `void` |
| `cancel` | 취소 시 | `void` |

## Configuration

`vibe.config.json` 파일로 설정 관리:

```json
{
  "autosave": {
    "outputDir": "./downloads",
    "filenameTemplate": "{title}_{videoId}",
    "quality": "highest",
    "format": "mp4",
    "maxConcurrent": 3,
    "skipExisting": true,
    "saveMetadata": true
  },
  "hooks": {
    "enabled": true,
    "timeout": 30000,
    "continueOnError": true
  }
}
```

## Examples

예제 파일은 `examples/` 디렉토리에서 확인할 수 있습니다:

- `basic-usage.ts` - 기본 사용법
- `custom-hooks.ts` - 커스텀 Hook 구현
- `batch-download.ts` - 일괄 다운로드

## Development

```bash
# 빌드
npm run build

# 개발 모드
npm run dev

# 타입 체크
npm run watch
```

## Project Structure

```
vibe/
├── src/
│   ├── hooks/           # Hook 시스템
│   │   ├── types.ts     # 타입 정의
│   │   ├── HookManager.ts
│   │   └── index.ts
│   ├── youtube/         # YouTube 다운로드
│   │   ├── types.ts
│   │   ├── YouTubeAutosave.ts
│   │   └── index.ts
│   ├── config/          # 설정 관리
│   │   └── index.ts
│   └── index.ts         # 메인 진입점
├── examples/            # 예제
├── package.json
├── tsconfig.json
└── vibe.config.example.json
```
