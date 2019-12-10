import boto3

S3 = boto3.client('s3')

SOURCE_FILENAME = 'selfie.jpg'
BUCKET_NAME = 'facialrecnewfacebucket'

S3.upload_file(SOURCE_FILENAME, BUCKET_NAME, SOURCE_FILENAME)
