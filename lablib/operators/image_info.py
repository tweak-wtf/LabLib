from __future__ import annotations
import subprocess
from dataclasses import dataclass
from pathlib import Path

from lablib.utils import get_logger


log = get_logger(__name__)


@dataclass
class ImageInfo:
    filepath: Path = None
    filename: str = None
    origin_x: int = 0
    origin_y: int = 0
    width: int = 1920
    height: int = 1080
    display_width: int = width
    display_height: int = height
    channels: int = 3
    fps: float = 24.0
    par: float = 1.0
    timecode: str = "01:00:00:01"

    def __init__(self, path: str | Path):
        super().__init__()

        if isinstance(path, str):
            path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if path.suffix not in (".exr"):
            raise ValueError(f"Invalid file type: {path}")

        self.filepath = path
        self.filename = path.name

        self.update_from_file()

    def __getitem__(self, k: str) -> any:
        return getattr(self, k)

    def __setitem__(self, k: str, v: any) -> None:
        if hasattr(self, k):
            log.debug(f"Setting {k} to {v}")
            setattr(self, k, v)
        else:
            log.error(f"Cannot set {k}={v}. Key {k} not found.", stack_info=True)

    def __run_command(self, cmd: list[str]) -> list[str]:
        log.debug(f"Running command with : {cmd}")
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        out, err = proc.communicate(timeout=2)
        if err:
            log.error(f"Error running command: {err}")
        # subprocess.run(cmd, capture_output=True, text=True)
        # result = out.strip().splitlines()
        result = [line.decode("utf-8").strip() for line in out.splitlines()]

        return result

    def __call_ffprobe(self) -> None:
        abspath = str(self.filepath.resolve())
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
        result = {}
        for line in self.__run_command(cmd):
            vars = line.split("=")
            if "width" in vars[0]:
                result["display_width"] = int(vars[1].strip())
            if "height" in vars[0]:
                result["display_height"] = int(vars[1].strip())
            if "r_frame_rate" in vars[0]:
                rate = vars[1].split("/")
                result["fps"] = float(
                    round(float(int(rate[0].strip()) / int(rate[1].strip())), 3)
                )
            if "timecode" in line:
                result["timecode"] = vars[1]
            if "sample_aspect_ratio" in line:
                par = vars[1].split(":")
                if vars[1] != "N/A":
                    result["par"] = float(int(par[0].strip()) / int(par[1].strip()))
                else:
                    result["par"] = 1

        return result

    def __call_iinfo(self) -> None:
        abspath = str(self.filepath.resolve())
        cmd = ["iinfo", "-v", abspath]
        result = {}
        for line in self.__run_command(cmd):
            if abspath in line and line.find(abspath) < 2:
                vars = line.split(": ")[1].split(",")
                size = vars[0].strip().split("x")
                channels = vars[1].strip().split(" ")
                result["width"] = int(size[0].strip())
                result["height"] = int(size[1].strip())
                result["display_width"] = int(size[0].strip())
                result["display_height"] = int(size[1].strip())
                result["channels"] = int(channels[0].strip())
            if "FramesPerSecond" in line or "framesPerSecond" in line:
                vars = line.split(": ")[1].strip().split(" ")[0].split("/")
                result["fps"] = float(round(float(int(vars[0]) / int(vars[1])), 3))
            if "full/display size" in line:
                size = line.split(": ")[1].split("x")
                result["display_width"] = int(size[0].strip())
                result["display_height"] = int(size[1].strip())
            if "pixel data origin" in line:
                origin = line.split(": ")[1].strip().split(",")
                result["origin_x"] = (int(origin[0].replace("x=", "").strip()),)
                result["origin_y"] = (int(origin[1].replace("y=", "").strip()),)
            if "smpte:TimeCode" in line:
                result["timecode"] = line.split(": ")[1].strip()
            if "PixelAspectRatio" in line:
                result["par"] = float(line.split(": ")[1].strip())

        return result

    def update_from_file(self, force_ffprobe=True) -> None:
        iinfo_res = self.__call_iinfo()
        log.debug(f"{iinfo_res = }")
        for k, v in iinfo_res.items():
            if not v:
                continue
            self[k] = v

        ffprobe_res = self.__call_ffprobe()
        log.debug(f"{ffprobe_res = }")
        for k, v in ffprobe_res.items():
            if not v:
                continue
            if self[k] != v:
                if force_ffprobe:
                    log.debug(f"Updating {k} from {self[k]} to {v}")
                    self[k] = v
                else:
                    log.warning(
                        f"Values do not match: {k} - {self[k]} != {v} - {ffprobe_res[k]}"
                    )
