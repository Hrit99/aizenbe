import boto3
from botocore.exceptions import NoCredentialsError
import os

def upload_file_to_s3(file, bucket_name, object_name=None):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=os.environ.get('AWS_REGION')
    )
    try:
        s3_client.upload_fileobj(file, bucket_name, object_name or file.filename)
        return f'https://{bucket_name}.s3.{os.environ.get("AWS_REGION")}.amazonaws.com/{object_name or file.filename}'
    except NoCredentialsError:
        return None
