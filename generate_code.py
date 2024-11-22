import utils

if __name__ == "__main__":
    initial_prompt = ("Generate possible Binary Trees such that leaves values are taken from a given list of random integers, "
                      "and such that every parent node has a value equals to the sum of its children, "
                      "and such that the root node has a given target value.")

    utils.erase_current_code()
    utils.erase_current_design()

    design = utils.designer(initial_prompt)
    print('first design:', type(design), design)
    critic = utils.critic_design(initial_prompt, design)
    print('critic:', critic)
    if critic == 'Yes':
        pass
    else:
        design = utils.concatenate_designs(design, critic)

    print('final design:', design)
    print('---------------')
    utils.save_design_to_file(design)

    # now code each subproblem in the design
    list_of_tasks = utils.parse_answer(design)
    for i, task in enumerate(list_of_tasks, start=1):
        print('Subproblem', i, task)
        code = utils.function_coder(str(task))
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
            code = utils.function_coder(str(task))
            print('Generated code:', code)
            utils.save_code_to_file(code)
            print('---------------')
