from __future__ import annotations
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ImageInfo:
    file_path: Path = None
    filename: str = None
    origin_x: int = 0
    origin_y: int = 0
    width: int = 1920
    height: int = 1080
    display_width: int = 1920
    display_height: int = 1080
    channels: int = 3
    fps: float = 24.0
    par: float = 1.0
    timecode: str = "01:00:00:01"

    def __run_command(self, cmd: list[str]) -> list[str]:
        result = (
            subprocess.run(cmd, capture_output=True, text=True)
            .stdout.strip()
            .splitlines()
        )
        return result

    def update_from_ffprobe(self) -> None:
        abspath = str(self.file_path.resolve())
        cmd = [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "format_tags=timecode:stream_tags=timecode:stream=width,height,r_frame_rate,sample_aspect_ratio",
            "-of",
            "default=noprint_wrappers=1",
            abspath,
        ]
        print(f"running ffprobe with: {cmd}")
        for line in self.__run_command(cmd):
            # print(f"{line = }")
            vars = line.split("=")
            if "width" in vars[0]:
                self.display_width = int(vars[1].strip())
            if "height" in vars[0]:
                self.display_height = int(vars[1].strip())
            if "r_frame_rate" in vars[0]:
                rate = vars[1].split("/")
                self.fps = float(
                    round(float(int(rate[0].strip()) / int(rate[1].strip())), 3)
                )
            if "timecode" in line:
                self.timecode = vars[1]
            if "sample_aspect_ratio" in line:
                par = vars[1].split(":")
                if vars[1] != "N/A":
                    self.par = float(int(par[0].strip()) / int(par[1].strip()))
                else:
                    self.par = 1

    def update_from_iinfo(self) -> None:
        abspath = str(self.file_path.resolve())
        cmd = ["iinfo", "-v", abspath]
        print(f"running iinfo with: {cmd}")
        for line in self.__run_command(cmd):
            # print(f"{line = }")
            if abspath in line and line.find(abspath) < 2:
                vars = line.split(": ")[1].split(",")
                size = vars[0].strip().split("x")
                channels = vars[1].strip().split(" ")
                self.width = int(size[0].strip())
                self.height = int(size[1].strip())
                self.display_width = int(size[0].strip())
                self.display_height = int(size[1].strip())
                self.channels = int(channels[0].strip())
            if "FramesPerSecond" in line or "framesPerSecond" in line:
                vars = line.split(": ")[1].strip().split(" ")[0].split("/")
                self.fps = float(round(float(int(vars[0]) / int(vars[1])), 3))
            if "full/display size" in line:
                size = line.split(": ")[1].split("x")
                self.display_width = int(size[0].strip())
                self.display_height = int(size[1].strip())
            if "pixel data origin" in line:
                origin = line.split(": ")[1].strip().split(",")
                self.origin_x = (int(origin[0].replace("x=", "").strip()),)
                self.origin_y = (int(origin[1].replace("y=", "").strip()),)
            if "smpte:TimeCode" in line:
                self.timecode = line.split(": ")[1].strip()
            if "PixelAspectRatio" in line:
                self.par = float(line.split(": ")[1].strip())

    @classmethod
    def from_path(cls, path: str | Path) -> ImageInfo:
        if isinstance(path, str):
            path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if path.suffix not in (".exr"):
            raise ValueError(f"Invalid file type: {path}")

        result = ImageInfo(file_path=path)
        result.update_from_iinfo()
        print(f"{result = }")
        result.update_from_ffprobe()
        print(f"{result = }")

        return result
