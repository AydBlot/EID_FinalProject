Use this tutorial in order to install openCV on a rpi: https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/

install AWS Command Line Interface (CLI) via pip3 install awscli --upgrade --user. Then check the version with the command "aws --version".  Lastly, run the command "aws configure" to properly set up the access key and region.

Must create s3 buckets "facialrecnewfacebucket" and "facialrecknownfacebucket" as well as add a trigger in the lambda function to be called once something is uploaded to the "facialrecnewbucket".
