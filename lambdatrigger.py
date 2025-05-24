import boto3

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    for record in event['Records']:
        source_bucket = 'sourcebucket123456'
        key = record['s3']['object']['key']

        # Determine destination bucket based on file extension
        if key.endswith('.png'):
            destination_bucket = 'pngfile123456'
        elif key.endswith('.txt'):
            destination_bucket = 'textfile123456'
        elif key.endswith('.pdf'):
            destination_bucket = 'pdffile123456'
        else:
            print(f"Unsupported file type: {key}")
            return
        
        # Copy the file to the destination bucket
        copy_source = {'Bucket': source_bucket, 'Key': key}
        s3_client.copy_object(CopySource=copy_source, Bucket=destination_bucket, Key=key)
        
        # Delete the original file from source bucket
        s3_client.delete_object(Bucket=source_bucket, Key=key)
        
        print(f"Moved {key} to {destination_bucket}")

    return {"status": "Success"}
