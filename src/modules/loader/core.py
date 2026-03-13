import pandas as pd
from pandas import DataFrame
from pathlib import Path
from .const import FILE_PATH
from loguru import logger
import os

class FileHandler():
    def __init__(self):
        self.file_loaded = False
        
    def load_file(self, file_name: str) -> DataFrame:
        if file_name.endswith(".csv"):
            path = FILE_PATH / file_name
            logger.debug(f"file path: {path}")
            dataframe = pd.read_csv(path, sep=";")
            if not dataframe.empty:
                logger.info(f"loaded file: {file_name}")
                self.file_loaded = True
                logger.debug(dataframe)
                return dataframe
            else:
                logger.warning(f"File: {file_name} is invalid")
                raise FileNotFoundError
        else:
            raise ValueError("Invalid file format")
        
    def save_file(self, dataframe: DataFrame, file_name: str):
        if file_name.endswith(".csv"):
            path = FILE_PATH / file_name
            logger.debug(f"saving data to file: {file_name}")
            dataframe.to_csv(path, sep=';', encoding='utf-8')
            logger.debug(f"file path: {path}")
        elif file_name.endswith(".xlsx"):
            path = FILE_PATH / file_name
            logger.debug(f"saving data to file: {file_name}")
            dataframe.to_excel(path)
            logger.debug(f"file path: {path}")
        else:
            raise ValueError("Invalid file format")
    
    def check_if_file_exists(self, file_name: str) -> bool:
        path: Path = FILE_PATH / file_name
        if path.is_file():
            logger.warning("file already exists")
            return True
        else:
            return False
        
    def launch_excel(self, file_name: str):
        os.system(f"start EXCEL.EXE {str(FILE_PATH / file_name)}")