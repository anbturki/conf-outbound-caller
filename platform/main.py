"""
Main module for the application
"""

from core.bootstrap.confera_app import ConferaApp
from dotenv import load_dotenv

load_dotenv()

app = ConferaApp()

# make the run for production and development
if __name__ == "__main__":
    app.run()
