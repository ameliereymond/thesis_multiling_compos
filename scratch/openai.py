import os
import requests
import json

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

def query_openai(prompt):
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        },
        json = {
            "model": "gpt-3.5-turbo",
            "messages": [

                {
                    "role": "user",
                    "content": prompt[1:-1]
                }
            ]
        }
    )

    if response.status_code == 200:
        return response.json().choices[0].message
    else:
        raise Exception(f"OpenAI returned HTTP {response.status_code} with message {response.json()}")


print(query_openai("""IN: run opposite right after look opposite left twice OUT: I_TURN_LEFT I_TURN_LEFT I_LOOK I_TURN_LEFT I_TURN_LEFT I_LOOK I_TURN_RIGHT I_TURN_RIGHT I_RUN
IN: turn around right after turn around right OUT: I_TURN_RIGHT I_TURN_RIGHT I_TURN_RIGHT I_TURN_RIGHT I_TURN_RIGHT I_TURN_RIGHT I_TURN_RIGHT I_TURN_RIGHT
IN: walk and turn opposite left OUT: I_WALK I_TURN_LEFT I_TURN_LEFT
IN: jump right thrice and run right twice OUT: I_TURN_RIGHT I_JUMP I_TURN_RIGHT I_JUMP I_TURN_RIGHT I_JUMP I_TURN_RIGHT I_RUN I_TURN_RIGHT I_RUN
IN: look opposite left thrice after walk right thrice OUT: I_TURN_RIGHT I_WALK I_TURN_RIGHT I_WALK I_TURN_RIGHT I_WALK I_TURN_LEFT I_TURN_LEFT I_LOOK I_TURN_LEFT I_TURN_LEFT I_LOOK I_TURN_LEFT I_TURN_LEFT I_LOOK
IN: jump after turn opposite right twice OUT: I_TURN_RIGHT I_TURN_RIGHT I_TURN_RIGHT I_TURN_RIGHT I_JUMP
IN: look right and walk around right OUT: I_TURN_RIGHT I_LOOK I_TURN_RIGHT I_WALK I_TURN_RIGHT I_WALK I_TURN_RIGHT I_WALK I_TURN_RIGHT I_WALK
IN: jump thrice after walk opposite right twice OUT: I_TURN_RIGHT I_TURN_RIGHT I_WALK I_TURN_RIGHT I_TURN_RIGHT I_WALK I_JUMP I_JUMP I_JUMP
IN: walk around left thrice and look opposite left twice OUT: """))

