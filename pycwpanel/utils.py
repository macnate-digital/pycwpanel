import boto3
import datetime
import logging
import os

from botocore.exceptions import ClientError
from dynaconf import settings


logger = logging.getLogger(__name__)


def upload_file_to_s3(
        filename: str,
        bucket: str,
        object_name: str = None) -> None:
    """
    Uploads a supplied file to an S3 bucket

    :param filename: The file to upload
    :param bucket: The bucket to upload to

    The logic below places the uploaded ZIP file under two S3 keys/
    directories. It assumes that you may have more that one CWP Panel
    instance, so it'd be a good practice to place the ZIP files under
    a directory of the respective CWP hostname e.g.

    <s3-bucket>/cwp1.myhostingcompany.com/2022-01-01/cwp1useraccount.zip
    <s3-bucket>/cwp2.myhostingcompany.com/2022-01-01/cwp2useraccount.zip

    """
    if object_name is None:
        object_name = os.path.basename(filename)

    s3_client = boto3.client('s3')
    s3_key = settings.AWS_S3_KEY

    try:
        logger.info(f"Uploading {filename} to S3 bucket {bucket}")

        today_date = datetime.datetime.now()

        s3_subkey = f"{today_date.strftime('%Y-%m-%d')}"
        s3_key = s3_key + '/' + s3_subkey + f'/{object_name}'

        s3_client.upload_file(filename, bucket, s3_key)

        logger.info("Uploading successful!")
    except ClientError as ce:
        logger.exception(ce)
