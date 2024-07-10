#SETUP
API,RUN = False,True
import json,os,requests,openai,importlib;from functools import lru_cache;pure_red,dark_green,orange,dark_blue,bright_purple,dark_cyan,dull_white,pure_black,bright_red,light_green,grey,reset_colour,reverse_colour,invisible,darken,italic,underline,bold,bright_white,bright_black,light_cyan,magenta,bright_blue,yellow,GPT_MODEL,openai.api_key = "\033[0;31m","\033[0;32m","\033[0;33m","\033[0;34m","\033[0;35m","\033[0;36m","\033[0;37m","\033[0;30m","\033[0;91m","\033[0;92m","\x1b[90m",'\033[0m','\033[07m','\033[08m',"\033[2m","\033[3m","\033[4m","\033[1m","\033[0;97m","\033[0;90m","\033[0;96m","\033[0;95m","\033[0;94m","\033[0;93m","gpt-3.5-turbo-0613",os.getenv("OPENAI_API_KEY")
if not API: 
    scripturemodel="genesis";os.system("clear");f = importlib.import_module(scripturemodel)
#RUN FUNCTIONS
def chat_completion_request(messages, functions=None, function_call=None, model=GPT_MODEL): 
    headers,json_data = {"Content-Type": "application/json","Authorization": "Bearer " + openai.api_key},{"model": model, "messages": messages}
    if functions is not None:json_data.update({"functions": functions})
    if function_call is not None:json_data.update({"function_call": function_call})
    try: response = requests.post("https://api.openai.com/v1/chat/completions",headers=headers,json=json_data);return response
    except Exception as e: print("Unable to generate ChatCompletion response");print(f"Exception: {e}");return e
#GET MODEL
if not API:
    filename = f"{scripturemodel}.json"
    with open(filename, "r") as file: functions = json.load(file)
#RUN STANDARD GPT MODEL
def return_result(msgs):
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=msgs,temperature=0.5)
    print(completion)
    for i in completion['choices']:
        output = i['message']['content']
    return output
#RETURN DATA AS RESULT
def run_func(func_name, args, lib, q):
    params = ", ".join(args)
    messages = [
    {"role": "system", "content": f"You will be give some data that is the result of the function '{func_name}' with the parameters {params}. Your job is to answer the user's question ({q}) using the data as the basis for your answer."}
]
    func = getattr(lib, func_name)
    res = func(**args)
    resstr = "\n".join(res)
    messages.append({"role": "user", "content": f"Data:\n{resstr}"})
    return return_result(messages)
messages = [
    {"role": "system", "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."},
]
@lru_cache(maxsize=128)
def run(query):
    messages.append({"role": "user", "content": query})
    chat_response = chat_completion_request(messages, functions=functions);print(chat_response.json());assistant_message = chat_response.json()["choices"][0]["message"];messages.append(assistant_message)
    try:
        result = run_func(assistant_message["function_call"]["name"], json.loads(assistant_message["function_call"]["arguments"]),f,query)
        print(bright_blue+result)
        return result
    except:
        for i in chat_response.json()['choices']:
            output = i['message']['content']
        print(bright_blue+output)
        return output
