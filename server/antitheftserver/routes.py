import app, os
from flask import render_template 

PHOTO_FOLDER = ""

@app.route('/')
def index():
    # Get a list of all the photo files in the folder
    photo_files = [f for f in os.listdir(PHOTO_FOLDER) if os.path.isfile(os.path.join(PHOTO_FOLDER, f))]

    # Render the HTML template with the list of photo files
    return render_template('index.html', photo_files=photo_files) 