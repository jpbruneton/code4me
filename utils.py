import openai
import ast
import openai_apikey
# Set up the OpenAI API key
openai.api_key = openai_apikey.api_key
assert openai.api_key != "your_api_key", "Please set your OpenAI API key in the `openai.api_key` variable"

# File to save the generated code
OUTPUT_CODE_FILE = "generated_code.py"
OUTPUT_DESIGN_FILE = "generated_design.txt"

def chat_with_gpt(prompt, model="gpt-4o"):
    """
    Interact with ChatGPT to get a response for a given prompt.
    """
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant for programming tasks in Python."},
            {"role": "user", "content": prompt},
        ]
    )
    return response['choices'][0]['message']['content']


def designer(initial_prompt):
    """
    Use ChatGPT to break down the goal into subproblems.
    """
    breakdown_prompt = (
    f"Decompose the following programming task into a datastructure problem and associated list of subproblems. "
    f"You can use both classes and functions. Each subproblem should describe a single Python function or method within a class"
    f" in a concise sentence. Take as many subproblems as needed to achieve the goal. "
    f"The description must include the function's purpose, the variables (with their types), "
    f"and the expected return value. Provide the response as a list of dictionnaries,"
    f" must be starting with [, ending with ] format with no additional comments. Each such item may describe functions, "
    f"or classes, depending on the task. If they are classes, you need to provide the detailed list of attributes and methods.\n\n"
    f"Make sure that the combinations of all these functions will achieve the goal. The main function to execute the program should be called 'run'.\n\n"
    f"The overall task is as follows:\n\n{initial_prompt}"
    )

    response = chat_with_gpt(breakdown_prompt)
    return response

def critic_design(initial_prompt, current_design):
    """
    Use a critic to evaluate the alignment of the initial prompt with the current design.
    """
    critic_prompt = f"""
    You are a critic evaluating programming tasks.

    The user provided this goal: "{initial_prompt}".

    Here is the current design:

    {current_design}

    Evaluate if this design and split of the main problem into smaller problems will be enough to achieve the goal.
    If yes, just return 'the design is ok as is' and nothing else. 
    If not, suggest more functions and/or data structures to do so. Provide the response as a list of dictionaries,"
    f" that must be starting with [, ending with ] with no additional comments.
    """
    response = chat_with_gpt(critic_prompt)
    return response

def critic_review(initial_prompt, current_code):
    """
    Use a critic to evaluate the alignment of the initial prompt with the current code.
    """
    critic_prompt = f"""
    You are a critic evaluating programming tasks.

    The user provided this goal: "{initial_prompt}".

    Here is the code so far:

    {current_code}

    Evaluate if this code meets the goal, especially if it can run as is to achieve the goal.
    If yes, just return 'Yes' and nothing else. 
    If not, suggest additional functions to do so. Provide the response as a list of dictionaries,"
    f" that must be starting with [, ending with ] with no additional comments.
    """
    response = chat_with_gpt(critic_prompt)
    return response


def concatenate_designs(design, critic):
    """
    Concatenate the initial design with the critic's suggestions.
    """
    concatenate_prompt = f""" You are a programmer combining different parts of a program. You have a design and a critic's feedback.
    The design is as follows:
    {design}
    The critic's feedback is as follows:
    {critic}
    Combine the design and the critic's feedback into a single design that addresses the critic's concerns. Avoid redundancy.
    Return an answer in the same format as the design, starting with [, ending with ] with no additional comments.
    Also, reorder the tasks such that classes are defined first, followed by functions. Make sure that functions are defined after the classes they depend on, 
    as well as other functions they may depend on. In this process, don't forget elements like imports, global variables, and the main function."""
    response = chat_with_gpt(concatenate_prompt)
    return response

def function_coder(current_code, prompt, model="gpt-3.5-turbo"):
    """
    Interact with ChatGPT to get a response for a given prompt.
    """
    function_prompt = f"""
    You are a programmer writing code for a specific function. The code you write should be a Python function or method within a class.
    The current code is as follows:
    {current_code}
    The task is as follows: you have to add a function or method to the code that will achieve the following goal:
    {prompt}
    Only return code without any extra comments. Make sure the code is correctly formatted and indented in particular 
    if its a method for a class that is being added. You cant change the existing code, only add new code.
    You can't pass or say "add speficic logic for function_name", you have to write the code.
    """
    response = chat_with_gpt(function_prompt, model=model)
    return response



def global_review(initial_prompt):
    current_code = get_current_code()
    critic_response = critic_review(initial_prompt, current_code)
    if critic_response == 'Yes' or 'Yes' in critic_response: # s'il renvoie ['Yes'] ce con
        additional_tasks = None
    else:
        additional_tasks = parse_answer(critic_response)
    return additional_tasks

    return critic_response


def save_code_to_file(content, file_path=OUTPUT_CODE_FILE):
    """
    Save content to a file.
    """
    with open(file_path, "a") as file:
        file.write(content)
        file.write("\n\n")

def save_design_to_file(content, file_path=OUTPUT_DESIGN_FILE):
    """
    Save content to a file.
    """
    with open(file_path, "a") as file:
        file.write(content)
        file.write("\n\n")

def get_current_code():
    with open("generated_code.py", "r") as file:
        current_code = file.read()
    return current_code

def erase_current_code():
    with open("generated_code.py", "w") as file:
        file.write("")

def erase_current_design():
    with open("generated_design.txt", "w") as file:
        file.write("")

def parse_answer(answer):
    """
    Parse the answer from the GPT-3 response, given that it should be of the form '["item1", "item2", ...]'.
    This function just removes the brackets and tranform the str to a python list.
    """
    if 'json' in answer:
        answer = str(answer[7:-3])
    if 'python' in answer:
        answer = str(answer[9:-3])
    try:
        return ast.literal_eval(answer)
    except Exception as e:
        print(f"Error parsing the answer: {e}")
        print(type(answer))
        print(answer)
        return None