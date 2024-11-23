import boto3

from src.settings import S3_URL


class S3Client:
    def __init__(self, bucket_name):
        session = boto3.session.Session()
        self.client = session.client(
            service_name='s3',
            endpoint_url=S3_URL,
        )
        self.bucket_name = bucket_name

    async def upload(self, filename, key):
        self.client.upload_file(filename, self.bucket_name, key)

    async def download(self, key, filename):
        return self.client.download_file(self.bucket_name, key, filename)
