from __future__ import annotations

# import subprocess
from dataclasses import dataclass
from pathlib import Path

from lablib.operators import BaseOperator
from lablib.utils import call_iinfo, call_ffprobe


@dataclass
class ImageInfo(BaseOperator):
    # filepath: Path = None
    # filename: str = None
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
        super().__init__(path)

        if not self.path.exists():
            raise FileNotFoundError(f"File not found: {self.path}")

        if self.path.suffix not in (".exr"):
            raise ValueError(f"Invalid file type: {self.path}")

        self.filename = self.path.name
        self.update_from_path()

    def update_from_path(self, force_ffprobe=True) -> None:
        iinfo_res = call_iinfo(self.path)
        for k, v in iinfo_res.items():
            if not v:
                continue
            self[k] = v

        ffprobe_res = call_ffprobe(self.path)
        for k, v in ffprobe_res.items():
            if not v:
                continue
            if self[k] != v:
                if force_ffprobe:
                    self.log.info(f"Updating {k} from {self[k]} to {v}")
                    self[k] = v
                else:
                    self.log.warning(
                        f"Values do not match: {k} - {self[k]} != {v} - {ffprobe_res[k]}"
                    )
