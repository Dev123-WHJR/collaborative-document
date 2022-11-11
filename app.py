import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'ACf9d1ededfeb00f9a7b82f40f232e75de'
    TWILIO_SYNC_SERVICE_SID = 'ISb0ca690820526dd6a515782210d4bc23'
    TWILIO_API_KEY = 'SK6695c1b0aed731c2492dbcc33a1c85ef'
    TWILIO_API_SECRET = 'ntbBunjWVQnuNeQaQPMkBMsTd8prU7vz'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
    text_from_notepad = request.form['text']
    with open('workfile.txt','w') as f:
        f.write(text_from_notepad)

    path_to_store_text = "workfile.txt"

    return send_file(path_to_store_text, as_attachment=True)
    
        

    

    


if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
