import argparse
import sys
from google.cloud import documentai
from google.cloud import storage
import os
from datetime import datetime
from config import config

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Upload and process an image using Google Document AI')
    parser.add_argument('image_path', help='Path to the image file to process')
    parser.add_argument('--project-id', default=config.PROJECT_ID, help='Google Cloud project ID')
    parser.add_argument('--location', default=config.LOCATION, help='Google Cloud location')
    parser.add_argument('--processor-id', default=config.PROCESSOR_ID, help='Document AI processor ID')
    parser.add_argument('--bucket-name', default=config.GCS_BUCKET_NAME, help='Google Cloud Storage bucket name to upload document to (optional)')

    # Parse arguments
    args = parser.parse_args()

    # Validate file exists
    if not os.path.exists(args.image_path):
        print(f"Error: File '{args.image_path}' does not exist.")
        sys.exit(1)

    # Check if it's an image file and determine MIME type
    file_ext = os.path.splitext(args.image_path)[1].lower()

    # Map file extensions to MIME types
    mime_type_map = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.bmp': 'image/bmp',
        '.tiff': 'image/tiff',
        '.webp': 'image/webp'
    }

    if file_ext not in mime_type_map:
        print(f"Warning: File '{args.image_path}' may not be an image file.")
        mime_type = 'image/jpeg'  # Default to JPEG if unknown
    else:
        mime_type = mime_type_map[file_ext]

    project_id = args.project_id
    location = args.location
    processor_id = args.processor_id

    client = documentai.DocumentProcessorServiceClient()
    name = client.processor_path(project_id, location, processor_id)

    try:
        with open(args.image_path, "rb") as image:
            image_content = image.read()

        # Load binary data
        raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)
        print(f"Successfully loaded image: {args.image_path}")
        print(f"Image size: {len(image_content)} bytes")

        # Configure the process request
        request = documentai.ProcessRequest(
            name=name,
            raw_document=raw_document,
        )

        result = client.process_document(request=request)

        # For a full list of `Document` object attributes, reference this page:
        # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
        document = result.document
        print('document type is: ', document.entities[0].type_)

        # Upload to Google Cloud Storage if bucket is specified
        if args.bucket_name:
            try:
                print(f"\nUploading document to Google Cloud Storage bucket: {args.bucket_name}")

                # Create storage client
                storage_client = storage.Client(project=project_id)
                bucket = storage_client.bucket(args.bucket_name)

                # Use just the filename without path
                gcs_filename = os.path.basename(args.image_path)

                # Create blob and upload
                blob = bucket.blob(gcs_filename)
                blob.upload_from_filename(args.image_path)

                # Set metadata for training purposes
                blob.metadata = {
                    'processor_id': processor_id,
                    'processed_date': datetime.now().isoformat(),
                    'document_type': document.entities[0].type_ if document.entities else 'unknown',
                    'confidence': str(document.entities[0].confidence) if document.entities else 'unknown'
                }
                blob.patch()

                print(f"✅ Successfully uploaded to: gs://{args.bucket_name}/{gcs_filename}")
                print(f"   Document type: {document.entities[0].type_ if document.entities else 'unknown'}")
                print(f"   Confidence: {document.entities[0].confidence if document.entities else 'unknown'}")

            except Exception as upload_error:
                print(f"⚠️  Warning: Failed to upload to GCS: {upload_error}")
                print("   Document AI processing completed successfully, but upload failed.")

    except Exception as e:
        print(f"Error processing image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
