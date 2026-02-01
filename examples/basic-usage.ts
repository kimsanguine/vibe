/**
 * 기본 사용 예제
 *
 * 실행: npx ts-node examples/basic-usage.ts
 */

import { YouTubeAutosave, HookManager, VideoInfo, DownloadProgress, SaveInfo } from '../src';

async function main() {
  // Hook Manager 생성
  const hookManager = new HookManager({
    enabled: true,
    timeout: 60000,
    continueOnError: true,
  });

  // Hook 등록: 다운로드 전 검증
  hookManager.register('beforeDownload', async (videoInfo: VideoInfo) => {
    console.log(`\n📹 비디오 정보:`);
    console.log(`   제목: ${videoInfo.title}`);
    console.log(`   채널: ${videoInfo.author}`);
    console.log(`   길이: ${Math.floor(videoInfo.lengthSeconds / 60)}분 ${videoInfo.lengthSeconds % 60}초`);
    console.log(`   조회수: ${videoInfo.viewCount.toLocaleString()}`);

    // 10분 이상 영상은 스킵 (예시)
    if (videoInfo.lengthSeconds > 600) {
      console.log('   ⚠️ 10분 초과 영상 - 스킵');
      return false;
    }

    return true;
  });

  // Hook 등록: 진행률 표시
  hookManager.register('progress', (progress: DownloadProgress) => {
    const percent = progress.percent.toFixed(1);
    const downloaded = (progress.downloaded / 1024 / 1024).toFixed(2);
    const total = (progress.total / 1024 / 1024).toFixed(2);
    process.stdout.write(`\r   ⬇️ 다운로드 중: ${percent}% (${downloaded}MB / ${total}MB)`);
  });

  // Hook 등록: 저장 전 처리
  hookManager.register('beforeSave', async (saveInfo: SaveInfo) => {
    console.log(`\n\n💾 저장 정보:`);
    console.log(`   경로: ${saveInfo.filePath}`);
    console.log(`   크기: ${(saveInfo.fileSize / 1024 / 1024).toFixed(2)}MB`);
    console.log(`   포맷: ${saveInfo.format}`);
    return true;
  });

  // Hook 등록: 저장 완료 후 처리
  hookManager.register('afterSave', async (saveInfo: SaveInfo) => {
    console.log(`   ✅ 저장 완료!`);
  });

  // Hook 등록: 에러 처리
  hookManager.register('error', async (errorInfo) => {
    console.error(`\n❌ 에러 발생: ${errorInfo.error.message}`);
    console.error(`   컨텍스트: ${errorInfo.context}`);
  });

  // YouTubeAutosave 인스턴스 생성
  const autosave = new YouTubeAutosave(
    {
      outputDir: './downloads',
      quality: 'highest',
      format: 'mp4',
      skipExisting: true,
      saveMetadata: true,
    },
    hookManager
  );

  // 이벤트 리스너 등록
  autosave.on('queued', (job) => {
    console.log(`\n📥 대기열 추가: ${job.videoId}`);
  });

  autosave.on('completed', (job) => {
    console.log(`\n🎉 완료: ${job.filePath}`);
  });

  autosave.on('failed', (job, error) => {
    console.error(`\n💥 실패: ${job.videoId} - ${error.message}`);
  });

  // 다운로드 실행
  try {
    console.log('='.repeat(50));
    console.log('YouTube 자동저장 시작');
    console.log('='.repeat(50));

    // 예시 URL (실제 사용시 유효한 URL로 변경)
    const testUrl = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ';

    const job = await autosave.download(testUrl);
    console.log(`\n작업 ID: ${job.id}`);

    // 완료 대기
    await new Promise<void>((resolve) => {
      autosave.on('completed', () => resolve());
      autosave.on('failed', () => resolve());
      autosave.on('cancelled', () => resolve());
    });

    console.log('\n' + '='.repeat(50));
    console.log('작업 완료!');
    console.log('='.repeat(50));
  } catch (error) {
    console.error('실행 에러:', error);
  }
}

main().catch(console.error);
