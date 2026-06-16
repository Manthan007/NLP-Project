import os
from pathlib import Path
import requests
import zipfile
from textSummarizer.entity.config_entity import DataIngestionConfig
from textSummarizer.logging import logger
from textSummarizer.utils.common import get_size

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_data(self):
        if not os.path.exists(self.config.local_data_file):
            try:
                # Using requests instead of urllib
                response = requests.get(self.config.source_URL, stream=True)
                response.raise_for_status()  # Check for HTTP errors
                
                with open(self.config.local_data_file, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                logger.info(f"File downloaded successfully to {self.config.local_data_file}")
                
            except requests.exceptions.SSLError as e:
                logger.error(f"SSL Error occurred: {e}")
                # If you are behind a corporate proxy, try setting verify=False (use with caution)
                # or provide the path to your CA bundle: verify='/path/to/cert.pem'
                raise
            except Exception as e:
                logger.error(f"Error during download: {e}")
                raise
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")


    def extract_zip_file(self):
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)