import openai
import openai_apikey
import json
import ast
import re
# Set up the OpenAI API key
openai.api_key = openai_apikey.api_key
assert openai.api_key != "your_api_key", "Please set your OpenAI API key in the `openai.api_key` variable"

def define_paths(folder_name):
    # File to save the generated code
    OUTPUT_CODE_FILE = "folder_name/generated_code.py"
    OUTPUT_DESIGN_FILE = "folder_name/generated_design.txt"
    return OUTPUT_CODE_FILE, OUTPUT_DESIGN_FILE


def chat_with_gpt(prompt, model):
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


def designer(initial_prompt, model):
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

    response = chat_with_gpt(breakdown_prompt, model)
    return response

def critic_design(initial_prompt, current_design, model):
    """
    Use a critic to evaluate the alignment of the initial prompt with the current design.
    """
    critic_prompt = (
        f"You are a programming critic tasked with evaluating the design of a project.\n\n"
        f"The user's goal is as follows: \"{initial_prompt}\".\n\n"
        f"The current design is:\n\n{current_design}\n\n"
        f"Evaluate whether this design sufficiently addresses the user's goal.\n\n"
        f"If the design is complete and effectively decomposes the problem into smaller, manageable components, "
        f"respond only with 'the design is okay as is' and nothing else.\n\n"
        f"If the design is incomplete, provide a detailed list of additional functions, methods, or data structures "
        f"necessary to fully achieve the user's goal. Include the following for each suggestion:\n"
        f"  - Purpose of the function or data structure.\n"
        f"  - Variables and their types.\n"
        f"  - Expected return value.\n\n"
        f"Present your response as a list of dictionaries in the format starting with [ and ending with ], "
        f"with no additional comments or explanations."
    )

    response = chat_with_gpt(critic_prompt, model)
    return response


def concatenate_designs(design, critic, model):
    """
    Concatenate the initial design with the critic's suggestions.
    """
    concatenate_prompt = (
        f"You are a programmer tasked with integrating a program's design and a critic's feedback.\n\n"
        f"The current design is as follows:\n{design}\n\n"
        f"The critic's feedback is as follows:\n{critic}\n\n"
        f"Your task is to combine the design and the critic's feedback into a single, unified design that fully addresses the critic's concerns. "
        f"Ensure the following guidelines are met:\n"
        f"1. Eliminate any redundancy between the design and the feedback.\n"
        f"2. Return the final design in the same format as the original design, starting with [ and ending with ], with no additional comments.\n"
        f"3. Reorder the elements as follows:\n"
        f"   - Define all classes first, including their attributes and methods.\n"
        f"   - Define functions afterward, ensuring that functions appear after any classes or other functions they depend on.\n"
        f"4. Include necessary elements such as imports, global variables, and the main function (`run`) in the correct order.\n"
    )
    response = chat_with_gpt(concatenate_prompt, model)
    return response

def class_coder(current_code, prompt, model):
    """
    Interact with ChatGPT to get a response for a given prompt.
    """
    class_prompt = (
        f"You are a programmer tasked with adding a new Python class to an existing codebase.\n\n"
        f"The current code is as follows:\n{current_code}\n\n"
        f"The new class to be implemented is described in the following JSON-like dictionary, which includes its name, description, "
        f"attributes, and methods:\n{prompt}\n\n"
        f"Your task is to:\n"
        f"1. Add the new class to the provided codebase without modifying the existing code.\n"
        f"2. Fully implement the class, including the `__init__` method and all described methods.\n"
        f"3. Include inline comments or docstrings within the class to explain its purpose and functionality.\n\n"
        f"Output requirements:\n"
        f"- Only return the code for the new class without any additional comments or explanations outside the code.\n"
        f"- Ensure proper formatting and indentation for Python code.\n"
        f"- You cannot use placeholders such as 'add specific logic here'; you must fully implement the logic described in the class descriptor.\n"
    )

    response = chat_with_gpt(class_prompt, model)
    return response


