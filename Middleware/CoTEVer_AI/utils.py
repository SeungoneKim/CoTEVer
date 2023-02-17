import datetime
import time
import json
import openai # For GPT-3 API ...

def print_now(return_flag=0):
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    now = now.strftime('%Y/%m/%d %H:%M:%S')
    if return_flag == 0:
        print(now)
    elif return_flag == 1:
        return now
    else:
        pass

def create_demo_text(prompt_path):
    # example sentences ...    
    file = open(prompt_path,"r")
    prompt = file.read()
    demo_text = prompt
    file.close()
    return demo_text

def decoder_for_gpt3(input, max_length=256, key="None",model="gpt3-code",):
    # GPT-3 API allows each users execute the API within 60 times in a minute ...
    time.sleep(1)
    if key == "None":
        with open("./key.json", "r") as f:
            key = json.load(f)
            api_key = key['key']
    else:
        api_key = key
    # https://beta.openai.com/account/api-keys
    openai.api_key = api_key
    
    # Specify engine ...
    # Instruct GPT3
    if model == "gpt3":
        engine = "text-ada-001"
    elif model == "gpt3-medium":
        engine = "text-babbage-001"
    elif model == "gpt3-large":
        engine = "text-curie-001"
    elif model == "gpt3-code":
        engine = "code-davinci-002"
    elif model == "gpt3-text":
            engine = "text-davinci-002"
    else:
        raise ValueError("model is not properly defined ...")
        
    response = openai.Completion.create(
        engine=engine,
        prompt=input,
        max_tokens=max_length,
        top_p=1,
        n=1,
        temperature=0,
        stop="\n\n"
    )
    
    return response["choices"][0]["text"]