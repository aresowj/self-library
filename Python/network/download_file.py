import requests
import os
import logging


logger = logging.getLogger(__name__)


def _download_file(self, remote_path, local_path, chunk_size=1024):
    """Download a tool from path. By default, the file should be a zip,
    but not a directory.
    """
    stream = requests.get(remote_path, stream=True)
    original_size = int(stream.headers['Content-Length'])
    with open(local_path, 'wb') as f:
        for chunk in stream.iter_content(chunk_size=chunk_size):
            if chunk:   # filter out keep-alive new chunks
                f.write(chunk)

    downloaded_size = os.path.getsize(local_path)
    logger.info('Original: %d, downloaded: %d' % (original_size, downloaded_size))

    # check if the file is downloaded completely.
    return original_size == downloaded_size
