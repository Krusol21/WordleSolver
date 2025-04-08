import random

#Choose a random word
def get_target():
    with open('wordle_targets.txt', 'r') as file:
        targets = file.readlines()
        targets = [target.strip().upper() for target in targets]
    answer = random.choice(targets)
    return answer

def is_valid_guess(guess):
    with open('wordle_possibles.txt', 'r') as file1:
        possibles = file1.readlines()
        possibles = [possible.strip().upper() for possible in possibles]
    with open('wordle_targets.txt', 'r') as file2:
        targets = file2.readlines()
        targets = [target.strip().upper() for target in targets]
    possibles.extend(targets)
    full_list = set(possibles)
    # print(full_list)
    if (guess in full_list):
        return True
    else:
        return False