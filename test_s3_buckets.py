import os
import tempfile
import unittest
import boto3
import botocore
from moto import mock_s3
from mock import download_json_files, MY_BUCKET, MY_PREFIX


@mock_s3
class TestDownloadJsonFiles(unittest.TestCase):
    # function to setup the testing environment
    def setUp(self):
        client = boto3.client(
            "s3",
            region_name="eu-west-1",
            aws_access_key_id = os.environ.get('ACCESS_KEY'),
            aws_secret_access_key = os.environ.get('SECRET_KEY'),
            )
        try:
            s3 = boto3.resource(
                "s3",
                region_name="eu-west-1",
                aws_access_key_id=os.environ.get('ACCESS_KEY'),
                aws_secret_access_key = os.environ.get('SECRET_KEY'),
                )
            s3.meta.client.head_bucket(Bucket=MY_BUCKET)
        except botocore.exceptions.ClientError:
            pass
        else:
            err = f'{bucket} should not exist.'
            raise EnvironmentError(err)
        client.create_bucket(Bucket=MY_BUCKET)
        current_dir = os.path.dirname(__file__)
        fixtures_dir = os.path.join(current_dir, "fixtures")
        _upload_fixtures(MY_BUCKET, fixtures_dir)

# function to restore the test environment to original state before tests were done, cleanup
    def tearDown(self):
        s3 = boto3.resource(
            "s3",
            region_name="eu-west-1",
            aws_access_key_id=os.environ.get('ACCESS_KEY'),
            aws_secret_access_key = os.environ.get('SECRET_KEY'),
            )
        bucket = s3.Bucket(MY_BUCKET)
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()

def _upload_fixtures(bucket, fixtures_dir):
    client = boto3.client("s3")
    fixtures_paths = [os.path.join(path,  filename) for path, _, files in os.walk(fixtures_dir) for filename in files ]
    for path in fixtures_paths:
        key = os.path.relpath(path, fixtures_dir)
        client.upload_file(Filename=path, Bucket=bucket, Key=key)

    def test_download_json_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            download_json_files(MY_BUCKET, MY_PREFIX, tmpdir)
            mock_folder_local_path = os.path.join(tmpdir, MY_PREFIX)
            self.assertTrue(os.path.isdir(mock_folder_local_path))
            result = os.listdir(mock_folder_local_path)
            desired_result = ["foo.json", "bar.json"]
            self.assertCountEqual(result, desired_result)
