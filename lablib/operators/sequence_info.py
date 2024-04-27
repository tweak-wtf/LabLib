from __future__ import annotations

# import subprocess
from dataclasses import dataclass, field
from pathlib import Path
import re

from lablib.operators import BaseOperator
from lablib.utils import get_logger


log = get_logger(__name__)


@dataclass
class SequenceInfo(BaseOperator):
    # path: str = None
    frames: list[str] = field(default_factory=lambda: list([]))
    frame_start: int = None
    frame_end: int = None
    head: str = None
    tail: str = None
    padding: int = 0
    hash_string: str = None
    format_string: str = None

    def __init__(self, path: str | Path):
        super().__init__()

        if isinstance(path, str):
            path = Path(path)

        if not path.is_dir():
            raise NotImplementedError(f"{path} is no directory")

        if path.suffix not in (".exr"):
            raise ValueError(f"Invalid file type: {path}")

        self.path = path
        self.update_from_path(path)

    def update_from_path(self, path: Path) -> None:
        if not path.is_dir():
            raise NotImplementedError(
                "SequenceInfo from a file is not yet implemented."
            )

        for file in path.iterdir():
            head, tail = file.stem, file.suffix
            print(f"{head = }")
            print(f"{tail = }")
            print(f"{file = }")
            matches = re.findall(r"\d+$", head)
            print(f"{matches = }")
            # if file.is_file():
            #     break
        seq = SequenceInfo(path)
        print(f"{seq = }")

        return seq
