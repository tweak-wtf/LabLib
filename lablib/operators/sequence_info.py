from __future__ import annotations

# import subprocess
from dataclasses import dataclass, field
from pathlib import Path
import re

from lablib.operators import BaseOperator, ImageInfo
from lablib.utils import get_logger


log = get_logger(__name__)


@dataclass
class SequenceInfo(BaseOperator):
    # path: str = None

    frames: list[ImageInfo] = list[ImageInfo]
    frame_start: int = None
    frame_end: int = None
    # head: str = None
    # tail: str = None
    padding: int = 0
    hash_string: str = None
    format_string: str = None

    def __init__(self, path: str | Path):
        super().__init__(path)

        self.update_from_path(self.path)

    @classmethod
    def scan(cls, path: str | Path) -> list[SequenceInfo]:
        if not isinstance(path, Path):
            path = Path(path)

        if not path.is_dir():
            raise NotImplementedError(f"{path} is no directory")

        files_map = {}
        for item in path.iterdir():
            if not item.is_file():
                continue
            if item.suffix not in (".exr"):
                cls.log.warning(f"{item.suffix} not in (.exr)")
                continue

            if re.findall(r"\.(\d+)", item.stem):
                name = item.stem.split(".")[0]
            else:
                name = item.stem
            cls.log.info(f"{name = }")

            if name not in files_map.keys():
                files_map[name] = []
            files_map[name].append(ImageInfo(item))

        for seq_name, seq_files in files_map.items():
            cls.log.info(f"{seq_name = }")
            cls.log.info(f"{seq_files = }")
            cls.log.info(f"{len(seq_files) = }")

    def update_from_path(self, path: Path) -> None:
        if not path.is_dir():
            raise NotImplementedError(
                "SequenceInfo from a file is not yet implemented."
            )
