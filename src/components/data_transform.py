# in data transformation we just transform label encoding , one hot encoding and all the numerical dtaa and categorical data
# do data clean feature cleaning
import sys
import os
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    # responsible for convert categorical to numerical
    def get_data_transformer(self):
        try:
            df = pd.read_csv('notebook\data\complete_eda_csv.csv')
            X = df.drop(columns=['rate'], axis=1)
            Y = df['rate']
            categorical_cols = X.select_dtypes(include='object').columns
            numerical_cols = X.select_dtypes(exclude='object').columns

            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy="median")),
                    ('scaler', StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('onehotencoder', OneHotEncoder(sparse_output=False,
                     handle_unknown='ignore', categories='auto'))
                ]
            )
            logging.info("numerical columns are scaled now")
            logging.info("encoding is completed")

            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline', num_pipeline, numerical_cols),
                    ('cat_pipeline', cat_pipeline, categorical_cols)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data")
            logging.info("Obtain preprocessing object")

            preprocessing_obj = self.get_data_transformer()

            target_column_name = "rate"
            numerical_columns = ['votes', 'cuisines', 'costing']

            input_feature_train_df = train_df.drop(
                columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(
                columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("apply preprocess to trian and test")

            input_feature_train_array = preprocessing_obj.fit_transform(
                input_feature_train_df)
            input_feature_test_array = preprocessing_obj.transform(
                input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_array, np.array(target_feature_train_df)
            ]

            test_arr = np.c_[input_feature_test_array,
                             np.array(target_feature_test_df)]
            logging.info(f"Saved preprocessing object.")

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e, sys)
