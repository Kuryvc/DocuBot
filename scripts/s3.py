import boto3
import os
from dotenv import load_dotenv

def s3_connection():
    load_dotenv()
    
    s3 = boto3.resource(
        service_name="s3",
        region_name="us-east-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    return s3

class s3ConnectionSingleton:
    connection = None
    
    @classmethod
    def getConnection(cls):
        if cls.connection is None:
            cls.connection = s3_connection()
        return cls.connection
    