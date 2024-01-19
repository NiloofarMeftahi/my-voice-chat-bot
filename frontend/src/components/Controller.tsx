import React from 'react'
import { useState } from 'react'
import Title from './Title';
import Recorder from './Recorder';
import axios from 'axios';

function Controller() {
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<any[]>([]);
  const [blob, setBlob] = useState("");

  const createBlobUrl = (data: any) => {
    const blob = new Blob([data], {type: "audio/mpeg"});
    const url = window.URL.createObjectURL(blob);
    return url;
  };

  const handleStop = async (blobUrl: string) => {
    setIsLoading(true);
    // append recorded message to messages

const myMessage = {sender: "me", blobUrl};
const messagesArr = [...messages, myMessage];
//convert blob url to blob object
fetch(blobUrl)
.then((res) => res.blob())
.then(async(blob) => {
  //construct audio to send file
  const formData = new FormData();
  formData.append("file", blob, "myFile.wav");
  //send form data to api endpoint
  await axios.post("http://localhost:8000/post-audio", 
  formData, {headers: {"Content-Type": "audio/mpeg"}, 
  responseType : "arraybuffer", })
  .then((res: any)=>{
    const blob = res.data;
    const audio = new Audio();
    audio.src = createBlobUrl(blob);

    //append to audio
    const mayaMessage = {sender: "Maya", blobUrl: audio.src};
    messagesArr.push(mayaMessage);
    setMessages(messagesArr);
    // play audio
    setIsLoading(false);
    audio.play();


  }).catch((err)=> {
    console.error(err.message);
    setIsLoading(false);
  })
});  
//setIsLoading(false);

    // setBlob(blobUrl);
   
  };
  return (
    <div className='h-screen overflow-y-hidden'>
        <Title setMessages={setMessages} />
        <div className='flex flex-col justify-between h-full overflow-y-scroll pb-96'>
          {/* Show conversation */}
          <div className='mt-5 px-5'>
            {messages.map((audio, index) => {
              return <div key={index + audio.sender} 
              className={"flex flex-col " + 
              (audio.sender == "Maya" && "flex items-end")}>
                {/* Sender */}
                <div className='mt-4'>
                 <p className={audio.sender == "Maya" ? "text-right mr-2 italic text-pink-400": 
                 "ml-2 italic text-blue-400"}>
                  {audio.sender}
                 </p>
                 {/* audio message  */}
                 <audio src = {audio.blobUrl} className=' appearance-none'
                 controls></audio>

                </div>
                
              </div>
            })}
            {messages.length == 0 && !isLoading && (
              <div className='text-center font-light italic mt-10'>
                Send Maya a message...
              </div>

            )}
            {isLoading && (
              <div className=' text-center font-light italic mt-10 animate-pulse'>
                Give me a few seconds...
              </div>
            )}
          </div>
            {/* Recorder */}
            <div className='fixed bottom-0 w-full py-6 border-t text-center bg-gradient-to-r from-sky-400 to-pink-400'>
              <div className='flex justify-center items-center w-full'> 
                <Recorder handleStop={handleStop}/>
              </div>
            </div>
        </div>
        
        </div>
  )
}

export default Controller