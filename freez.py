from flask_frozen import Freezer
from app.app import app

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()
