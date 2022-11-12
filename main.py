from imikino import app, database

if __name__ == '__main__':
    with app.app_context():
        #database.drop_all()
        #database.create_all()
        app.run(debug=True)
