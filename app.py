import os
import pandas as pd
from flask import Flask, flash, request, redirect, url_for, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Users/ritika/Desktop/SIN/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

####################################################################
products_prob = pd.read_csv("products_prob.csv")

def recommend(prod, n):
    #Now lets select a hypothetical basket of goods (one or more products) that a customer has already purchased or
    #shown an interest for by clicking on an add or something, and then suggest him relative ones
    #basket = ['HOME BUILDING BLOCK WORD']
    basket=prod
    #Also select the number of relevant items to suggest
    no_of_suggestions = n
    all_of_basket = products_prob[basket]
    all_of_basket = all_of_basket.sort_values( ascending=False)
    suggestions_to_customer = list(all_of_basket.index[:no_of_suggestions])
    #print(products_prob)
    #print(all_of_basket)
    print('You may also consider buying:', suggestions_to_customer)
    output=[]
    for i in suggestions_to_customer:
        output.append(products_prob.loc[i,'Unnamed: 0'])
    return (output)
####################################################################

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/index', methods=['GET', 'POST'])
def home():
    return render_template("./index.html")

@app.route('/index/<product>', methods=['GET', 'POST'])
def predict(product):
    l=recommend(product, 3)
    return render_template("./index.html", ob1=l[0], ob2=l[1], ob3=l[2])

@app.route('/about')
@app.route('/index/about')
def about():
    return render_template("./about.html")


if __name__=='__main__':
    app.run(debug=True)