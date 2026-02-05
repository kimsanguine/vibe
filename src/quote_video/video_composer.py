"""FFmpeg 영상 합성 모듈."""

import subprocess
from pathlib import Path

from .config import Config, OUTPUT_CLIPS, FONT_PATH


class VideoComposer:
    """FFmpeg를 사용해 이미지 + 오디오 + 자막을 영상으로 합성한다."""

    def __init__(self, config: Config | None = None):
        self.config = config or Config()

    def compose_scene(
        self,
        image_path: str | Path,
        audio_path: str | Path,
        srt_path: str | Path,
        output_path: str | Path | None = None,
        scene_index: int = 1,
    ) -> Path:
        """단일 씬 영상을 합성한다.

        이미지 위에 오디오와 자막을 올리고, fade-in/out 효과를 적용한다.

        Args:
            image_path: 배경 이미지 경로.
            audio_path: 나레이션 WAV 경로.
            srt_path: SRT 자막 경로.
            output_path: 출력 MP4 경로. None이면 output/clips/scene_{index}.mp4.
            scene_index: 씬 번호.

        Returns:
            생성된 MP4 파일 경로.
        """
        image_path = Path(image_path)
        audio_path = Path(audio_path)
        srt_path = Path(srt_path)

        if output_path is None:
            OUTPUT_CLIPS.mkdir(parents=True, exist_ok=True)
            output_path = OUTPUT_CLIPS / f"scene_{scene_index:02d}.mp4"
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

        # 오디오 길이 구하기
        duration = self._get_audio_duration(audio_path)

        # 자막 필터 (폰트 존재 여부에 따라)
        font_path = self.config.font_path
        if font_path.exists():
            subtitle_filter = (
                f"subtitles='{srt_path}':"
                f"force_style='FontName=KOTRA_SONGEULSSI,"
                f"FontSize=28,PrimaryColour=&HFFFFFF,"
                f"OutlineColour=&H000000,Outline=2,"
                f"Alignment=2,MarginV=60'"
            )
        else:
            subtitle_filter = (
                f"subtitles='{srt_path}':"
                f"force_style='FontSize=28,PrimaryColour=&HFFFFFF,"
                f"OutlineColour=&H000000,Outline=2,"
                f"Alignment=2,MarginV=60'"
            )

        # fade 효과
        fade = self.config.fade_duration
        fade_out_start = max(0, duration - fade)

        # FFmpeg 커맨드
        video_filter = (
            f"loop=loop=-1:size=1:start=0,"
            f"trim=duration={duration},"
            f"fps={self.config.video_fps},"
            f"scale={self.config.video_width}:{self.config.video_height}:"
            f"force_original_aspect_ratio=decrease,"
            f"pad={self.config.video_width}:{self.config.video_height}:"
            f"(ow-iw)/2:(oh-ih)/2:color=black,"
            f"fade=t=in:st=0:d={fade},"
            f"fade=t=out:st={fade_out_start}:d={fade},"
            f"{subtitle_filter}"
        )

        audio_filter = (
            f"afade=t=in:st=0:d={fade},"
            f"afade=t=out:st={fade_out_start}:d={fade}"
        )

        cmd = [
            "ffmpeg", "-y",
            "-i", str(image_path),
            "-i", str(audio_path),
            "-vf", video_filter,
            "-af", audio_filter,
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            "-movflags", "+faststart",
            str(output_path),
        ]

        print(f"[VideoComposer] Composing scene {scene_index}...")
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"[VideoComposer] Saved: {output_path}")
        return output_path

    def compose_batch(
        self,
        image_paths: list[Path],
        audio_paths: list[Path],
        srt_paths: list[Path],
    ) -> list[Path]:
        """여러 씬의 영상을 일괄 합성한다."""
        if not (len(image_paths) == len(audio_paths) == len(srt_paths)):
            raise ValueError("image, audio, srt 경로 목록의 길이가 일치해야 합니다.")

        clip_paths = []
        for i, (img, aud, srt) in enumerate(
            zip(image_paths, audio_paths, srt_paths), start=1
        ):
            path = self.compose_scene(
                image_path=img,
                audio_path=aud,
                srt_path=srt,
                scene_index=i,
            )
            clip_paths.append(path)
        return clip_paths

    def concatenate(
        self,
        clip_paths: list[Path],
        output_path: str | Path | None = None,
        bgm_path: str | Path | None = None,
    ) -> Path:
        """여러 클립을 하나의 영상으로 연결하고, 선택적으로 BGM을 믹싱한다.

        Args:
            clip_paths: 클립 MP4 경로 목록.
            output_path: 최종 출력 경로. None이면 output/final_video.mp4.
            bgm_path: BGM 파일 경로. None이면 BGM 없이 합성.

        Returns:
            최종 MP4 파일 경로.
        """
        if output_path is None:
            output_path = self.config.output_dir / "final_video.mp4"
        else:
            output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # concat 리스트 파일 생성
        concat_list = self.config.output_dir / "concat_list.txt"
        with open(concat_list, "w") as f:
            for clip in clip_paths:
                f.write(f"file '{clip.resolve()}'\n")

        if bgm_path is not None:
            bgm_path = Path(bgm_path)
            self._concat_with_bgm(concat_list, bgm_path, output_path)
        else:
            self._concat_simple(concat_list, output_path)

        # concat 리스트 정리
        concat_list.unlink(missing_ok=True)
        print(f"[VideoComposer] Final video: {output_path}")
        return output_path

    def _concat_simple(self, concat_list: Path, output_path: Path) -> None:
        """BGM 없이 클립을 연결한다."""
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_list),
            "-c", "copy",
            "-movflags", "+faststart",
            str(output_path),
        ]
        subprocess.run(cmd, check=True, capture_output=True, text=True)

    def _concat_with_bgm(
        self, concat_list: Path, bgm_path: Path, output_path: Path
    ) -> None:
        """클립을 연결하고 BGM을 믹싱한다."""
        bgm_vol = self.config.bgm_volume

        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_list),
            "-stream_loop", "-1",
            "-i", str(bgm_path),
            "-filter_complex",
            f"[0:a]volume=1.0[narration];"
            f"[1:a]volume={bgm_vol}[bgm];"
            f"[narration][bgm]amix=inputs=2:duration=shortest[aout]",
            "-map", "0:v",
            "-map", "[aout]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            "-movflags", "+faststart",
            str(output_path),
        ]
        subprocess.run(cmd, check=True, capture_output=True, text=True)

    @staticmethod
    def _get_audio_duration(audio_path: Path) -> float:
        """ffprobe로 오디오 파일의 길이(초)를 반환한다."""
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-show_entries", "format=duration",
            "-of", "json",
            str(audio_path),
        ]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        import json
        info = json.loads(result.stdout)
        return float(info["format"]["duration"])
