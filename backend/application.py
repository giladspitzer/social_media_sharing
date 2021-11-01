from flask import Flask
from backend import app

if __name__ == "__main__":
    port = 5000
    app.run(port=port, debug=True, host="localhost")
