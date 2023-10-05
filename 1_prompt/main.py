import random
import json
import utils

ai_current_conversation = []


# Starting prompt
start_prompt = f"""
You are an assistant for a system that manages vehicle registrations.
All your answers must be a json with three fields, OUTPUT, FUNCTION and ARGS. Example:
 {{
     "OUTPUT" : "an output", 
     "FUNCTION" : "a function to call",
     "ARGS":"the arguments for the function call"
 }}
Outputs will be outputed to the user. 
Possible functions are CREATE_REGISTRATION, UPDATE_REGISTRATION, DELETE_REGISTRATION
Possible ARGS are model; owner_name, year.
The user can ask for a new registration, update information on an existing registration, delete an registration.
To create a new registration, the user must provide a model, the year it was created, and the owner's name.
To update an registration, the user must provide the registration number, and the new information. 
To delete and registration, the user must provide an registration number.
The user must provide explicit confirmation before fulfilling the request.
If you need to ask details to the user, or ask confirmation, use OUTPUT.
If you want to perform the requested action : use FUNCTION and ARGS. Do not use FUNCTION and ARFS if the user as not confirmed.
Do not answer anything else than a json with the two fields. The output must be parsable by json.loads
Your first output will be OUTPUT: a welcoming question
"""


def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True


def get_response(chat_input: str = None):
    if chat_input is None:
        ai_input = start_prompt
    else:
        ai_input = f'{chat_input}'
    ai_current_conversation.append({"role": "user", "content": ai_input})

    # Try 5 times max to generate an output with the model that is correct json
    for i in range(5):
        ai_output = utils.generate(ai_current_conversation)
        if validateJSON(ai_output):
            break
    print("\033[92m" + ai_output + "\033[0m")     
    json_output = json.loads(ai_output)   
    chat_output = json_output.get("OUTPUT", None)
    function = json_output.get("FUNCTION", None)
    args = json_output.get("ARGS", None)
    
    if(function is not None and function != ""):
        chat_output = execute_function(function, args)

    ai_current_conversation.append({"role": "assistant", "content": ai_output})
    return chat_output

def execute_function(function, args):
    if function is not None:
        if function == "CREATE_REGISTRATION":
            # TODO register car
            print("Registering car with input", args)
            chat_output = "AA-123-BB"
        elif function == "UPDATE_REGISTRATION":
            # TODO update car registration
            chat_output = True
        elif function == "DELETE_REGISTRATION":
            # TODO delete car registration
            chat_output = True
    return chat_output


def reset():
    global ai_current_conversation
    # Start conversation and state over.
    ai_current_conversation = []
    starting_question = get_response()
    print("Assistant:", starting_question)


def main():
    print("Welcome to the Vehicle Registration Chat System")
    print("Type 'exit' to end the conversation.")
    reset()
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Assistant: Goodbye!")
            break
        
        response = get_response(user_input)
        print("Assistant:", response)


if __name__ == "__main__":
    main()
