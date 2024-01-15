## Imports
import random # For picking a random line
import subprocess # For GUI
import sys # For neat exits

## GUI Defs
def ask_if_known_word(word):
    command = '''
    osascript -e 'display dialog "Do you know this word: '''+word+'''" buttons {"Exit", "No", "Yes"} default button "Yes"'
    '''
    user_response = subprocess.check_output(command)

    print(user_response)
          
    exit() # Pause

    

    user_response = str(user_response)[16:] # Only look at the stuff after the "Button received" generic output text

    if user_response == 'Yes':
        print("Yes")
    elif user_response == 'No':
        print("No")
    elif user_response == 'Exit':
        print("Exit")
    else:
        sys.exit(f"Error: invalid button received. Expected ['Yes', 'No', 'Exit'] but got {command}")


## Main function that gets repeated
def mainloop():
    line_number = random.randint(1, 10000) # Pick a line number within the file range
    with open('english_words.txt', 'r') as file: # Open the words file
        for current_line, line in enumerate(file, start=1): # Go down line by line
            if current_line == line_number: # When the random line is reached
                word = line.strip() # Get the line cleanly
                word = word.upper() # Makes the word uppercase for better readability
                ask_if_known_word(word) # Ask if word is known

    print(f"At line {line_number} I saw {word}")

## Code call
mainloop()