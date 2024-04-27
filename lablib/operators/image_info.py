from __future__ import annotations
import subprocess
from dataclasses import dataclass
from pathlib import Path

# from lablib.utils import read_image_info


def get_iinfo_output(path: Path) -> list[str]:
    abspath: str = path.as_posix()
    cmd = ["iinfo", "-v", abspath]
    print(f"{cmd = }")
    _out = (
        subprocess.run(cmd, capture_output=True, text=True).stdout.strip().splitlines()
    )

    result = {  # NOTE: that's basically ImageInfo
        "filename": abspath,
        "origin_x": None,
        "origin_y": None,
        "width": None,
        "height": None,
        "display_width": None,
        "display_height": None,
        "channels": None,
        "fps": None,
        "par": None,
        "timecode": None,
    }
    for l in _out:
        if abspath in l and l.find(abspath) < 2:
            vars = l.split(": ")[1].split(",")
            size = vars[0].strip().split("x")
            channels = vars[1].strip().split(" ")
            result.update(
                {
                    "width": int(size[0].strip()),
                    "height": int(size[1].strip()),
                    "display_width": int(size[0].strip()),
                    "display_height": int(size[1].strip()),
                    "channels": int(channels[0].strip()),
                }
            )
        if "FramesPerSecond" in l or "framesPerSecond" in l:
            vars = l.split(": ")[1].strip().split(" ")[0].split("/")
            result.update({"fps": float(round(float(int(vars[0]) / int(vars[1])), 3))})
        if "full/display size" in l:
            size = l.split(": ")[1].split("x")
            result.update(
                {
                    "display_width": int(size[0].strip()),
                    "display_height": int(size[1].strip()),
                }
            )
        if "pixel data origin" in l:
            origin = l.split(": ")[1].strip().split(",")
            result.update(
                {
                    "origin_x": int(origin[0].replace("x=", "").strip()),
                    "origin_y": int(origin[1].replace("y=", "").strip()),
                }
            )
        if "smpte:TimeCode" in l:
            result["timecode"] = l.split(": ")[1].strip()
        if "PixelAspectRatio" in l:
            result["par"] = float(l.split(": ")[1].strip())

    return result


def get_ffprobe_output(path: Path) -> list[str]:
    abspath: str = path.as_posix()
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
        path,
    ]
    result = (
        subprocess.run(cmd, capture_output=True, text=True).stdout.strip().splitlines()
    )

    return out


@dataclass
class ImageInfo:
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

    @classmethod
    def from_path(cls, path: str | Path) -> ImageInfo:
        if isinstance(path, str):
            path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if path.suffix not in (".exr"):
            raise ValueError(f"Invalid file type: {path}")

        iinfo_out = get_iinfo_output(path)
        result = ImageInfo(**iinfo_out)
        print(f"{iinfo_out = }")
        print(f"{result = }")

        return result
