import sys
import pandas as pd
from src.exception import CustomException
from src.utils import load_object

class PredictPipeline:
    def __init__(self):
        pass
    def predict(self,feature):
        try:
            model_path = "artifacts\model.pkl"
            preprocessor_path = "artifacts\preprocessor.pkl"
            model = load_object(file_path = model_path)
            preprocessor = load_object(file_path = preprocessor_path)
            
            data_scale = preprocessor.transform(feature)
            predict = model.predict(data_scale)
            return predict
        except Exception as e:
            raise CustomException(e,sys)

class CustomData:
    def __init__(self,
                 online_order: str,
                 book_table: str,
                 votes : int,
                 cuisines : int,
                 costing : int,
                 listed_in : str):
        
        self.online_order = online_order
        self.book_table = book_table
        self.votes = votes
        self.cuisines = cuisines
        self.costing  = costing
        self.listed_in = listed_in
       
    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "online_order":[self.online_order],
                "book_table" : [self.book_table],
                "votes":[self.votes],
                "cuisines" : [self.cuisines],
                "costing" : [self.costing],
                "listed_in" : [self.listed_in]
                
            }
            
            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise CustomException(e,sys) 
        