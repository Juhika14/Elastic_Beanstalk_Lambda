# Elastic_Beanstalk_Lambda

# AWS Lambda S3 Auto File Sorter

## Overview
This AWS Lambda function automatically moves files from a source S3 bucket (`sourcebucket123456`) to designated buckets based on their file extensions:
- **PNG files** → `pngfile123456`
- **Text files (.txt)** → `textfile123456`
- **PDF files (.pdf)** → `pdffile123456`

The function is triggered whenever a new file is uploaded to the `sourcebucket123456`.

## How It Works
1. The function listens for new objects created in the `sourcebucket123456` S3 bucket.
2. It examines the file extension (`.png`, `.txt`, `.pdf`).
3. Based on the extension, it copies the file to the appropriate bucket.
4. After copying, the original file is deleted from `sourcebucket123456` to ensure clean processing.

## Prerequisites
- An AWS account.
- Three S3 buckets:
  - `sourcebucket123456`
  - `pngfile123456`
  - `textfile123456`
  - `pdffile123456`
- IAM Role with necessary permissions (`AmazonS3FullAccess`).

## Deployment Steps
1. **Create an AWS Lambda Function**
   - Go to AWS Lambda.
   - Click **Create Function** → Choose **Author from Scratch**.
   - Select **Python 3.x** runtime.
   - Assign an IAM role with S3 permissions.

2. **Add an S3 Trigger**
   - Navigate to **Configuration** → **Triggers**.
   - Click **Add Trigger** → Select **S3**.
   - Choose **sourcebucket123456**.
   - Set event type to **Object Created**.
   - Click **Add**.

3. **Upload the Lambda Function Code**
   - Copy and paste the following Python script into the AWS Lambda console:

   ```python
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
