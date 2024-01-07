import openai
from decouple import config
#import custno functions
from functions.database import get_recent_messages

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
#oprn AI chatgpt
# get reposnce to the message
def get_chat_response(message_input):
    messages = get_recent_messages()
    user_message = {"role" : "user", "content" : message_input}
    messages.append(user_message)
    #print(messages)
    try:
        response = openai.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = messages,
            stream=True,
        )
        message_text = ""
        #print(response)
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content is not None:
                #print(chunk.choices[0].delta.content, end="")
                
                message_text += chunk.choices[0].delta.content
       
        return message_text
    except Exception as e:
        print(e)
        return