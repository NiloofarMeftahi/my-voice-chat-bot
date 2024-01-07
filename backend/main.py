#uvicorn main:app
#uvicorn main:app --reload
#venv\Scripts\activate
#breakibf reload ctrl c


from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai

#custom Function Imports
from functions.openai_requests import convert_audio_to_text , get_chat_response
from functions.database import store_messages, reset_messages
from functions.text_to_speech import convert_text_to_speech 
#...

#Initiate App
app = FastAPI()

#CORS - Origins
origins = [
    "http://localhost:5173"
    "http://localhost:5174"
    "http://localhost:4173"
    "http://localhost:4174"
    "http://localhost:3000"
]

#CORS - middlaeware
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

#Check Health
@app.get("/health")
async def check_health():
    return {"message": "Healthy"}

#reset messages
@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"message": "Conversation reset"}

#get audio
@app.get("/post-audio-get/")
async def get_audio():

    # Get saved audio
    audio_input = open("voice.mp3", "rb")
    #Decode audio
    message_decoded = convert_audio_to_text(audio_input)    
    # gaurd message decoded
    if not message_decoded:
        return HTTPException(status_code=400, detail = "Failed to decode audio")
    #print(message_decoded)
    #get chatgpt response
    chat_response = get_chat_response(message_decoded)
     # gaurd message decoded
    if not chat_response:
        return HTTPException(status_code=400, detail = "Failed to get chat response")
    #store messages
    store_messages(message_decoded , chat_response)
    #print(chat_response)

    #conver chat response to audio
    audio_output = convert_text_to_speech(chat_response)
     # gaurd message decoded
    if not message_decoded:
        return HTTPException(status_code=400, detail = "Failed to get eleven lans audio response")
    #creat a generator that yields chunks of data

    def iterfile():
        yield audio_output
    #returtn audio
    return StreamingResponse(iterfile(), media_type="audio/mpeg")

    #return "Done"
#Post bot response
#Note: not playing in the browser when using the post request
# @app.post("/post-audio/")
# async def post_audio(file: UploadFile = File(...)):

#         print("Hello")