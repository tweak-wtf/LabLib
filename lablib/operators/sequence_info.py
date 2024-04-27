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
    head: str = None
    tail: str = None
    padding: int = 0
    hash_string: str = None
    format_string: str = None

    def __init__(self, path: str | Path):
        super().__init__(path)
        self.log.debug(f"{self.path.suffix = }")
        if not self.path.is_dir():
            raise NotImplementedError(f"{path} is no directory")

        if self.path.suffix not in (".exr"):
            raise ValueError(f"Invalid file type: {path}")

        self.update_from_path(self.path)

    def update_from_path(self, path: Path) -> None:
        if not path.is_dir():
            raise NotImplementedError(
                "SequenceInfo from a file is not yet implemented."
            )

        sequenced_files = []
        matched_files = []
        for file in path.iterdir():
            head, tail = file.stem, file.suffix
            self.log.debug(f"{head = }")
            self.log.debug(f"{tail = }")
            self.log.debug(f"{file = }")
            matches = re.findall(r"\d+$", head)
            self.log.debug(f"{matches = }")
            if matches:
                sequenced_files.append(file)
                matched_files.append(head.replace(matches[0], ""))
            matched_files = list(set(matched_files))

            # if file.is_file():
            #     break
        # seq = SequenceInfo(path)
        # print(f"{seq = }")

        # return seq


#
