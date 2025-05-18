"""
Main module for the application
"""

from app.core.bootstrap.confera_app import ConferaApp

app = ConferaApp()

# make the run for production and development
if __name__ == "__main__":
    app.run()
