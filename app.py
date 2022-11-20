from flask import Flask, request, jsonify, make_response
from flask_restplus import Api, Resource, fields

import os
import sys

model_path = os.path.dirname(os.path.dirname(os.getcwd()))
print(model_path)
sys.path.append(model_path)

from evaluation.segmentor import Segmentor
# import joblib

methods = [
    'fmm', 'bmm', 'bimm', 'mmseg', 'hmm', 'jieba', 'thulac', 'ltp', 'hanlp'
]
segmentor = Segmentor(methods, corpus='msr')

flask_app = Flask(__name__)
app = Api(app=flask_app,
          version="1.0",
          title="Chinese Word Segmentation",
          description="Predict results using a trained model")

name_space = app.namespace('prediction', description='Prediction APIs')

model = app.model(
    'Prediction params', {
        'InputSentence':
        fields.String(required=True,
                      description="Input Sentence",
                      help="Input Sentence cannot be blank"),
        'Model':
        fields.Integer(required=True,
                       description="Select Model",
                       help="Model cannot be blank"),
    })


@name_space.route("/")
class MainClass(Resource):

    def options(self):
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

    @app.expect(model)
    def post(self):
        try:
            formData = request.json
            data = [val for val in formData.values()]
            method = data[1]
            sent = data[0]
            res = ""
            if method == 'all':
                for method in methods:
                    seg = "/".join(getattr(segmentor, method)(sent))
                    res += "{:<10}{}\n".format(method + ":", seg)
            else:
                seg = "/".join(getattr(segmentor, method)(sent))
                res += "{:<15}{}\n".format(method + ":", seg)
            response = jsonify({
                "statusCode": 200,
                "status": "Prediction made",
                "result": "Result:\n" + res
            })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        except Exception as error:
            return jsonify({
                "statusCode": 500,
                "status": "Could not make prediction",
                "error": str(error)
            })
