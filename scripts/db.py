import boto3
import os
from dotenv import load_dotenv

def dynamo_connection():
    load_dotenv()
    dynamodb = boto3.client(
        "dynamodb",
        region_name="us-east-1",
        aws_access_key_id= os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key= os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    return dynamodb

class dynamoConnectionSingleton:
    connection = None
    
    @classmethod
    def getConnection(cls):
        if cls.connection is None:
            cls.connection = dynamo_connection()
        return cls.connection
    