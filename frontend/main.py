from functools import wraps
import json
from os import environ as env
from urllib.parse import urlencode

from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.integrations.flask_client import OAuth

from frontend.app import constants #from app import constants

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


@app.errorhandler(Exception)
def handle_auth_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    print(response)
    return response


oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url=AUTH0_BASE_URL + '/oauth/token',
    authorize_url=AUTH0_BASE_URL + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if constants.PROFILE_KEY not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated


# Controllers API
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/callback')
def callback_handling():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    session[constants.JWT_PAYLOAD] = userinfo
    session[constants.PROFILE_KEY] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/dashboard')


@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)


@app.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': url_for('home', _external=True), 'client_id': AUTH0_CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


@app.route('/dashboard')
@requires_auth
def dashboard():
    print(session[constants.JWT_PAYLOAD])
    return render_template('dashboard.html',
                           userinfo=session[constants.PROFILE_KEY],
                           userinfo_pretty=json.dumps(session[constants.JWT_PAYLOAD], indent=4))


@app.route('/dashboard2')
def dashboard2():
    data = {
        1: {
            "link": "google.com",
            "text": "Link to Google"
        },
        2: {
            "link": "bing.com",
            "text": "Link to Bing"
        }
    }
    return render_template("homepage.html", data=data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=env.get('PORT', 8080), debug=True)

# #--------------------------------------------------------------------------------------------IMPORTS
# from fastapi import FastAPI, Request
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import HTMLResponse, RedirectResponse
#
# #--------------------------------------------------------------------------------------------DEPENDENCIES
# app = FastAPI()
# templates = Jinja2Templates(directory="../templates")
# app.mount("/static", StaticFiles(directory="../static"), name="static")
# #--------------------------------------------------------------------------------------------ROUTES
#
# @app.get("/", response_class=HTMLResponse)
# async def home(request: Request):
#     data = {
#         1: {
#             "link": "google.com",
#             "text": "Link to Google"
#         },
#         2: {
#             "link": "bing.com",
#             "text": "Link to Bing"
#         }
#     }
#     return templates.TemplateResponse("homepage.html", {"request": request, "data": data})
#
# @app.get("/login", response_class=HTMLResponse)
# async def login(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})
#
#