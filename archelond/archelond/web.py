"""
Main entry point for flask application
"""
import logging
import os

from flask import Flask, jsonify, request
from passlib.apache import HtpasswdFile

from archelond.log import configure_logging
from archelond.auth import requires_auth, generate_token

log = logging.getLogger('archelond')

DUMMY_HISTORY = [
    {'command': 'cd'},
    {'command': 'blah'},
    {'command': 'echo hi'},
]

def run_server():
    """
    If started from command line, rebuild object in
    debug mode and run directly
    """
    host = os.environ.get('ARCHELOND_HOST', 'localhost')
    port = int(os.environ.get('ARCHELOND_PORT', '8580'))

    app.debug = True
    log.critical(
        'Running in debug mode. Do not run this way in production'
    )
    app.config['LOG_LEVEL'] = 'DEBUG'
    configure_logging(app)
    app.run(host=host, port=port)


def wsgi_app(debug=False):
    """
    Start flask application runtime
    """
    # Setup the app
    app = Flask('archelond')
    # Get configuration from default or via environment variable
    if os.environ.get('ARCHELOND_CONF'):
        app.config.from_envvar('ARCHELOND_CONF')
    else:
        app.config.from_object('archelond.config')

    # Load up user database
    app.config['users'] = HtpasswdFile(app.config['HTPASSWD_PATH'])

    # Set up logging
    configure_logging(app)
    
    return app


# Setup flask application
app = wsgi_app()


@app.route('/')
@requires_auth
def index(user):
    """
    Simple index view for documentation and navigation.
    """
    return 'Archelond Ready for Eating Shell History'


@app.route('/api/v1/token', methods=['GET'])
@requires_auth
def token(user):
    """
    Return the user token for API auth that is based off the
    flask secret and user password
    """
    return jsonify({'token': generate_token(user)})


@app.route('/api/v1/history', methods=['GET', 'POST'])
@requires_auth
def history(user):
    """
    POST=Add entry
    GET=Get entries with query
    """
    if request.method == 'GET':
        query = request.args.get('q')
        if query:
            results = [x for x in DUMMY_HISTORY if query in x['command']]
        else:
            results = DUMMY_HISTORY
        return jsonify({'commands': results})

    if request.method == 'POST':
        # Accept json or form type
        if request.json:
            data = request.json
        else:
            data = request.form
        if not data.get('command'):
            return jsonify({'error': 'Missing command parameter'}), 422

        DUMMY_HISTORY.append({'command': data['command']})
        return '', 201
    raise Exception