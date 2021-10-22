import argparse
import boto3
import os
import sys
import threading

S3_CLIENT = boto3.client("s3")

parser = argparse.ArgumentParser()

parser.add_argument(
    "-r", "--region", default=None, dest="aws_region", help="Sets AWS Region.", type=str
)

parser.add_argument(
    "-n",
    "--bucket-name",
    required=True,
    dest="bucket_name",
    help="Sets bucket name to use or create.",
    type=str,
)

parser.add_argument(
    "-o",
    "--origin-path",
    required=True,
    dest="origin_path",
    help="Sets folder source path to get files.",
    type=str,
)

parser.add_argument(
    "-d",
    "--destiny-path",
    required=True,
    dest="destiny_path",
    help="Sets s3 bucket folder path to upload files.",
    type=str,
)

args_command = parser.parse_args()

AWS_REGION = args_command.aws_region
BUCKET_NAME = args_command.bucket_name
BUCKET_FOLDER_PATH = args_command.destiny_path
SOURCE_FOLDER_PATH = args_command.origin_path

# TODO: INCLUDE -> files to upload
# TODO: EXCLUDE -> files to not upload
# TODO: OVERWRITE -> flag to overwrite files
# TODO: implement error hadling with botocore


class ProgressPercentage(object):
    """Progress percentage for s3 upload

    Args:
        object (string): file path and name
    """

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)"
                % (self._filename, self._seen_so_far, self._size, percentage)
            )
            sys.stdout.flush()


def check_or_create_s3_bucket():
    """Checks if s3 bucket exist, in otherwise will create it

    Raises:
        Exception: s3 bucket creation error handler
    """
    s3 = boto3.resource("s3")
    try:
        if s3.Bucket(BUCKET_NAME).creation_date is None:
            print("Bucket not exist.\nCreating the bucket...")
            if AWS_REGION is None:
                s3.create_bucket(
                    Bucket=BUCKET_NAME,
                )
            else:
                s3.create_bucket(
                    Bucket=BUCKET_NAME,
                    CreateBucketConfiguration={"LocationConstraint": AWS_REGION},
                )
    except Exception as e:
        # Attempt change bucket name or aws region or wait a fill minutes and try again.
        raise Exception("Error: ".format(e))


def check_source_folder_path():
    """Checks if source folder path exists

    Raises:
        ValueError: folder path do not exists
    """
    if not os.path.isdir(SOURCE_FOLDER_PATH):
        raise ValueError("SOURCE_FOLDER_PATH %r not found." % SOURCE_FOLDER_PATH)


def is_file_already_uploaded(filename: str, list_objects):
    """Checks if the file already uploaded in s3 bucket path

    Args:
        filename (str): name of file to be checked

    Returns:
        bool: true if already uploaded or false if not
    """
    key = BUCKET_FOLDER_PATH + filename
    if list_objects:
        try:
            for obj in list_objects["Contents"]:
                if key == obj["Key"]:
                    print("[Skipped] " + filename + " already exists.\n")
                    return True
        except KeyError:
            pass
    return False


def upload_to_s3():
    """Check if bucket s3 exists and upload all files"""

    check_source_folder_path()

    check_or_create_s3_bucket()

    list_files = os.listdir(SOURCE_FOLDER_PATH)
    count_files = len(list_files)

    list_objects = S3_CLIENT.list_objects_v2(
        Bucket=BUCKET_NAME, Prefix=BUCKET_FOLDER_PATH
    )

    print(
        "Uploading:\nFrom {}\nTo: s3://{}/{}\n\n".format(
            SOURCE_FOLDER_PATH, BUCKET_NAME, BUCKET_FOLDER_PATH
        )
    )

    for filename in list_files:

        index_file = list_files.index(filename) + 1

        print(
            "[{}/{}] {}".format(
                index_file,
                count_files,
                filename,
            )
        )
        if not is_file_already_uploaded(filename, list_objects):
            try:
                S3_CLIENT.upload_file(
                    SOURCE_FOLDER_PATH + filename,
                    BUCKET_NAME,
                    BUCKET_FOLDER_PATH + filename,
                    Callback=ProgressPercentage(SOURCE_FOLDER_PATH + filename),
                )
            except Exception as e:
                print(filename + ": Failled!\nError: {}".format(e))
            print("[Uploaded] Done!\n")


upload_to_s3()
