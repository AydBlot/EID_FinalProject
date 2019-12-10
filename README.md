###Facial Recognition Security System
Developers: Ayden Blotnick and Ajitesh Batra

###Notes and Installation Instructions
1. Use this tutorial in order to install openCV on a rpi: https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/

2. Install AWS Command Line Interface (CLI) via pip3 install awscli --upgrade --user. Then check the version with the command "aws --version".  Lastly, run the command "aws configure" to properly set up the access key and region.

3. Must create s3 buckets "facialrecnewfacebucket" and "facialrecknownfacebucket" as well as add a trigger in the lambda function to be called once something is uploaded to the "facialrecnewbucket".

4. Install espeak from the command line with pip3 install speake3. 

5. Install the AWS python sdk library with pip3 install boto3

6. For SpeechRecognition python library:
pip3 install SpeechRecognition
pip3 install pyaudio
