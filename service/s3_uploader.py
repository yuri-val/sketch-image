import os
import boto3
from botocore.exceptions import ClientError

class S3Uploader:
    """A class to handle uploading files to Amazon S3."""

    def __init__(self):
        """
        Initialize the S3Uploader.

        """
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION_NAME'),
        )
        self.bucket_name = os.environ.get('S3_BUCKET_NAME')

    def upload(self, local_file_path, s3_directory_path, file_name):
        """
        Upload a file to S3, creating the directory path if it doesn't exist.

        Args:
            local_file_path (str): Path to the local file to upload.
            s3_directory_path (str): Path to the directory in S3 where the file should be uploaded.
            file_name (str): Name to give the file in S3.

        Returns:
            str: The public URL of the uploaded file in S3.

        Raises:
            FileNotFoundError: If the local file does not exist.
            Exception: If there's an error during the upload process.
        """
        if not os.path.exists(local_file_path):
            raise FileNotFoundError(f"The file {local_file_path} does not exist.")

        try:
            # Construct the full S3 key (path + filename)
            s3_key = os.path.join(s3_directory_path.strip('/'), file_name)

            # Upload the file
            self.s3_client.upload_file(local_file_path, self.bucket_name, s3_key)

            # Generate the public URL
            public_url = f"https://{self.bucket_name}.s3.amazonaws.com/{s3_key}"
            return public_url

        except ClientError as e:
            raise Exception(f"An error occurred while uploading the file: {str(e)}")

    def _ensure_directory_exists(self, directory_path):
        """
        Ensure that a directory exists in S3.

        Note: S3 doesn't actually have directories, but we can simulate them with prefixes.
        This method is a no-op for S3 but is included for consistency with the MegaUploader interface.

        Args:
            directory_path (str): The path of the directory in S3.
        """
        pass  # No action needed for S3