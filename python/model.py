from flask import Blueprint, request, jsonify
import ktrain
import os
import numpy as np
import json
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import PromptTemplate

from report_model import chain

os.environ['TF_USE_LEGACY_KERAS'] = 'True'

# Load the trained model for prediction
predictor_file_path = 'd://HACKFEST/twitter_disaster_predictor'
predictor = ktrain.load_predictor(predictor_file_path)

model = Blueprint('model', __name__)

def make_serializable(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.float32):
        return float(obj)
    if isinstance(obj, np.float64):
        return float(obj)
    return obj

@model.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        twitter_data = data.get('twitter_data')
        hashtags_data = data.get('hashtags_data')
        mentions_data = data.get('mentions_data')

        if not twitter_data or not isinstance(twitter_data, list):
            return jsonify({'error': 'Invalid input data'}), 400

        # Make predictions
        response = {}
        for i, tweet in enumerate(twitter_data):
            prediction = predictor.predict(tweet)
            confidence = predictor.predict_proba(tweet)
            response[i + 1] = {
                'text': tweet,
                'prediction': make_serializable(prediction),
                'confidence': make_serializable(confidence)
            }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@model.route('/get_report', methods=['POST'])
def get_report():
    data = request.json
    tweet = data.get('tweet')
    population = data.get('population')
    
    if not tweet or not population:
        return jsonify({'error': 'Both tweet and population data are required'}), 400
    
    try:
        output = chain.invoke({
            "tweet": tweet,
            "population": json.dumps(population)
        })
    except Exception as e:
        return jsonify({'error': f'Error invoking model: {str(e)}'}), 500
    
    try:
        return jsonify(output), 200
    except json.JSONDecodeError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'An error has occured': str(e)}), 500