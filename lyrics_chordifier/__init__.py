import os

from dotenv import load_dotenv
from flask import Flask

from .api import blueprint as api_blueprint
from .views import blueprint as views_blueprint

load_dotenv()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev"),
        BUCKET_ENDPOINT_URL=os.getenv("BUCKET_ENDPOINT_URL"),
        BUCKET_ACCESS_KEY_ID=os.getenv("BUCKET_ACCESS_KEY_ID"),
        BUCKET_SECRET_ACCESS_KEY=os.getenv("BUCKET_SECRET_ACCESS_KEY"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.register_blueprint(api_blueprint)
    app.register_blueprint(views_blueprint)

    return app
