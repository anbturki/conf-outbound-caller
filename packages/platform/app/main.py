"""
Main module for the application
"""

from dotenv import load_dotenv

from app.core.bootstrap.confera_app import ConferaApp

load_dotenv()

app = ConferaApp()

# make the run for production and development
if __name__ == "__main__":
    app.run()
