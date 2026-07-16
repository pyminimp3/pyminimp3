##
## NOTE: These tests are initial tests that test the core API bindings. They
##       will be migrated to tests that instead test the public API when the
##       public API is ready

import itertools
import sys
import wave
from array import array
from pathlib import Path

import pytest

import pyminimp3

# Data files
DATA_PATH = Path(__file__).parent / "data"

MP3_FILES = (
    "dwd_diabolic_10s.mp3",
    "meganeko_discovery_10s.mp3",
    "meganeko_discovery_10s_middle.mp3",
)


def _get_sound_files():
    sound_files = []
    for fname in MP3_FILES:
        mp3_path = DATA_PATH / fname
        wav_path = str(mp3_path.with_suffix(".wav"))
        sound_files.append((mp3_path, wav_path))

    return sound_files


SOUND_FILES = _get_sound_files()

# Each fixture starts with a 1152-sample Xing/LAME information frame.  FFmpeg
# omits that frame from the reference WAV and skips another 529 samples of MP3
# decoder delay.
REFERENCE_SAMPLE_DELAY = 1152 + 529

# Layer III frames may depend on the bit reservoir populated by earlier frames.
WARMUP_FRAME_COUNT = 4


def _read_wav_samples(wav_path, start, frame_count):
    with wave.open(wav_path, "rb") as wav_file:
        wav_file.setpos(start)
        wav_bytes = wav_file.readframes(frame_count)
        channel_count = wav_file.getnchannels()

    interleaved_samples = array("h")
    interleaved_samples.frombytes(wav_bytes)
    if sys.byteorder != "little":
        interleaved_samples.byteswap()

    return tuple(
        interleaved_samples[channel::channel_count] for channel in range(channel_count)
    )


def _join_frame_samples(frames):
    channel_count = frames[0].channels
    assert all(frame.channels == channel_count for frame in frames)

    return tuple(
        array(
            "h",
            itertools.chain.from_iterable(frame.samples[channel] for frame in frames),
        )
        for channel in range(channel_count)
    )


def _assert_samples_match(actual, expected):
    assert len(actual) == len(expected)

    for channel in range(len(actual)):
        actual_channel = actual[channel]
        expected_channel = expected[channel]
        assert len(actual_channel) == len(expected_channel)
        assert actual_channel

        max_difference = max(
            abs(actual_channel[index] - expected_channel[index])
            for index in range(len(actual_channel))
        )
        assert max_difference <= 1


# Tests
@pytest.mark.parametrize("mp3_path, wav_path", SOUND_FILES)
@pytest.mark.parametrize("frame_count", (1, 2), ids=("single", "multiple"))
def test_decode_frames(mp3_path, wav_path, frame_count):
    frames_to_read = WARMUP_FRAME_COUNT + frame_count
    with open(mp3_path, "rb") as mp3_file:
        frames = tuple(pyminimp3.load_frame(mp3_file) for _ in range(frames_to_read))

    decoded_frames = frames[-frame_count:]
    actual_samples = _join_frame_samples(decoded_frames)
    sample_count = len(actual_samples[0])

    samples_before_decoded_frames = sum(
        len(frame.samples[0]) for frame in frames[:-frame_count]
    )
    reference_start = samples_before_decoded_frames - REFERENCE_SAMPLE_DELAY
    expected_samples = _read_wav_samples(
        wav_path,
        reference_start,
        sample_count,
    )

    _assert_samples_match(actual_samples, expected_samples)
