from google.cloud import storage
import vertexai
from vertexai.generative_models import GenerativeModel, Part

bucket_name = '20241105_345_1543_test_bucket'
source_file_name = 'C:/Users/SBA/NLP/videos/2020_travel.mp4'
blob_name = '2020_travel.mp4'
uri = f'gs://{bucket_name}/{blob_name}'

# 버킷 만들기
def create_bucket_class_location(bucket_name):
    """
    Create a new bucket in the US region with the coldline storage
    class
    """
    # bucket_name = "your-new-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = "COLDLINE"
    new_bucket = storage_client.create_bucket(bucket, location="us")

    print(
        "Created bucket {} in {} with storage class {}".format(
            new_bucket.name, new_bucket.location, new_bucket.storage_class
        )
    )
    return new_bucket


# 객체 업로드
def upload_blob(bucket_name, source_file_name, blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to upload is aborted if the object's
    # generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0.
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    generation_match_precondition = 0

    blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)

    print(
        f"File {source_file_name} uploaded to {blob_name}."
    )

# 영상파일 분석
def vertext_ai_video(bucket_name,blob_name):
    PROJECT_ID = 'sesac-24-123'
    LOCATION = 'us-central1'
    MODEL = "gemini-1.5-flash-001"
    # TODO(developer): Update project_id and location
    vertexai.init(project=PROJECT_ID, location= LOCATION)
    model = GenerativeModel(MODEL)

    prompt = """
    Provide a description of the video.
    The description should also contain anything important which people say in the video.
    """
    
    video_file = Part.from_uri(
        uri = f'gs://{bucket_name}/{blob_name}',
        mime_type="video/mp4",
    )

    contents = [video_file, prompt]

    response = model.generate_content(contents)
    print(response.text)


# 객체 삭제하기
def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    generation_match_precondition = None

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to delete is aborted if the object's
    # generation number does not match your precondition.
    blob.reload()  # Fetch blob metadata to use in generation_match_precondition.
    generation_match_precondition = blob.generation

    blob.delete(if_generation_match=generation_match_precondition)

    print(f"Blob {blob_name} deleted.")


# 버킷 삭제하기 
def delete_bucket(bucket_name):
    """Deletes a bucket. The bucket must be empty."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.get_bucket(bucket_name)
    bucket.delete()

    print(f"Bucket {bucket.name} deleted")


create_bucket_class_location(bucket_name)
upload_blob(bucket_name, source_file_name, blob_name)
vertext_ai_video(bucket_name, blob_name)
delete_blob(bucket_name, blob_name)
delete_bucket(bucket_name)




