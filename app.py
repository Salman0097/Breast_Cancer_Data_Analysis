import pickle
from flask import Flask, request, app, jsonify, url_for, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)
svm_model_pkl = pickle.load(open('classifiers.pkl','rb'))
piping=pickle.load(open('piping.pkl','rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api', methods=['POST'])

def predict_api():
    data = request.json['data']
    print(data)
    print(np.array(list(data.values())).reshape(1,-1))
    new_data=piping.transform(np.array(list(data.values())).reshape(1,-1))
    output=svm_model_pkl.predict(new_data)
    print(output[0])
    return jsonify(output[0])

@app.route('/predict',methods=['POST'])
def predict():
    data=[float(x) for x in request.form.values()]
    final_input=piping.transform(np.array(data).reshape(1,-1))
    print(final_input)
    output=svm_model_pkl.predict(final_input)[0]
    op_txt =''
    if output == 1:       
        op_txt.append('Sorry.You have Breast cancer')
    else:
        op_txt.append('Hurray!You are awesome and good to go')
    
    return render_template("home.html",prediction_text= op_txt )


if __name__=="__main__":
    app.run(debug=True)
