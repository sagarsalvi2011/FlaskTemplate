#!/usr/bin/env python
from flask import Flask

from app import app as application
import app.module.views

if __name__ == '__main__':
    HOST = application.config['HOST']
    PORT = application.config['PORT']

    from werkzeug.serving import run_simple
    from werkzeug.wsgi import DispatcherMiddleware
    application.config['DEBUG'] = True
    # Load a dummy app at the root URL to give 404 errors.
    # Serve app at APPLICATION_ROOT for localhost development.
    application = DispatcherMiddleware(Flask('user_app'), {
       application.config['APPLICATION_ROOT']: application,
    })
    run_simple(HOST, PORT, application, use_reloader=True, threaded=True)
