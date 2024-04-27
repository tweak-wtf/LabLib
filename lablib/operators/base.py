from dataclasses import dataclass
from pathlib import Path

from lablib.utils import get_logger

log = get_logger(__name__)


@dataclass
class BaseOperator:
    path: Path | None = None
    log = get_logger(__name__)

    def __init__(self, *args, **kwargs):
        super().__init__()
        if len(args) > 0:
            path = args[0]
            if isinstance(path, Path):
                self.path = path

            if isinstance(path, str):
                self.path = Path(path)

    def __getitem__(self, k: str) -> any:
        return getattr(self, k)

    def __setitem__(self, k: str, v: any) -> None:
        if hasattr(self, k):
            log.debug(f"Setting {k} to {v}")
            setattr(self, k, v)
        else:
            log.error(f"Cannot set {k}={v}. Key {k} not found.", stack_info=True)

    def update_from_path(self, path: Path) -> None:
        raise NotImplementedError("update_from_path method not implemented.")
