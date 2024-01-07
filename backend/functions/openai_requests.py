import openai
from decouple import config


#Retrieve Enrivonment Variables
openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")

#Open AI - Whisper
#Convert Audio to Text

def convert_audio_to_text(audio_file):
    try:
        # transcript = openai.Audio.transcribe("whisper-1", audio_file)
        transcript = openai.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format='text'
        )
        #print(transcript)
       # message_text = transcript['data']['translations'][0]['text']
        return transcript
       
    except Exception as e:
        print(e)
        return "this is an error"
