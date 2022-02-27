from src.app import app
from waitress import serve


if __name__ == "__main__":
    print("The application is now running on port 5000")
    serve(
        app,
        host='0.0.0.0',
        port=5000,
        threads=2
    )