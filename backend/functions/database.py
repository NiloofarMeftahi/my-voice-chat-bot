import json
import random
#get recent messages
def get_recent_messages():
    #define the file name abd  learn instructions
    file_name = "stored_data.json"
    learn_instruction = {
        "role" : "system",
        "content" : "You are a mental health recommender system. Your name is Maya. The user is called Nil. Keep your answers under 50 words."
    }

    # initialize messages
    messages = []

    # add a random element
    x = random.uniform( 0, 1)
    if x < 0.5:
        learn_instruction["content"] = learn_instruction["content"] + "Your responce will be supportive and encouraging"
    else:
         learn_instruction["content"] = learn_instruction["content"] + "Your responce will be challenging"
    messages.append(learn_instruction)
    # get last messages
    try:
        with open(file_name) as user_file:
            data = json.load(user_file)

            # append last 5 items of data
            if data:
                if len(data) < 5:
                    for item in data:
                        messages.append(item)
                else:
                    for item in data[-5]:
                        messages.append(item)
    except Exception as e:
        print(e)
        pass
    #retutb
    return messages

#store messages
def store_messages(request_message, response_message):
    #define the file name
    file_name = "stored_data.json"

    #get recent messages
    messages = get_recent_messages()[1:]

    # add nessages to data
    user_message = {"role": "user" , "content" : request_message}
    assistant_message = {"role": "assistant" , "content" : response_message}
    messages.append(user_message)
    messages.append(assistant_message)

    # save the updated file
    with open(file_name, "w") as f:
        json.dump(messages , f)
    
    #rest messages
    
def reset_messages():
        #overwrite the current file with nothing
        open("stored_data.json" , "w")
