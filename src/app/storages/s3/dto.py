from dataclasses import dataclass
from pathlib import PurePath
from typing import BinaryIO


@dataclass(frozen=True, slots=True, kw_only=True)
class FilePartDTO:
    chunk: bytes
    part_number: int


@dataclass(frozen=True, slots=True, kw_only=True)
class FileDto:
    io: BinaryIO
    filename: str


@dataclass(frozen=True, slots=True, kw_only=True)
class UploadFileDTO:
    io: BinaryIO
    path: PurePath


@dataclass(frozen=True, slots=True, kw_only=True)
class UploadedFileDTO:
    path: PurePath
    url: str
