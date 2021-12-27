#!/usr/bin/env python3.9

import os
import logging
import subprocess
import shutil
import tempfile

from datetime import datetime
from dynaconf import settings

from pycwpanel.api import CWPAccountApiRequest
from pycwpanel.utils import upload_file_to_s3


# Environment settings
AWS_S3_BUCKET = settings.AWS_S3_BUCKET

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_cwp_user_backup(username: str) -> None:
    """
    This function executes the CWP `user_backup` script at /scripts that
    handles archiving the user's home dir and databases which
    are written to a `backups` folder under the user's home directory

    :params
    username - str - the CWP account's username
    """

    try:
        logger.info(f"Running CWP backup script for user {username}")

        backup_cmd = f"/scripts/user_backup {username}"

        result = subprocess.run(
            backup_cmd, shell=True, check=True)

        assert result.returncode == 0

    except subprocess.CalledProcessError:
        logger.exception(
            f"CWP backup script failed for user {username}")


def run_backup(username: str) -> None:
    """
    This utility is made to compile a backup ZIP file for a
    CWP Panel user account.

    The main compoments of a CWP User account are:

    - User account's home directory e.g. /home/tings
    - User account's DNS configs at /var/named/mybusiness.com
    - User account's database(s) be it MySQL or PostgreSQL
    - TeeDeeBee...

    :params
    username - str - the CWP user account username

    This utility's end goal is to upload a ZIP file of the account's
    components to an S3 bucket.
    """

    #  CWP user account directories are placed under /home/
    cwp_backup_dir = os.path.join('/home/', username, 'backups')

    try:
        logger.info(f"Attempting archiving data for user {username}")

        # Run the CWP backup script
        run_cwp_user_backup(username)

        with tempfile.TemporaryDirectory() as tmp_dir:
            now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            #  Craft a meaningful archive name with the username,
            #  and the current timestamp separated by a colon e.g.
            #  macnate:24-12-2021-01-06-13
            archive_name = username + ':' + now

            #  Craft the absolute path to write the zip file
            full_archive_path = os.path.join(tmp_dir, archive_name)

            #  make zip archive, make_archive returns absolute path
            #  string of newly created zip file
            zip_file_path = shutil.make_archive(
                full_archive_path, 'zip', cwp_backup_dir)

            upload_file_to_s3(zip_file_path, AWS_S3_BUCKET)

        # Cleanup the files to optimize server disk space
        shutil.rmtree(cwp_backup_dir)

    except Exception:
        logger.exception(
            f"Failed to archive data for user {username}")


if __name__ == "__main__":
    """
    This script is intended to be executed as a UNIX Cronjob;
    recommended interval is everyday at midnight to the
    specified S3 bucket
    """

    try:
        cwp = CWPAccountApiRequest()
    except Exception:
        raise

    usernames = cwp.get_usernames()

    for username in usernames:
        run_backup(username)
