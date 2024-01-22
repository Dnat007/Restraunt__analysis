# data ingestion when we are reading the data from the database
import os
import sys
from src.exception import CustomException
import pandas as pd
from src.logger import logging
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from pymongo.mongo_client import MongoClient

from src.components.data_transform import DataTransformation
from src.components.data_transform import DataTransformationConfig

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer
# defining variable


@dataclass
# where i have save the raw input or test data or train data
class DataIngestionConfig:
    train_data: str = os.path.join('artifacts', 'train.csv')
    test_data: str = os.path.join('artifacts', 'test.csv')
    raw_data: str = os.path.join('artifacts', 'data.csv')


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    # read the data from the database

    def initiate_data_ingestion(self):
        logging.info("Enter the data ingestion mehtod")
        try:
            dataset = pd.read_csv("notebook\data\complete_eda_csv.csv")
            logging.info("Reading the dataset")

            os.makedirs(os.path.dirname(
                self.ingestion_config.train_data), exist_ok=True)

            dataset.to_csv(self.ingestion_config.raw_data,
                           index=False, header=True)

            logging.info("Train test split initiated")
            train_set, test_set = train_test_split(
                dataset, test_size=0.30, random_state=30)

            train_set.to_csv(self.ingestion_config.train_data,
                             index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data,
                            index=False, header=True)
            logging.info("Ingestion of the data is completed")

            return (
                self.ingestion_config.train_data,
                self.ingestion_config.test_data

            )

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(
        train_data, test_data)

    modeltrainer = ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr, test_arr))
