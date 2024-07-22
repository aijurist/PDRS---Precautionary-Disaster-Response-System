from flask import Flask
from flask_cors import CORS
from model import model
from twitter import twitter_blueprint
from population_location import validation
app = Flask(__name__)
CORS(app)

# Register blueprint
app.register_blueprint(model, url_prefix='/api_model')
app.register_blueprint(twitter_blueprint, url_prefix='/api_twitter')
app.register_blueprint(validation, url_prefix='/api_validation')

# Run the application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
