from flask import Flask,request,render_template
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData,PredictPipeline
application = Flask(__name__)
app = application

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata',methods=['GET','POST'])
def predict_data():
    if request.method == 'GET':
        return render_template('home.html')
    else :
        data = CustomData(
                online_order = request.form.get("online_order"),
                book_table  = request.form.get("Book_Table") ,
                votes = request.form.get("Votes"),
                location = request.form.get("location"),
                cuisines = request.form.get("cuisines"),
                costing =request.form.get("Approx_cost"),
                listed_in = request.form.get("listed_in")
            
        )