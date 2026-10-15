import boto3

from ..config import settings


class S3Service:

    def __init__(self):

        self.client = boto3.client(
            "s3",
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name=settings.S3_REGION,
        )

        self.bucket = settings.S3_BUCKET_NAME


    def upload_file(
        self,
        file_bytes: bytes,
        object_key: str,
        content_type: str,
    ):

        self.client.put_object(
            Bucket=self.bucket,
            Key=object_key,
            Body=file_bytes,
            ContentType=content_type,
        )

        return object_key