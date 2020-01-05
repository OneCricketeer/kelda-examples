from app import app
import os


# run the app.
if __name__ == "__main__" and bool(os.getenv('FLASK_DEBUG')):
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()
