from app.init import init_app

app = init_app()

if __name__ == "__main__":
    app.run("0.0.0.0", 5001, debug=True)
