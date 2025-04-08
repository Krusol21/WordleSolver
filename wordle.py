"""
A simple Wordle emulator in Python.
You can manually set the SECRET_WORD to define what the answer should be.
"""
import string
from word_lists import get_target
from word_lists import is_valid_guess
SECRET_WORD = get_target()

def initialize_letter_status():
    """
    Create a dictionary mapping 'A'..'Z' to "not_guessed".
    """
    return {ch: "not_guessed" for ch in string.ascii_uppercase}

def update_letter_status_for_guess(
    guess_in_right_place, guess_in_wrong_place, guess_not_in_word, letter_status
):
    """
    Given three lists of letters for the *current guess*:
      guess_in_right_place, guess_in_wrong_place, guess_not_in_word
    plus the global letter_status dict, update letter_status as follows:
      - if a letter is in_right_place now, set status to "in_right_place" (highest priority).
      - else if a letter is in_wrong_place now, set status to "in_wrong_place" only if it
        isn't already "in_right_place".
      - else if a letter is not_in_word, set status to "not_in_word" only if it isn't
        already "in_wrong_place" or "in_right_place".
    This ensures that once we discover a letter is definitely in the correct place, that
    knowledge doesn't get overwritten by subsequent guesses. Similarly for other statuses.
    """
    # For letters in the correct position:
    for letter in guess_in_right_place:
        letter_status[letter] = "in_right_place"

    # For letters in the word, but not in the right position
    for letter in guess_in_wrong_place:
        # Only update if we haven't discovered a better status
        if letter_status[letter] != "in_right_place":
            letter_status[letter] = "in_wrong_place"

    # For letters not in the word at all
    for letter in guess_not_in_word:
        # Only update if we haven't discovered it's in the word
        if letter_status[letter] == "not_guessed":
            letter_status[letter] = "not_in_word"

def wordle_feedback_for_guess(guess: str, solution: str):
    """
    Standard Wordle-like logic for a single guess:
      - We do a two-pass approach to handle duplicate letters.
      - Return three lists of letters from this guess:
          in_right_place, in_wrong_place, not_in_word.
      - Duplicates are handled so a letter won't appear multiple times in the same list.
    """
    guess = guess.upper()
    solution = solution.upper()
    sol_chars = list(solution)

    in_right_place_set = set()
    in_wrong_place_set = set()
    not_in_word_set = set()

    # 1st pass: exact matches
    for i in range(5):
        if guess[i] == sol_chars[i]:
            in_right_place_set.add(guess[i])
            sol_chars[i] = None  # Mark used

    # 2nd pass: letters in the solution but in different positions
    for i in range(5):
        if guess[i] == solution[i]:
            continue
        letter = guess[i]
        if letter in sol_chars:
            in_wrong_place_set.add(letter)
            idx = sol_chars.index(letter)
            sol_chars[idx] = None  # Use up one occurrence
        else:
            not_in_word_set.add(letter)

    # Convert to sorted lists
    in_right_place = sorted(in_right_place_set)
    in_wrong_place = sorted(in_wrong_place_set)
    not_in_word = sorted(not_in_word_set)

    return in_right_place, in_wrong_place, not_in_word

def categorize_global(letter_status):
    """
    Based on the global letter_status dictionary, produce four sets:
      in_right_place, in_wrong_place, not_in_word, not_guessed
    Then convert them to sorted lists so we can display them.
    """
    in_right_place_set = set()
    in_wrong_place_set = set()
    not_in_word_set = set()
    not_guessed_set = set()

    for letter, status in letter_status.items():
        if status == "in_right_place":
            in_right_place_set.add(letter)
        elif status == "in_wrong_place":
            in_wrong_place_set.add(letter)
        elif status == "not_in_word":
            not_in_word_set.add(letter)
        else:
            # "not_guessed"
            not_guessed_set.add(letter)

    return (
        sorted(list(in_right_place_set)),
        sorted(list(in_wrong_place_set)),
        sorted(list(not_in_word_set)),
        sorted(list(not_guessed_set))
    )

def play_wordle_persistent():
    print("Welcome to the Wordle Emulator with Persistent Letter Tracking!")
    print(f"SECRET_WORD is set to: {SECRET_WORD} (for testing).")
    print("Up to 6 attempts.\n")

    # Initialize the global letter status dict
    letter_status = initialize_letter_status()

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
        guess_in_right_place, guess_in_wrong_place, guess_not_in_word = wordle_feedback_for_guess(
            guess, SECRET_WORD
        )

        # Step 2: Update the global letter_status
        update_letter_status_for_guess(
            guess_in_right_place,
            guess_in_wrong_place,
            guess_not_in_word,
            letter_status
        )

        # Step 3: Recompute the global categories
        (global_in_right_place,
         global_in_wrong_place,
         global_not_in_word,
         global_not_guessed) = categorize_global(letter_status)

        # Display the single-guess feedback (optional if you want to see it)
        print(f"\nThis guess: {guess}")
        print(" in_right_place (this guess):", guess_in_right_place)
        print(" in_wrong_place (this guess):", guess_in_wrong_place)
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