from functools import wraps
import json
from os import environ as env
from urllib.parse import urlencode

from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import Flask, render_template
from flask import session
from flask import url_for
from authlib.integrations.flask_client import OAuth

from app import constants  # from app import constants

ENV_FILE = find_dotenv(filename='app/.env')
if ENV_FILE:
    load_dotenv(ENV_FILE)
else:
    print("The .env file is missing!")

AUTH0_CALLBACK_URL = env.get(constants.AUTH0_CALLBACK_URL)
AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)

app = Flask(__name__)
app.secret_key = constants.SECRET_KEY
app.debug = True


@app.route('/home')
def dashboard2():
    return render_template("fhome.html")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=env.get('PORT', 8080), debug=True)
