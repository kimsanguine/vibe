/**
 * 일괄 다운로드 예제
 *
 * 여러 영상을 동시에 다운로드하는 방법을 보여줍니다.
 */

import { YouTubeAutosave, HookManager, DownloadJob } from '../src';

interface BatchResult {
  completed: DownloadJob[];
  failed: DownloadJob[];
  cancelled: DownloadJob[];
}

async function batchDownload(urls: string[]): Promise<BatchResult> {
  const hookManager = new HookManager();
  const autosave = new YouTubeAutosave(
    {
      outputDir: './downloads/batch',
      maxConcurrent: 3, // 동시 3개 다운로드
      retryCount: 2,
      skipExisting: true,
    },
    hookManager
  );

  const result: BatchResult = {
    completed: [],
    failed: [],
    cancelled: [],
  };

  // 진행 상황 추적
  const jobStatuses = new Map<string, string>();

  hookManager.register('progress', (progress) => {
    jobStatuses.set(progress.videoId, `${progress.percent.toFixed(0)}%`);
    printProgress(jobStatuses);
  });

  // 결과 수집
  autosave.on('completed', (job) => {
    result.completed.push(job);
    jobStatuses.set(job.videoId, '✅');
    printProgress(jobStatuses);
  });

  autosave.on('failed', (job) => {
    result.failed.push(job);
    jobStatuses.set(job.videoId, '❌');
    printProgress(jobStatuses);
  });

  autosave.on('cancelled', (job) => {
    result.cancelled.push(job);
    jobStatuses.set(job.videoId, '⏹️');
    printProgress(jobStatuses);
  });

  // 일괄 다운로드 시작
  console.log('='.repeat(50));
  console.log(`📥 일괄 다운로드 시작 (${urls.length}개 영상)`);
  console.log('='.repeat(50));

  const jobs = await autosave.downloadBatch(urls);

  // 초기 상태 설정
  jobs.forEach((job) => {
    jobStatuses.set(job.videoId, '⏳');
  });

  // 모든 작업 완료 대기
  await waitForCompletion(autosave, jobs.length);

  // 결과 출력
  console.log('\n\n' + '='.repeat(50));
  console.log('📊 다운로드 결과');
  console.log('='.repeat(50));
  console.log(`✅ 성공: ${result.completed.length}`);
  console.log(`❌ 실패: ${result.failed.length}`);
  console.log(`⏹️ 취소: ${result.cancelled.length}`);

  if (result.completed.length > 0) {
    console.log('\n완료된 파일:');
    result.completed.forEach((job) => {
      console.log(`  - ${job.filePath}`);
    });
  }

  if (result.failed.length > 0) {
    console.log('\n실패한 영상:');
    result.failed.forEach((job) => {
      console.log(`  - ${job.videoId}: ${job.error?.message}`);
    });
  }

  return result;
}

function printProgress(statuses: Map<string, string>): void {
  const lines = Array.from(statuses.entries())
    .map(([id, status]) => `${id.substring(0, 8)}...: ${status}`)
    .join(' | ');

  process.stdout.write(`\r${lines}${' '.repeat(20)}`);
}

function waitForCompletion(autosave: YouTubeAutosave, totalCount: number): Promise<void> {
  return new Promise((resolve) => {
    let completedCount = 0;

    const checkDone = () => {
      completedCount++;
      if (completedCount >= totalCount) {
        resolve();
      }
    };

    autosave.on('completed', checkDone);
    autosave.on('failed', checkDone);
    autosave.on('cancelled', checkDone);
  });
}

// 예시 실행
async function main() {
  // 테스트용 URL 목록
  const testUrls = [
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'https://www.youtube.com/watch?v=9bZkp7q19f0',
    'https://www.youtube.com/watch?v=kJQP7kiw5Fk',
  ];

  try {
    await batchDownload(testUrls);
  } catch (error) {
    console.error('에러 발생:', error);
  }
}

main().catch(console.error);
