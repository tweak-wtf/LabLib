import pytest
import logging
from pathlib import Path

from lablib.operators import ImageInfo, SequenceInfo

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


@pytest.mark.parametrize(
    "path", ["resources/public/plateMain/v000/BLD_010_0010_plateMain_v000.1001.exr"]
)
def test_ImageInfo(path: str):
    image_info = ImageInfo(path)
    path = Path(path)
    log.info(f"{image_info = }")
    assert image_info.par == 1.0
    assert image_info.fps == 25.0
    assert image_info.width == 4382
    assert image_info.height == 2310
    assert image_info.channels == 3
    assert image_info.filepath == path
    assert image_info.filename == path.name
    assert image_info.timecode == "02:10:04:17"


def test_single_frame_sequence():
    path = Path("resources/public/plateMain/v000")
    seq_info = SequenceInfo.scan(path)
    log.info(f"{seq_info = }")
    assert seq_info.path == path
    assert seq_info.hash_string == "BLD_010_0010_plateMain_v000.1001#1.exr"
    assert seq_info.start_frame == 1001
    assert seq_info.end_frame == 1001
    assert seq_info.padding == 4


def test_SequenceInfo_missing_frames():
    path = Path("resources/public/plateMain/v001")
    seq_info = SequenceInfo.scan(path)
    log.info(f"{seq_info = }")
    assert seq_info.path == path
    # assert seq_info.version == 1
    assert seq_info.start_frame == 1001
    assert seq_info.end_frame == 1003
    # assert seq_info.hash_string == "v002.1001#exr"
