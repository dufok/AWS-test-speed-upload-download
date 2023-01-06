
from flask import Flask, render_template, request
import boto3
import time
import os

app = Flask(__name__)
from werkzeug.utils import secure_filename

s3 = boto3.client('s3',
                    aws_access_key_id=os.environ['S3_ACCESS_KEY'],
                    aws_secret_access_key=os.environ['S3_SECRET_KEY'],
                   # aws_session_token=keys.AWS_SESSION_TOKEN
                     )

BUCKET_NAME='speed_testing_bucket_only_delet_it'

@app.route('/')  
def home():
    return render_template("file_upload_to_s3.html")

@app.route('/upload',methods=['post'])
def upload():
    if request.method == 'POST':
        img = request.files['file']
        if img:
                # Start the timer
                start_time = time.time()
            
                # Perform the file upload
                filename = secure_filename(img.filename)
                img.save(filename)
                s3.upload_file(
                    Bucket = BUCKET_NAME,
                    Filename=filename,
                    Key = filename
                )
                
                # Stop the timer and calculate the elapsed time
                end_time = time.time()
                elapsed_time = end_time - start_time
                
                # Display the elapsed time
                print("Elapsed time:", elapsed_time)
                
                msg = "Upload Done ! Elapsed time:", elapsed_time

    return render_template("file_upload_to_s3.html",msg =msg)


if __name__ == "__main__":
    
    app.run(debug=True)


