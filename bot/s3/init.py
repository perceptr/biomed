import boto3

class S3Client:
    def __init__(self, bucket_name):
        session = boto3.session.Session()
        self.client = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net'
        )
        self.bucket_name = bucket_name

    def upload(self, filename, key):
        self.client.upload_file(filename, self.bucket_name, key)

    def download(self, key, filename):
        return self.client.download_file(self.bucket_name, key, filename)
