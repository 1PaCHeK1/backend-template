from __future__ import annotations

import contextlib
import mimetypes
from collections.abc import AsyncIterator, Sequence
from io import BytesIO
from os import PathLike
from pathlib import PurePath
from types import TracebackType
from typing import TYPE_CHECKING, Final, Literal, Self
from urllib.parse import urlsplit

from botocore.exceptions import ClientError
from result import Err, Ok, Result

from .errors import UploadS3Error

if TYPE_CHECKING:
    from types_aiobotocore_s3 import S3Client


from .dto import FilePartDTO, UploadedFileDTO, UploadFileDTO

Path = PathLike[str] | str


class S3Storage:
    def __init__(
        self,
        client: S3Client,
        bucket: str,
        endpoint_url: str,
        addressing_style: Literal["virtual", "path"],
    ) -> None:
        self._client: Final = client
        self._endpoint_url: Final = endpoint_url
        self._bucket: Final = bucket
        self._addressing_style = addressing_style

    def generate_public_url(self, key: Path) -> str:
        key = PurePath(key).as_posix()

        match self._addressing_style:
            case "path":
                return f"{self._endpoint_url}/{self._bucket}/{key}"
            case "virtual":
                result = urlsplit(self._endpoint_url)
                return f"{result.scheme}://{self._bucket}.{result.netloc}/{key}"
            case _:
                raise ValueError

    async def download_object(self, path: Path) -> Result[BytesIO, ClientError]:
        file_stream = BytesIO()
        try:
            await self._client.download_fileobj(
                Bucket=self._bucket,
                Key=PurePath(path).as_posix(),
                Fileobj=file_stream,
            )
        except ClientError as ex:
            return Err(ex)

        return Ok(file_stream)

    async def delete_object(self, path: Path) -> None:
        await self._client.delete_object(
            Bucket=self._bucket,
            Key=PurePath(path).as_posix(),
        )

    async def delete_objects(self, paths: Sequence[Path]) -> None:
        await self._client.delete_objects(
            Bucket=self._bucket,
            Delete={
                "Objects": [
                    {
                        "Key": PurePath(path).as_posix(),
                    }
                    for path in paths
                ],
            },
        )

    def multipart_upload(self, path: Path) -> _S3MultipartUpload:
        return _S3MultipartUpload(
            client=self._client,
            path=PurePath(path),
            bucket=self._bucket,
        )

    @contextlib.asynccontextmanager
    async def upload_object(self, dto: UploadFileDTO) -> AsyncIterator[UploadedFileDTO]:
        uploaded_dto = await self._upload_object(dto)
        try:
            yield uploaded_dto
        except BaseException as ex:
            await self.delete_object(uploaded_dto.path)
            msg = "An error occurred after downloading the file"
            raise UploadS3Error(msg) from ex

    async def _upload_object(self, dto: UploadFileDTO) -> UploadedFileDTO:
        mimetype, _ = mimetypes.guess_type(url=dto.path)
        await self._client.put_object(
            Body=dto.io,
            Bucket=self._bucket,
            Key=dto.path.as_posix(),
            ContentType=mimetype or "binary/octet-stream",
        )
        return UploadedFileDTO(
            path=dto.path,
            url=self.generate_public_url(dto.path),
        )


class _S3MultipartUpload:
    def __init__(
        self,
        client: S3Client,
        path: PurePath,
        bucket: str,
    ) -> None:
        self._s3_client = client
        self._bucket = bucket
        self._path_key = path.as_posix()
        self._upload_id = ""
        self._e_tags: list[tuple[int, str]] = []
        self._part_number = 0

    async def __aenter__(self) -> Self:
        self._upload_id = await self._create_multipart_upload()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_val is not None:
            await self._abort_multipart_upload()

        await self._complete_multipart_upload()

    async def upload_part(self, chunk: bytes) -> None:
        self._part_number += 1
        dto = FilePartDTO(
            chunk=chunk,
            part_number=self._part_number,
        )
        e_tag = await self._upload_part(dto)
        self._e_tags.append((self._part_number, e_tag))

    async def _upload_part(
        self,
        dto: FilePartDTO,
    ) -> str:
        response = await self._s3_client.upload_part(
            Bucket=self._bucket,
            Key=self._path_key,
            Body=dto.chunk,
            PartNumber=dto.part_number,
            UploadId=self._upload_id,
        )
        return response["ETag"].replace('"', "")

    async def _create_multipart_upload(self) -> str:
        response = await self._s3_client.create_multipart_upload(
            Bucket=self._bucket,
            Key=self._path_key,
        )
        return response["UploadId"]

    async def _complete_multipart_upload(self) -> int:
        response = await self._s3_client.complete_multipart_upload(
            Bucket=self._bucket,
            Key=self._path_key,
            UploadId=self._upload_id,
            MultipartUpload={
                "Parts": [
                    {"PartNumber": part_number, "ETag": e_tag}
                    for part_number, e_tag in self._e_tags
                ],
            },
        )
        return response["ResponseMetadata"]["HTTPStatusCode"]

    async def _abort_multipart_upload(self) -> int:
        response = await self._s3_client.abort_multipart_upload(
            Bucket=self._bucket,
            Key=self._path_key,
            UploadId=self._upload_id,
        )
        return response["ResponseMetadata"]["HTTPStatusCode"]