def function_coder(current_code, prompt, model="gpt-4o"):
    """
    Interact with ChatGPT to get a response for a given prompt.
    """
    function_prompt = (
        f"You are a programmer tasked with adding a new Python function or method to an existing codebase.\n\n"
        f"The current code is as follows:\n{current_code}\n\n"
        f"The task is to:\n"
        f"1. Implement a function or method that achieves the following goal:\n{prompt}\n"
        f"2. Add the function or method to the existing code without modifying the current code.\n"
        f"3. If the function is part of a class, ensure it is correctly formatted and indented as a method within the class.\n\n"
        f"Output requirements:\n"
        f"- Only return the code for the new function or method, with no additional comments or explanations outside the code.\n"
        f"- Ensure proper formatting and indentation for Python code.\n"
        f"- Include inline comments or a docstring to describe the function's purpose and behavior.\n"
        f"- Fully implement the logic for the function; avoid placeholders like 'add specific logic here.'\n"
    )

    response = chat_with_gpt(function_prompt, model)
    return response


def improve_code(initial_prompt, current_code, model):
    """
    Use a critic to evaluate the alignment of the initial prompt with the current code.
    """
    improve_prompt = (
        f"You are a critic tasked with improving a codebase to better achieve a programming goal.\n\n"
        f"The user's goal is as follows:\n\"{initial_prompt}\"\n\n"
        f"The current code is as follows:\n{current_code}\n\n"
        f"Your task is to:\n"
        f"1. Rewrite the code to improve its overall quality, readability, and effectiveness in achieving the specified goal.\n"
        f"2. You may:\n"
        f"   - Reorganize the code, changing the order of classes, functions, or methods if needed.\n"
        f"   - Add new functions, methods, or classes to enhance functionality.\n"
        f"   - Remove redundant or unnecessary parts of the code.\n"
        f"   - Fully implement any methods or functions that are currently incomplete.\n"
        f"3. Ensure the code is well-structured and adheres to Python best practices.\n"
        f"4. Include inline comments or docstrings to explain the purpose and functionality of classes, functions, or methods where relevant.\n\n"
        f"Output requirements:\n"
        f"- Return only the improved code, with no additional comments or explanations outside the code.\n"
        f"- Ensure proper formatting, indentation, and a clear, logical flow in the final output.\n"
    )

    response = chat_with_gpt(improve_prompt, model)
    return response


def save_code_to_file(content, file_path):
    """
    Save content to a file.
    """
    with open(file_path, "a") as file:
        file.write(content)
        file.write("\n\n")

def save_design_to_file(content, folder_name):
    """
    Save content to a file.
    """
    path = f"{folder_name}/generated_design.txt"
    with open(path, "a") as file:
        file.write(content)
        file.write("\n\n")

def get_current_code(folder_name, version=None):
    try:
        if version is None:
            with open(f"{folder_name}/generated_code.py", "r") as file:
                current_code = file.read()
        else:
            with open(f"{folder_name}/generated_code_iteration{version}.py", "r") as file:
                current_code = file.read()
        return current_code
    except Exception as e:
        return ""

def erase_current_code(folder_name):
    with open(f"{folder_name}/generated_code.py", "w") as file:
        file.write("")


def erase_current_design(folder_name):
    with open(f"{folder_name}/generated_design.txt", "w") as file:
        file.write("")

def parse_code_output(code_output):
    """
    Parse the code output from the GPT-3 response.
    """
    if 'json' in code_output:
        answer = str(code_output[7:-3])
    elif 'python' in code_output:
        answer = str(code_output[9:-3])
    else:
        answer = code_output if type(code_output) == str else str(code_output)
    return answer

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
        print('trying other method') #dirty hacks here

        input_text = answer
        input_text = re.sub(r"'''(json|python)", "", input_text).strip("'''").strip()
        try:
            return json.loads(input_text)
        except json.JSONDecodeError:
            pass
        try:
            return ast.literal_eval(input_text)
        except (ValueError, SyntaxError):
            pass

        match = re.search(r"\[.*\]", input_text, re.DOTALL)
        if match:
            try:
                return ast.literal_eval(match.group(0))
            except (ValueError, SyntaxError):
                pass

        # If all methods fail, return None or raise an error
        raise ValueError("No valid list found in the input")