from application import app
from application.models import initialize_database

with app.app_context():
    initialize_database()

if __name__ == "__main__":
    app.run()