import pytest

import json

# from lablib import operators, processors, renderers, utils


# System Constants
FFMPEG_PATH = "vendor/bin/ffmpeg/windows/bin"
OIIO_PATH = "vendor/bin/oiio/windows"
OCIO_PATH = "vendor/bin/ocioconfig/OpenColorIOConfigs/aces_1.2/config.ocio"

# Project Constants
SOURCE_DIR = "resources/public/plateMain/v000"
DATA_PATH = "resources/public/mock_data.json"
EFFECT_PATH = (
    "resources/public/effectPlateMain/v000/BLD_010_0010_effectPlateMain_v000.json"
)
SLATE_TEMPLATE_PATH = "templates/slates/slate_generic/slate_generic.html"
STAGING_DIR = "results"
OUTPUT_WIDTH = 1920
OUTPUT_HEIGHT = 1080

# Get data from Asset
working_data = []
with open(DATA_PATH, "r") as f:
    working_data.append(json.load(f))


@pytest.mark.skip(reason="Test is not implemented yet")
@pytest.mark.parametrize(
    "directory",
    [
        "resources/public/plateMain/v000",
        "resources/public/plateMain/v001",
    ],
)
def test_SequenceInfo(directory):
    # main_seq = operators.SequenceInfo().compute_longest(directory)
    seq_info = operators.SequenceInfo.from_directory(directory)
    # if "v000" in directory:
    #     assert main_seq.frame_start == 1001
    #     assert main_seq.frame_end == 1001
    #     assert main_seq.head == "BLD_010_0010_plateMain_v000."
    #     assert main_seq.tail == ".exr"
    #     assert main_seq.padding == 4
    #     assert main_seq.hash_string == "BLD_010_0010_plateMain_v000.#.exr"
    #     assert main_seq.format_string == r"BLD_010_0010_plateMain_v000.%04d.exr"
    # if "v001" in directory:
    #     assert main_seq.frame_start == 1001
    #     assert main_seq.frame_end == 1003
    #     assert main_seq.head == "BLD_010_0010_plateMain_v001."
    #     assert main_seq.tail == ".exr"
    #     assert main_seq.padding == 4
    #     assert main_seq.hash_string == "BLD_010_0010_plateMain_v001.#.exr"
    #     assert main_seq.format_string == r"BLD_010_0010_plateMain_v001.%04d.exr"


# @pytest.mark.parametrize("dir", ["resources/public/plateMain/v000"])
# def test_ImageInfo(dir):
#     main_seq = operators.ImageInfo().compute_longest(dir)
#     print(f"{main_seq = }")
#     assert main_seq is not None
