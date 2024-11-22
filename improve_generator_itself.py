from generate_code import main
import os

def improve_generator_itself():
    folder_for_model_improvement = 'generated_new_generator'
    if not os.path.exists(folder_for_model_improvement):
        os.mkdir(folder_for_model_improvement)

    with open('generate_code.py', 'r') as file:
        generate_code = file.read()
    with open('utils.py', 'r') as file:
        utils_code = file.read()

    # generate improved code
    initial_prompt = (" I am developping a code that will automatically convert any initial prompt "
                      "into a fully functional Python program. It works by making iterative calls to chatGPT"
                      " to both design and code the program. The current version is the following: \n \n"
                      f"{generate_code} \n\n f{utils_code}\n\n. Now that you understand the current version, and my goal,"
                      f" please provide feedback on how to improve the program. Dont spend too much efforts on error handlings "
                      f"or edge cases, as the program is designed to be run in a controlled environment. My main concern is the logic; "
                      f"how to improve this code generation process. Dont be afraid of being inventive, as I am open to any suggestions."
                      f"The main goal is somehow to get codes that improve themselves via chatgpt or any other LLM model. \n\n"
                      f"You can also provide additional tasks, suggest and implement improvements, and so on")
    main(initial_prompt, folder_for_model_improvement)

improve_generator_itself()