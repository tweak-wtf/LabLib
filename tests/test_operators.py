import pytest
from pathlib import Path

from lablib.operators import ImageInfo
from lablib.utils import get_logger

log = get_logger(__name__)


@pytest.mark.parametrize(
    "path", ["resources/public/plateMain/v000/BLD_010_0010_plateMain_v000.1001.exr"]
)
def test_ImageInfo(path: str, caplog):
    image_info = ImageInfo(path)
    path = Path(path)
    log.info(f"{image_info = }")
    assert image_info.width == 4382
    assert image_info.height == 2310
    assert image_info.timecode == "02:10:04:17"
    assert image_info.fps == 25.0
    assert image_info.channels == 3
    assert image_info.par == 1.0
    assert image_info.filename == path.name
    assert image_info.filepath == path
