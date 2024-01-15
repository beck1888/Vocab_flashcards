## Imports
import random # For picking a random line
import subprocess # For GUI w/ input capture
import os # For GUI w/o input capture
import sys # For neat exits


# Helper functions
def word_known(word):
    with open('known.txt', 'a') as file_2:
        file_2.write(f"{word}\n")
        file_2.close()

def word_unknown(word):
    with open('unknown.txt', 'a') as file_2:
        file_2.write(f"{word}\n")
        file_2.close()


## GUI Defs
def ask_if_known_word(word):
    command = f'''
    osascript -e 'display dialog "Do you know this word: {word}" buttons {{"🚫 No", "✅ Yes"}}'
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
def mainloop():
    line_number = random.randint(1, 10000) # Pick a line number within the file range
    with open('english_words.txt', 'r') as file: # Open the words file
        for current_line, line in enumerate(file, start=1): # Go down line by line
            if current_line == line_number: # When the random line is reached
                word = line.strip() # Get the line cleanly
                word = word.upper() # Makes the word uppercase for better readability
                ask_if_known_word(word) # Ask if word is known

    # mainloop() # Recursion call for repeating the word ask process

    # print(f"At line {line_number} I saw {word}")

## Code call

# Ask how many vocab words to review
command_cycles = '''
osascript -e 'display dialog "How many words would you like to review?" default answer "10" buttons {"Start!"} default button "Start!"'
'''

user_response_bytes = subprocess.check_output(command_cycles, shell=True) # Run the command and capture output
user_response = user_response_bytes.decode('utf-8') # Format output to regular string
times_to_run = int(user_response[38:-1]) # Crop output to number part only


# Initialize score
known = 0

# Run the mainloop the number times the user asked for
for _ in range(times_to_run):
    result = mainloop()
    # Ad
    if result is True:
        known += 1

# Build score
score = round(known / times_to_run)


# When loop is done, say goodbye
bye_command = f'''
osascript -e 'display dialog "Great job today! See you later!\n\nScore: {score}%" buttons {{"Goodbye!"}} default button "Goodbye!"'
'''
os.system(bye_command) # Run the command
# print("Good-bye!")
exit()