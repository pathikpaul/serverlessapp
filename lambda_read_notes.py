import boto3,json
from botocore.errorfactory import ClientError

S3_BUCKET_NAME="pathik2020"
S3_OBJECT_NAME="notes_db.json"
S3_REGION_NAME="us-west-2"

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    try:
        obj = s3.get_object(Bucket=S3_BUCKET_NAME, Key=S3_OBJECT_NAME)
        j = json.loads(obj['Body'].read())
    except ClientError:
        j=[{"topic": "T1", "comment": "comment one"}, {"topic": "T2", "comment": "comment two"}, {"topic": "T3", "comment": "comment three"}, {"topic": "T4 ", "comment": "comment four"}]
    return {'statusCode': 200, 'body': j}
