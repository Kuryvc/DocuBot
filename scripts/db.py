import boto3
import os

def dynamo_connection():
    dynamodb = boto3.client(
        "dynamodb",
        region_name="us-east-1",
        aws_access_key_id= "AKIAZ7XICEOYVZP5MCWF",
        aws_secret_access_key= "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",
    )

    return dynamodb

class dynamoConnectionSingleton:
    connection = None
    
    @classmethod
    def getConnection(cls):
        if cls.connection is None:
            cls.connection = dynamo_connection()
        return cls.connection
    