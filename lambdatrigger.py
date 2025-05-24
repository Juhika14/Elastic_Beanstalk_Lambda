import boto3
import urllib.parse

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    for record in event.get('Records', []):
        source_bucket = 'sourceebucket123456'
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])
        
        # Determine destination bucket based on file extension
        if key.endswith('.png'):
            destination_bucket = 'pngfile123456'
        elif key.endswith('.txt'):
            destination_bucket = 'textfile123456'
        elif key.endswith('.pdf'):
            destination_bucket = 'pdffile123456'
        else:
            print(f"Unsupported file type: {key}")
            continue  # skip instead of returning for multiple files
        
        try:
            # Copy the object
            copy_source = {'Bucket': source_bucket, 'Key': key}
            s3_client.copy_object(CopySource=copy_source, Bucket=destination_bucket, Key=key)
            
            # Delete from source
            s3_client.delete_object(Bucket=source_bucket, Key=key)
            
            print(f"Moved {key} from {source_bucket} to {destination_bucket}")
        
        except Exception as e:
            print(f"Error processing {key}: {str(e)}")

    return {"status": "Success"}
