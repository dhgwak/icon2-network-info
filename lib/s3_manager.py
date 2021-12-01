import boto3
import time


class S3Manager:

    def __init__(self, aws_access_key_id, aws_secret_access_key):
        # account info ( be args )
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_default_region = 'ap-northeast-2'
        # sts session
        self.s3_client = self.aws_client('s3')
        # CF client
        self.cf_client = self.aws_client('cloudfront')

    def aws_client(self, service):
        client = boto3.client(service,
                              aws_access_key_id=self.aws_access_key_id,
                              aws_secret_access_key=self.aws_secret_access_key,
                              region_name=self.aws_default_region
                              )
        return client

    def buckets(self, ):
        dict_buckets = self.s3_client.list_buckets()
        buckets = dict_buckets['Buckets']
        return [bucket['Name'] for bucket in buckets]

    def bucket_contents(self, bucket_name):
        if self.s3_client.list_objects_v2(Bucket=bucket_name).get('Contents'):
            return [content for content in self.s3_client.list_objects_v2(Bucket=bucket_name)['Contents']]
        return []

    def content_list(self, bucket_name, prefix='icon2'):
        if self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix).get('Contents'):
            return [content['Key'] for content in self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)['Contents']]
        return []

    def upload(self, bucket, key, file_name, extra_args=None):
        if extra_args is None:
            self.s3_client.upload_file(file_name, bucket, key)
        else:
            self.s3_client.upload_file(file_name, bucket, key, ExtraArgs=extra_args)

    def cf_re_caching(self, dist_id):
        self.cf_client.create_invalidation(
            DistributionId=dist_id,
            InvalidationBatch={
                'Paths': {
                    'Quantity': 1,
                    'Items': [
                        '/*',
                    ]
                },
                'CallerReference': str(time.time()).replace('.', '')
            }
        )

    def download(self, bucket, key, file_name):
        self.s3_client.download_file(bucket, key, file_name)

    def delete(self, bucket, key):
        self.s3_client.delete_object(Bucket=bucket, Key=key)