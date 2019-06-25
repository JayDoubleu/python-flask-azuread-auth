import adal
import flask
import uuid
import requests
import config
from datetime import datetime
from datetime import timedelta

app = flask.Flask(__name__)
app.debug = True
app.secret_key = config.APP_SECRET

PORT = 5000  # A flask app by default runs on PORT 5000
AUTHORITY_URL = config.AUTHORITY_HOST_URL + '/' + config.TENANT
REDIRECT_URI = 'http://localhost:{}/authorize'.format(PORT)
AUTH_URL = ('https://login.microsoftonline.com/{}/oauth2/authorize?' +
            'response_type=code&client_id={}&redirect_uri={}&' +
            'state={}&resource={}')


@app.before_request
def is_authorized():
    if ('access_token' not in flask.session
            and flask.request.endpoint != 'login'
            and flask.request.endpoint != 'authorize'):
        return flask.redirect(flask.url_for('login'))


@app.route("/")
def main():
    return flask.render_template('index.html')


@app.route("/login")
def login():
    auth_state = str(uuid.uuid4())
    flask.session['state'] = auth_state
    authorization_url = AUTH_URL.format(config.TENANT, config.CLIENT_ID,
                                        REDIRECT_URI, auth_state,
                                        config.RESOURCE)
    resp = flask.Response(status=307)
    resp.headers['location'] = authorization_url
    return resp


@app.route("/authorize")
def authorize():
    code = flask.request.args['code']
    state = flask.request.args['state']
    if state != flask.session['state']:
        raise ValueError("State does not match")
    auth_context = adal.AuthenticationContext(AUTHORITY_URL)
    token_response = auth_context.acquire_token_with_authorization_code(
        code, REDIRECT_URI, config.RESOURCE, config.CLIENT_ID,
        config.CLIENT_SECRET)
    if 'accessToken' in token_response:
        flask.session['access_token'] = str(uuid.uuid4())

    return flask.redirect('/')


if __name__ == "__main__":
    app.run()
