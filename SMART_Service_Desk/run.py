from app import create_app, db, migrate

flask_app = create_app()

if __name__ == '__main__':
    flask_app.run(debug=True)