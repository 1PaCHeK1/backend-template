from typing import TYPE_CHECKING, NewType

if TYPE_CHECKING:
    from types_aiobotocore_s3 import S3Client
else:
    S3Client = NewType("S3Client", int)
