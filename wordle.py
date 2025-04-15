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
    # For letters in the correct position:
    for _, letter in guess_in_right_place:
        letter_status[letter] = "in_right_place"

    # For letters in the word, but not in the right position
    for _, letter in guess_in_wrong_place:
        if letter_status[letter] != "in_right_place":
            letter_status[letter] = "in_wrong_place"

    # For letters not in the word at all
    for letter in guess_not_in_word:
        if letter_status[letter] == "not_guessed":
            letter_status[letter] = "not_in_word"


def wordle_feedback_for_guess(guess: str, solution: str):
    """
    Wordle logic with index-aware feedback:
      - Returns:
          in_right_place: List of (index, letter) tuples where letter is correct and in correct place.
          in_wrong_place: List of (index, letter) tuples where letter is correct but in wrong place.
          not_in_word: List of letters not in the solution.
    """
    guess = guess.upper()
    solution = solution.upper()
    sol_chars = list(solution)

    in_right_place = []
    in_wrong_place = []
    not_in_word_set = set()

    # Track used letters in solution to avoid reusing them
    used = [False] * 5

    # First pass: check for letters in the right place
    for i in range(5):
        if guess[i] == sol_chars[i]:
            in_right_place.append((i, guess[i]))
            used[i] = True

    # Second pass: check for correct letters in the wrong place
    for i in range(5):
        if guess[i] == sol_chars[i]:
            continue  # Already matched
        found = False
        for j in range(5):
            if not used[j] and guess[i] == sol_chars[j]:
                in_wrong_place.append((i, guess[i]))
                used[j] = True
                found = True
                break
        if not found:
            not_in_word_set.add(guess[i])

    return in_right_place, in_wrong_place, sorted(list(not_in_word_set))


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