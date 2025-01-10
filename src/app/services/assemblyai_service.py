import assemblyai as aai
from utils.response_builder import ResponseBuilder
from config import ASSEMBLYAI_API_KEY

aai.settings.api_key = ASSEMBLYAI_API_KEY

def assemblyaiTranscribe(audioContent):
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audioContent)
    return ResponseBuilder().setSuccess(True).setMessage("Transcription Generated Successfully").setData(transcript.text).setStatusCode(200).build()