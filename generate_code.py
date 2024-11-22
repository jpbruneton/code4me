import utils
import os
if __name__ == "__main__":
    # create the folder generated_scripts/
    os.mkdir('generated_scripts')

    initial_prompt = ("code a space invader game from scratch. The game should have a spaceship that can move left and right,"
                      " shoot bullets, and destroy the aliens. The aliens should move left and right, and when they reach the "
                      "spaceship, the game should end. The game should have a score that increases when the spaceship destroys an alien."
                      " The game should have a start screen, a game over screen, and a way to restart the game. The game should have "
                      "sound effects for shooting, destroying an alien, and the game over screen. The game should have background music"
                      " that loops. The game should have a background image that scrolls. The game should have a way to pause and resume"
                      " the game. The game should have a way to exit the game. The game should have a way to save the high score. The game"
                      " should have a way to load the high score. The game should have a way to display the high score. The game should have"
                      " a way to display the current score. The game should have a way to display the number of lives remaining. The game should"
                      " have a way to display the level. The game should have a way to display the number of aliens remaining. You are allowed to use"
                      " standard libraries to help you code the game, but you should not use any game development frameworks or engines. You don't have the actual graphics,"
                      " sound effects, or music files, so you can use placeholder graphics, sound effects, and music files. You should write the code in Python."
                      "")

    utils.erase_current_code()
    utils.erase_current_design()

    design = utils.designer(initial_prompt)
    print('first design:', type(design), design)
    for _ in range(2):
        critic = utils.critic_design(initial_prompt, design)
        print('critic:', critic)
        design = utils.concatenate_designs(design, critic)

    print('final design:', design)
    print('---------------')
    utils.save_design_to_file(design)

    # now code each subproblem in the design
    list_of_tasks = utils.parse_answer(design)
    for i, task in enumerate(list_of_tasks, start=1):
        print('Subproblem', i, task)
        current_code = utils.get_current_code()
        code = utils.function_coder(current_code, str(task))
        code = utils.parse_code_output(code)
        print('Generated code:', code)
        utils.save_code_to_file(code)
        print('---------------')

    #lets review the code
    print('Getting feedback from the critic...\n')
    additional_tasks = utils.global_review(initial_prompt)
    if additional_tasks is None:
        print('No additional tasks needed. Program should run just fine')
    else:
        print('Additional tasks:', additional_tasks)
        for i, task in enumerate(additional_tasks, start=1):
            print('Subproblem', i, task)
            current_code = utils.get_current_code()
            code = utils.function_coder(current_code, str(task))
            code = utils.parse_code_output(code)
            print('Generated code:', code)
            utils.save_code_to_file(code)
            print('---------------')

    from time import sleep
    for i in range(10):
        print('iteration i:', i)
        version = None if i == 0 else i - 1
        answer = utils.improve_yourself(initial_prompt, utils.get_current_code(version=version))
        answer = utils.parse_code_output(answer)
        utils.save_code_to_file(answer, file_path=f'generated_code_iteration{i}.py')
        sleep(10)