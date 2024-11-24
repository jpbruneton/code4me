# Auto-gpt like project for code only
## Required 
openai APIkey 
## How to run
Execute generate_code with your own prompt

## Descrption
The script generate a code that tries to achieve the user description via multiple, iterative api calls to chatGPT 4o in Python

The goal is to automatically generate comprehensive code based on a single prompt from the user. The process begins by making multiple calls to a large language model, 
such as ChatGPT. First, the model creates a detailed design to meet the user’s requirements. It iterates multiple times to get a proper design in JSON like format.
Next, the design is broken down into smaller components, and the code for each part is generated step by step. 
After each step, another call is made to critique the initial design and code, suggesting improvements and refining the solution until it’s fully optimized.

## Displayed example 
Run results of automatic coding from scratch a space invador game, and of a IMDB like website

todo : run it to see if it works more or less ; add unit tests ; check every functions, etc

Just for the fun :)
See also : https://github.com/Significant-Gravitas/AutoGPT
