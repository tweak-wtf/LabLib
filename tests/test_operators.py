import pytest

from lablib.operators import ImageInfo


@pytest.mark.parametrize(
    "path", ["resources/public/plateMain/v000/BLD_010_0010_plateMain_v000.1001.exr"]
)
def test_ImageInfo(path: str, caplog):
    image_info = ImageInfo.from_path(path)
    assert image_info.width == 4382
    assert image_info.height == 2310
    assert image_info.timecode == "02:10:04:17"
    assert image_info.fps == 25.0
