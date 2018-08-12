##
## NOTE: These tests are initial tests that test the core API bindings. They
##       will be migrated to tests that instead test the public API when the
##       public API is ready

from pyminimp3._backend import load_frame

import wave
from array import array

from pathlib import Path

import pytest

# Data files
DATA_PATH = Path(__file__).parent / 'data'

MP3_FILES = (
    'dwd_diabolic_10s.mp3',
    'meganeko_discovery_10s.mp3',
    'meganeko_discovery_10s_middle.mp3',
)

def _get_sound_files():
    sound_files = []
    for fname in MP3_FILES:
        mp3_path = DATA_PATH / fname
        wav_path = str(mp3_path.with_suffix('.wav'))
        sound_files.append((mp3_path, wav_path))

    return sound_files

SOUND_FILES = _get_sound_files()

# Tests
@pytest.mark.parametrize('mp3_path, wav_path', SOUND_FILES)
def test_decode_frame(mp3_path, wav_path):
    # Test that a single frame can be decoded
    with open(mp3_path, 'rb') as f:
        samples = load_frame(f)

    with wave.open(wav_path, 'rb') as f:
        wav_bytes = f.readframes(len(samples) // f.getnchannels())
        wav_samples = array('h')
        wav_samples.frombytes(wav_bytes)

    assert samples == wav_samples


@pytest.mark.parametrize('mp3_path, wav_path', SOUND_FILES)
def test_decode_multi_frames(mp3_path, wav_path):
    with open(mp3_path, 'rb') as f:
        frames = load_frame(f)
        frames.extend(load_frame(f))

    with wave.open(wav_path, 'rb') as f:
        wav_bytes = f.readframes(len(frames) // f.getnchannels())
        wav_samples = array('h')
        wav_samples.frombytes(wav_bytes)

