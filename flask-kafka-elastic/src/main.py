from app import app
import os

# run the app.
_debug = bool(os.getenv('FLASK_DEBUG'))
if __name__ == "__main__" and _debug:
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = _debug
    app.run()
