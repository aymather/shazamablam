from flask import Flask
from flask_cors import CORS
from etc.DbClient import DbClient
from etc.CustomJSONEncoder import CustomJSONEncoder
import os

# Init db client
db = DbClient()

# Init app
app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

# Application config
app.secret_key = 'FLASK_SECRET_KEY'

# Route imports
import routes.test

# Open cors
CORS(app)

if __name__ == '__main__':

    # Get environment
    debug = False if os.environ.get('ENV') == 'production' else True

    # Run app
    app.run(debug=debug)