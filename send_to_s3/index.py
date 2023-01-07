
from flask import Flask, render_template, request
import boto3
import tempfile
import time
import os

app = Flask(__name__)
from werkzeug.utils import secure_filename

s3 = boto3.client('s3',
                    aws_access_key_id=os.environ['S3_ACCESS_KEY'],
                    aws_secret_access_key=os.environ['S3_SECRET_KEY'],
                    endpoint_url=os.environ['S3_END_POINT']
                     )

BUCKET_NAME='speedtestingbucketonlydeletit'

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
                # Save the file to a temporary location
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = os.path.join(temp_dir, filename)
                    img.save(temp_path)
                    # Open the file in binary mode
                    with open(temp_path, 'rb') as file:
                        # Use the upload_fileobj method to safely upload the file
                        s3.upload_fileobj(
                            Fileobj=file,
                            Bucket=BUCKET_NAME,
                            Key=filename
                        )
                
                # Stop the timer and calculate the elapsed time
                end_time = time.time()
                elapsed_time = end_time - start_time
                
                # Display the elapsed time
                print("Elapsed time:", elapsed_time)
                
                msg = "Upload Done ! Elapsed time: "elapsed_time

    return render_template("file_upload_to_s3.html",msg =msg)



if __name__ == "__main__":app.run(debug=True)
