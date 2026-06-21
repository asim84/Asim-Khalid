import logging
import os

import dropbox
from dropbox.exceptions import ApiError, AuthError

logger = logging.getLogger(__name__)


class DropboxConnector:
    def __init__(self):
        self.access_token = os.getenv("DROPBOX_ACCESS_TOKEN")
        self.folder = os.getenv("DROPBOX_LINNWORKS_FOLDER", "/Linnworks/exports")
        if not self.access_token:
            raise ValueError("DROPBOX_ACCESS_TOKEN not set")
        self.dbx = dropbox.Dropbox(self.access_token)

    def list_new_files(self, already_processed: list[str]) -> list[dict]:
        """List CSV files in the Linnworks folder that haven't been processed yet."""
        try:
            result = self.dbx.files_list_folder(self.folder)
            files = []
            while True:
                for entry in result.entries:
                    if isinstance(entry, dropbox.files.FileMetadata):
                        if entry.name not in already_processed and entry.name.endswith(".csv"):
                            files.append(
                                {
                                    "name": entry.name,
                                    "path": entry.path_lower,
                                    "modified": entry.server_modified,
                                }
                            )
                if not result.has_more:
                    break
                result = self.dbx.files_list_folder_continue(result.cursor)
            logger.info(f"Found {len(files)} new files in Dropbox folder")
            return files
        except AuthError as e:
            logger.error(f"Dropbox authentication error: {e}")
            raise
        except ApiError as e:
            logger.error(f"Dropbox API error listing files: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error listing Dropbox files: {e}")
            raise

    def download_file(self, path: str) -> bytes:
        """Download a file from Dropbox and return its content as bytes."""
        try:
            _, response = self.dbx.files_download(path)
            content = response.content
            logger.info(f"Downloaded {path} ({len(content)} bytes)")
            return content
        except ApiError as e:
            logger.error(f"Failed to download {path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error downloading {path}: {e}")
            raise
