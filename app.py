# Import all the necessary modules and packages
from website import create_app


# Initialize the function create_app
if __name__ == "__main__":
    app = create_app()
    app.run(debug = False)

     