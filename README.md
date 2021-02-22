# AutoRack Backend


### Getting Started
1. Clone the repository using the `git clone <repository url>`
2. In the root folder of the application create a virtual environment 
   via the following: `python3 -m venv <virtualenv_name>`
3. Activate the virtual environment: `source  <virtualenv_name>/bin/activate`
4. Install dependencies from requirements.txt: `pip install -r requirements.txt`
   
### Running the App
1. Set the FLASK_APP variable to run.py which is our Flask entry point:
    ```bash
    export FLASK_APP=run.py 
    export FLASK_ENV=development
    ```
2. Run the app: `flask run`

### Basic File Structure
```
.
├── app
│   ├── auth
│   ├── controllers
│   ├── models
│   ├── routes
│   └── __init__.py
├── .env
├── requirements.txt
└── run.py
```
- **auth** - configures the authentication (Firebase) we will be using for the app
- **controllers** - files that contain all logic such as grabbing/storing data in database
- **models** - should consist of classes that create the objects stored in the database
- **routes** - all the routes we need to server

# IMPORTANT NOTES 

- ALWAYS DO WORK IN THE VIRTUAL ENVIRONMENT
- When installing packages make sure that requirements.txt is updated using:
   ```
   pip freeze > requirements.txt
   ```
