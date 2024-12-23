import utils
import os
from time import sleep


def main(model, initial_prompt, design_iterations, project_name, folder_name='generated_scripts'):

    utils.make_directory(project_name)
    folder_name = os.path.join(project_name, folder_name)
    utils.make_directory(folder_name)

    utils.erase_current_code(folder_name)
    utils.erase_current_design(folder_name)

    design = utils.designer(initial_prompt, model)
    print('first design:', type(design), design)
    for _ in range(design_iterations):
        critic = utils.critic_design(initial_prompt, design, model)
        print('critic:', critic)
        design = utils.concatenate_designs(design, critic, model)
        sleep(10)
    print('final design:', design)
    print('---------------')
    utils.save_design_to_file(design, folder_name)

    # now code each subproblem in the design
    list_of_tasks = utils.parse_answer(design)
    for i, task in enumerate(list_of_tasks):
        print('Subproblem', i, task)
        if ('description' in task.keys() and 'class' in task['description']) or 'class' in task:
            current_code = utils.get_current_code(folder_name)
            code = utils.class_coder(current_code, str(task), model)
        else:
            current_code = utils.get_current_code(folder_name)
            code = utils.function_coder(current_code, str(task), model)
        code = utils.parse_code_output(code)
        print('Generated code:', code)
        filepath = f'{folder_name}/generated_code_iteration0.py'
        utils.save_code_to_file(code, filepath)
        sleep(20)
        print('---------------')

    for i in range(1, 6):
        print('iteration i:', i)
        version = i - 1
        answer = utils.improve_code(initial_prompt, utils.get_current_code(folder_name, version=version), model)
        answer = utils.parse_code_output(answer)
        filepath = f'{folder_name}/generated_code_iteration{i}.py'
        utils.save_code_to_file(answer, filepath)
        sleep(20)

if __name__ == "__main__":

    model = 'gpt-4o'
    # this is just an example prompt, itself refined by online chatGPT
    initial_prompt = (
    "Code a Space Invaders game from scratch with the following features:\n\n"
    "Core Gameplay:\n"
    "1. A spaceship that can move left and right and shoot bullets to destroy aliens.\n"
    "2. Aliens that move left and right, descending progressively. The game ends if an alien reaches the spaceship.\n"
    "3. A scoring system that increases when the spaceship destroys an alien.\n"
    "4. A start screen, game over screen, and a way to restart the game.\n"
    "5. Display current score, high score, level, number of lives, and remaining aliens.\n"
    "6. Include a way to pause/resume the game and exit it.\n\n"
    "Technical Details:\n"
    "1. Use Python to write the code.\n"
    "2. Do not use any game development frameworks or engines; standard libraries are allowed.\n"
    "3. Use placeholder graphics for the spaceship, aliens, and background as needed.\n"
    "4. Implement functionality to save and load the high score.\n\n"
    "Additional Notes:\n"
    "- Focus on core gameplay mechanics and visuals, not sound effects or music.\n"
    "- Ensure smooth gameplay and responsiveness."
    )
    #main(model, initial_prompt, design_iterations=5, project_name='space_invador', folder_name='generated_scripts')

    # another example prompt, same comment
    initial_prompt = (
    "Develop a fully functional website modeled after IMDb with the following features and specifications:\n\n"
    "Core Features:\n"
    "1. Add Titles: Users should be able to add new titles (e.g., movies, shows, or other content).\n"
    "2. Rankings: Users can assign a ranking (e.g., 1-10 scale) to each title.\n"
    "3. Reviews: Users can provide a text-based review for each title.\n"
    "4. Search Bar: Include a search functionality to allow users to find titles easily by name.\n"
    "5. Sorting: Provide the ability to sort titles by their ranking.\n\n"
    "Technical Requirements:\n"
    "1. Database:\n"
    "- Use a small, lightweight database to store titles, rankings, and reviews.\n"
    "- No user-specific data (e.g., user accounts or personal details) should be stored.\n\n"
    "2. Backend:\n"
    "- Use Python to develop the backend.\n"
    "- The backend should handle CRUD (Create, Read, Update, Delete) operations for titles, rankings, and reviews.\n"
    "- Implement RESTful APIs to support communication between the frontend and backend.\n\n"
    "3. Frontend:\n"
    "- Design a simple, user-friendly interface for the website.\n"
    "- The frontend can be built using any programming language or framework (e.g., HTML/CSS/JavaScript, React, Vue, etc.).\n\n"
    "4. Deployment:\n"
    "- Deploy the website on an AWS instance. Ensure it is fully operational and accessible online.\n"
    "- Provide setup instructions for deploying and running the application on AWS.\n\n"
    "Additional Notes:\n"
    "- Ensure the website is responsive and works across devices (desktop, tablet, mobile).\n"
    "- Optimize the code for maintainability and scalability.\n"
    "- Provide detailed documentation for both the backend and frontend, including setup, deployment, and usage instructions."
    )


    main(model, initial_prompt, design_iterations=5, project_name='trading_grid', folder_name='generated_scripts')