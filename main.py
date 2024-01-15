## Imports
import random # For picking a random line
import subprocess # For GUI w/ input capture
import os # For GUI w/o input capture
import playsound # For sound effects
import time # For waiting for sound effect to play

# Helper functions
def audio(name):
    if name == 'correct':
        playsound.playsound('audio/correct.mp3', False) # False lets this run async
        time.sleep(0.6)
    elif name == 'wrong':
        playsound.playsound('audio/wrong.mp3', False)
        time.sleep(0.6)

def word_known(word):
    audio('correct')
    with open('known.txt', 'a') as file_2:
        file_2.write(f"{word}\n")
        file_2.close()

def word_unknown(word):
    audio('wrong')
    with open('unknown.txt', 'a') as file_2:
        file_2.write(f"{word}\n")
        file_2.close()

def ask_if_known_word(word, question, total_questions):
    command = f'''
    osascript -e 'display dialog "Question {question} out of {total_questions}: Do you know this word?\n\n{word}" buttons {{"🚫 No", "✅ Yes"}}'
    '''
    user_response_bytes = subprocess.check_output(command, shell=True) # Run the command and capture output
    user_response = user_response_bytes.decode('utf-8') # Format output to regular string

    # Extract the relevant parts of the response
    user_response = user_response[16:] # Get rid of the 'button pressed' part
    user_response = user_response[0:-1] # Get rid of the new line

    if user_response == '✅ Yes':
        word_known(word)
        return True
    else:
        word_unknown(word)

## Main function that gets repeated
def mainloop(question_num, total_num):
    line_number = random.randint(1, 10000) # Pick a line number within the file range
    with open('source.txt', 'r') as file: # Open the words file
        for current_line, line in enumerate(file, start=1): # Go down line by line
            if current_line == line_number: # When the random line is reached
                word = line.strip() # Get the line cleanly
                word = word.upper() # Makes the word uppercase for better readability
                return ask_if_known_word(word, question_num, total_num) # Ask if word is known
            
            
## Functions from start menu            
def reset_mode():
    command = f'''
    osascript -e 'display dialog "ERASE MODE:\n\nWhat will be erased:\n- Entries into known.txt (the known words file)\n- Entries into unknown.txt (the known words file)\n\nWhat will not be erased:\n- source.txt (the file with the list of words to study)\n\nARE YOU SURE YOU WOULD LIKE TO ERASE THE FILES SPECIFIED ABOVE?" buttons {{"No, keep them", "Yes, erase them"}} default button "Yes, erase them"'
    '''
    user_response_bytes = subprocess.check_output(command, shell=True) # Run the command and capture output
    user_response = user_response_bytes.decode('utf-8') # Format output to regular string

    # Extract the relevant parts of the response
    user_response = user_response[16:] # Get rid of the 'button pressed' part
    user_response = user_response[0:-1] # Get rid of the new line

    if user_response == 'Yes, erase them':
            # Erase unknown words
            with open('unknown.txt', 'w') as erasing_file_1: # Use overwrite mode
                erasing_file_1.write('') # Write nothing
                erasing_file_1.close()
            # Erase known words
            with open('known.txt', 'w') as erasing_file_2:
                erasing_file_2.write('')
                erasing_file_2.close()
    else:
        main_menu()
            
def flashcard_mode():
    # Ask how many vocab words to review
    command_cycles = '''
    osascript -e 'display dialog "How many words would you like to review?" default answer "15" buttons {"Start!"} default button "Start!"'
    '''

    user_response_bytes = subprocess.check_output(command_cycles, shell=True) # Run the command and capture output
    user_response = user_response_bytes.decode('utf-8') # Format output to regular string
    times_to_run = int(user_response[38:-1]) # Crop output to number part only

    # Initialize score
    known = 0

    # Run the mainloop the number times the user asked for
    for _ in range(times_to_run):
        result = mainloop((_ + 1) , times_to_run)
        # Ad
        if result is True:
            known += 1

    # Calculate score
    score = round(((known / times_to_run) * 100), 1)

    # When loop is done, say goodbye and show score
    bye_command = f'''
    osascript -e 'display dialog "👍🏻 Great job today! See you later!\n\n🥇 Score: {score}%" buttons {{"Goodbye!"}} default button "Goodbye!"'
    '''
    os.system(bye_command) # Run the command

def main_menu():    
    command = f'''
    osascript -e 'display dialog "Main Menu: Welcome! What would you like to do?" buttons {{"🔁 Erase and reset", "📖 Start flashcards"}} default button "📖 Start flashcards"'
    '''
    user_response_bytes = subprocess.check_output(command, shell=True) # Run the command and capture output
    user_response = user_response_bytes.decode('utf-8') # Format output to regular string

    # Extract the relevant parts of the response
    user_response = user_response[16:] # Get rid of the 'button pressed' part
    user_response = user_response[0:-1] # Get rid of the new line

    if user_response == '🔁 Erase and reset':
        reset_mode()
    else:
        flashcard_mode()

## Start of execution flow
if __name__ == '__main__':
    main_menu()