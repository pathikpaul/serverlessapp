import boto3,json
from botocore.errorfactory import ClientError
S3_BUCKET_NAME="pathik2020"
S3_OBJECT_NAME="notes_db.json"
S3_REGION_NAME="us-west-2"

def lambda_handler(event, context):
#    return {'statusCode': 200, 'body': event}
    list_of_notes=event.get("list_of_notes")
#    return {'statusCode': 200, 'body': list_of_notes}
    if not list_of_notes:
        return {'statusCode': 200, 'body': 'List of Notes not found'}
    s3 = boto3.client('s3',region_name=S3_REGION_NAME)
    try:
        s3.put_object(Bucket=S3_BUCKET_NAME, Key=S3_OBJECT_NAME, Body=json.dumps(list_of_notes))
    except ClientError:
        location = {'LocationConstraint': S3_REGION_NAME}
        bucket = s3.create_bucket(Bucket=S3_BUCKET_NAME,CreateBucketConfiguration=location)
        s3.put_object(Bucket=S3_BUCKET_NAME, Key=S3_OBJECT_NAME, Body=json.dumps(list_of_notes))
    return {'statusCode': 200, 'body': list_of_notes }
