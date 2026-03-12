import pandas as pd
from pandas import DataFrame
from .const import FILE_PATH
from loguru import logger

class FileHandler():
    def __init__(self):
        self.file_loaded = False
        
    def load_file(self, file_name: str) -> DataFrame:
        path = FILE_PATH / file_name
        logger.debug(f"file path: {path}")
        dataframe = pd.read_csv(path)
        if not dataframe.empty:
            logger.info(f"loaded file: {file_name}")
            self.file_loaded = True
            logger.debug(dataframe)
            return dataframe
        else:
            logger.warning(f"File: {file_name} is invalid")
            raise FileNotFoundError
        
    def save_file(self, dataframe: DataFrame, file_name: str):
        path = FILE_PATH / file_name
        logger.debug(f"saving data to file: {file_name}")
        dataframe.to_csv(path, sep='\t', encoding='utf-8')
        logger.debug(f"file path: {path}")