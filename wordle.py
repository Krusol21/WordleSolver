"""
A simple Wordle emulator in Python.
You can manually set the SECRET_WORD to define what the answer should be.
"""
import string
from word_lists import get_target
from word_lists import is_valid_guess
from pruning import wordlePrune, infoPrune

SECRET_WORD = get_target()

def initialize_letter_status():
    """
    Creates a dict of all letters
    """
    # ─── initialization ───────────────────────────────────────────────
    return {
        ch: {"state": "not_guessed",
            "green": set(),           # positions confirmed green
            "yellow": set()}          # positions where it is NOT allowed
        for ch in string.ascii_uppercase
    }



def wordle_feedback_for_guess(guess: str, solution: str):
    """
    Evaluate one Wordle guess.

    Returns
    -------
    in_right_place : list[(idx, letter)]
    in_wrong_place : list[(idx, letter)]
    not_in_word    : list[letter]               # sorted, no dups
    guess_colors   : str                        # e.g. "GGBYB"
        For each index i:
            G → green  (correct letter, correct spot)
            Y → yellow (correct letter, wrong spot)
            B → black/gray (letter not in word)
    written with assistance of ChatGPT-o3
    """
    guess = guess.upper()
    solution = solution.upper()
    colors = ["B"] * 5                # default everything to gray/black
    sol_chars = list(solution)
    used      = [False] * 5           # which letters of solution already matched


    in_right_place = []
    in_wrong_place = []
    not_in_word_set = set()

    # Track used letters in solution to avoid reusing them
    used = [False] * 5

    # Pass 1 – exact matches → GREEN
    for i in range(5):
        if guess[i] == sol_chars[i]:
            colors[i] = "G"
            in_right_place.append((i, guess[i]))
            used[i] = True

    # Pass 2 – wrong‑place matches → YELLOW or still B
    for i in range(5):
        if colors[i] == "G":
            continue                  # already handled
        found = False
        for j in range(5):
            if not used[j] and guess[i] == sol_chars[j]:
                # letter exists elsewhere and not consumed yet
                colors[i] = "Y"
                in_wrong_place.append((i, guess[i]))
                used[j] = True
                found = True
                break
        if not found:
            not_in_word_set.add(guess[i])

    return (
        in_right_place,
        in_wrong_place,
        sorted(not_in_word_set),
        "".join(colors),
    )


def categorize_global(letter_status):
    greens, yellows, grays, untried = [], [], [], []

    for L, entry in letter_status.items():
        st    = entry["state"]
        green = sorted(entry["green"])
        yel   = sorted(entry["yellow"])

        if st == "in_right_place":
            greens.append((L, green))      # list indices that ARE green
        elif st == "in_wrong_place":
            yellows.append((L, yel))       # list indices that CANNOT be yellow
        elif st == "not_in_word":
            grays.append(L)
        else:
            untried.append(L)

    greens.sort(key=lambda t: t[0])
    yellows.sort(key=lambda t: t[0])
    grays.sort()
    untried.sort()
    return greens, yellows, grays, untried



def play_wordle_persistent():
    #ChatGPT-o1
    print("Welcome to the Wordle Emulator!")
    # print(f"SECRET_WORD is set to: {SECRET_WORD} (for testing).")
    print("Up to 6 attempts.\n")

    # Initialize the global letter status dict
    letter_status = initialize_letter_status()

    # Initialize the pruning list for pruning.py (can be changed for multiple pruning algorithms)
    with open('wordle_targets.txt', 'r') as file:
        targets = file.readlines()
        targets = [target.strip().upper() for target in targets]
    with open('wordle_possibles.txt', 'r') as file1:
        possibles = file1.readlines()
        possibles = [possible.strip().upper() for possible in possibles]
    

    # solutions_list = targets.copy()
    solutions_list = possibles + targets
    information_list = possibles + targets

    max_guesses = 6
    for attempt in range(1, max_guesses + 1):
        guess = input(f"Guess #{attempt}: ").strip().upper()
        while (len(guess) != 5
        or not guess.isalpha()
        or not is_valid_guess(guess)):
            print("Invalid guess. Please enter exactly 5 letters (A-Z).")
            guess = input(f"Guess #{attempt}: ").strip().upper()

        # For each letter in this guess, if we haven't used it yet, set it to not_in_word
        # but we override that logic with the actual feedback below. (Optional step)
        # For now, we won't force that logic, since we'll see the real feedback anyway.

        # Step 1: Get single-guess feedback
        (
            guess_in_right_place,
            guess_in_wrong_place,
            guess_not_in_word,
            guess_colors,
        ) = wordle_feedback_for_guess(guess, SECRET_WORD)

        print(guess_colors)

        # run pruning algorithm and print result of len of list
        solutions_list = wordlePrune(guess, solutions_list, guess_colors)
        print("Length of Viable Solutions List:")
        print(len(solutions_list))
        print("Viable Solutions List:")
        print(solutions_list)

        # run pruning algorithm and print result of len of list
        information_list = infoPrune(guess, information_list, guess_colors)
        print("Length of Info Words List:")
        print(len(information_list))
        print("Info Words List:")
        print(information_list)


        # Step 2: Update the global letter_status
        # GREENS
        for idx, L in guess_in_right_place:
            letter_status[L]["state"] = "in_right_place"
            letter_status[L]["green"].add(idx)           # confirmed position

        # YELLOWS
        for idx, L in guess_in_wrong_place:
            letter_status[L]["yellow"].add(idx)          # cannot be here
            if letter_status[L]["state"] != "in_right_place":
                letter_status[L]["state"] = "in_wrong_place"

        # GRAYS (unchanged)
        for L in guess_not_in_word:
            if letter_status[L]["state"] == "not_guessed":
                letter_status[L]["state"] = "not_in_word"



        # Step 3: Recompute the global categories
        (global_in_right_place,
         global_in_wrong_place,
         global_not_in_word,
         global_not_guessed) = categorize_global(letter_status)
        

        #-----------------------PRINT BLANKS----------------------
        pattern = ["_"] * 5           # start with all blanks

        # place confirmed greens
        for letter, pos_list in global_in_right_place:      # e.g. [('E',[1]), ('N',[3])]
            for p in pos_list:
                pattern[p] = letter

        # positions that are NOT green but have at least one yellow ⇒ “?”
        for letter, pos_list in global_in_wrong_place:      # e.g. [('I',[2,4])]
            for p in pos_list:
                if pattern[p] == "_":                       # don’t overwrite a green
                    pattern[p] = "?"

        print("Known pattern so far :", "".join(pattern))   # e.g.  _E?__

        # Display the single-guess feedback (optional if you want to see it)
        print(f"\nThis guess: {guess}")
        print(" in_right_place (this guess):", [(i, ch) for i, ch in guess_in_right_place])
        print(" in_wrong_place (this guess):", [(i, ch) for i, ch in guess_in_wrong_place])
        print(" not_in_word    (this guess):", guess_not_in_word, "\n")

        # Display the persistent categories across all guesses so far
        print("==> GLOBAL KNOWN STATUS ACROSS GUESSES <==")
        print(" in_right_place:", global_in_right_place)
        print(" in_wrong_place:", global_in_wrong_place)
        print(" not_in_word:   ", global_not_in_word)
        print(" not_guessed:   ", global_not_guessed)
        print()

        # Check if guess is exactly correct
        if guess == SECRET_WORD:
            print(f"Congratulations! You guessed '{SECRET_WORD}' in {attempt} tries!")
            return

    print(f"Out of attempts! The secret word was '{SECRET_WORD}'.")

if __name__ == "__main__":
    play_wordle_persistent()