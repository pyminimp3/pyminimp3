import array
import typing

class Frame:
    samples: tuple[array.array[int], ...]
    channels: int
    hz: int
    layer: int
    bitrate_kbps: int

    def __init__(
        self,
        samples: tuple[array.array[int], ...],
        hz: int,
        layer: int,
        bitrate_kbps: int,
    ) -> None: ...

def load_frame(mp3_fobj: typing.BinaryIO, buf_size: int = ...) -> Frame: ...

class InsufficientData(ValueError): ...
class InvalidDataError(ValueError): ...
