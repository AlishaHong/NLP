import vertexai
from vertexai.generative_models import GenerativeModel, Part

def vertext_ai_video():

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
        uri="gs://cloud-samples-data/generative-ai/video/pixel8.mp4",
        mime_type="video/mp4",
    )

    contents = [video_file, prompt]

    response = model.generate_content(contents)
    print(response.text)