# Imports the Google Cloud Translation library
from google.cloud import translate_v3 as translate

DATASET_ID = "example-set1"  # change this to any dataset ID

def create_adaptive_mt_dataset():
    # Create a client
    client = translate.TranslationServiceClient()
    # Initialize request argument(s)
    adaptive_mt_dataset = translate.types.AdaptiveMtDataset()
    adaptive_mt_dataset.name = f"projects/sesac-24-123/locations/us-central1/adaptiveMtDatasets/{DATASET_ID}"
    adaptive_mt_dataset.display_name = "Example set"
    adaptive_mt_dataset.source_language_code = "en"
    adaptive_mt_dataset.target_language_code = "ko"
    request = translate.CreateAdaptiveMtDatasetRequest(
        parent="projects/sesac-24-123/locations/us-central1",
        adaptive_mt_dataset=adaptive_mt_dataset,
    )
    # Make the request
    response = client.create_adaptive_mt_dataset(request=request)
    # Handle the response
    print(response)

def import_adaptive_mt_file():
    # Create a client
    client = translate.TranslationServiceClient()
   # Define the request with the required parameters
    request = translate.ImportAdaptiveMtFileRequest(
        parent=f"projects/sesac-24-123/locations/us-central1/adaptiveMtDatasets/{DATASET_ID}",
        input_config=translate.InputConfig(
            gcs_source=translate.GcsSource(input_uri="gs://path/to/your/file")  # Update this with your file path
        )
    )
    # Make the request
    response = client.import_adaptive_mt_file(request)
    # Handle the response
    print(response)

def adaptive_mt_translate():
    # Create a client
    client = translate.TranslationServiceClient()
    # Initialize the request
    request = translate.AdaptiveMtTranslateRequest(
        parent="projects/sesac-24-123/locations/us-central1",
        dataset=f"projects/sesac-24-123/locations/us-central1/adaptiveMtDatasets/{DATASET_ID}",
        content=[]
    )
    # Make the request
    response = client.adaptive_mt_translate(request)
    # Handle the response
    print(response)

create_adaptive_mt_dataset()
import_adaptive_mt_file()
adaptive_mt_translate()