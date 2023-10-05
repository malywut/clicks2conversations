import random
import json
import utils

ai_current_state = "START"
ai_current_conversation = []

# Import transition prompts from the json file
transition_prompts = json.load(open("./transition_prompts.json", "r"))

# Starting prompt
start_prompt = f"""
You are an assistant for a system that manages vehicle registrations.
All your answers must be a json with two fields, STATE and OUTPUT. Example:
 {{
     "STATE" : "a state",
     "OUTPUT" : "an output"
 }}
Possible states are: {transition_prompts.keys()}.  Do not use anything else
Outputs will be outputed to the user. 
Do not answer anything else than a json with the two fields. The output must be parsable by json.loads
Your first output will be STATE: START and OUTPUT: a welcoming question
"""


def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True


def get_response(chat_input: str = None):
    global ai_current_state
    if chat_input is None:
        ai_input = start_prompt
    else:
        ai_input = f'User input : {chat_input}. {transition_prompts[ai_current_state]}'
    ai_current_conversation.append({"role": "user", "content": ai_input})

    # Try 5 times max to generate an output with the model that is correct json
    for i in range(5):
        ai_output = utils.generate(ai_current_conversation)
        if validateJSON(ai_output):
            break

    chat_output = json.loads(ai_output)["OUTPUT"]
    ai_current_state = json.loads(ai_output)["STATE"]
    ai_current_conversation.append({"role": "assistant", "content": ai_output})
    return chat_output


def do_action():
    # Print actions in blue
    print("\033[94m" + ai_current_state + "\033[0m")
    reset()


def reset():
    global ai_current_state
    global ai_current_conversation
    # Start conversation and state over.
    ai_current_state = "START"
    ai_current_conversation = []
    starting_question = get_response()
    print("Assistant:", starting_question)


def main():
    print("Welcome to the Vehicle Registration Chat System")
    print("Type 'exit' to end the conversation.")
    reset()
    while True:
        # Print in green states
        print("\033[92m" + ai_current_state + "\033[0m")

        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Assistant: Goodbye!")
            break
        print("\033[92m" + ai_current_state + "\033[0m")
        
        response = get_response(user_input)
        print("Assistant:", response)
        if (ai_current_state.startswith("ACTION")):
            do_action()


if __name__ == "__main__":
    main()
