from backend import app


if __name__ == "__main__":  # guard to silence this warning.
    port = 8080
    app.run(port=port, debug=True, host="localhost")
