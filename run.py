"""
Time Series AI Forecasting Platform - Main Application Entry Point
"""

import os
import sys

# ADD BACKEND FOLDER TO PYTHON PATH

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

BACKEND_DIR = os.path.join(
    BASE_DIR,
    "backend"
)

sys.path.append(
    BACKEND_DIR
)

# IMPORT FLASK APP

from app import create_app

from app.config.settings import (
    DevelopmentConfig,
    ProductionConfig
)

# CREATE APPLICATION

def run():

    env = os.environ.get(
        "FLASK_ENV",
        "development"
    )

    if env == "production":

        app = create_app(
            ProductionConfig
        )

    else:

        app = create_app(
            DevelopmentConfig
        )

    port = int(
        os.environ.get(
            "FLASK_PORT",
            5000
        )
    )

    app.run(

        host="0.0.0.0",

        port=port,

        debug=True
    )

# MAIN ENTRY

if __name__ == "__main__":

    run()