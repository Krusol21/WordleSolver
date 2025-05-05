# this method prunes the list of possible words from the guess that has been made
# guess - (string) word used to get
# currentWordList - (array) list of words still possible originating from the text file
# guessColor - (string) five letter word containing characters "g" for green, "y" for yellow, and "b" for gray/black
def wordlePrune(guess, currentWordList, guessColors):
    #start pruning process
    newWordList = []
    greens  = [c for c, g in zip(guess, guessColors) if g == "G"]
    yellows = [c for c, g in zip(guess, guessColors) if g == "Y"]
    grays   = [c for c, g in zip(guess, guessColors) if g == "B"]

    # letters that must appear at least once somewhere (greens+yellows)
    must_have = greens + yellows

    for word in currentWordList:
        valid = True

        # 1. Position checks (greens / yellows)
        for i in range(5):
            g_c = guess[i]
            w_c = word[i]
            color = guessColors[i]

            if color == "G":
                if w_c != g_c:
                    valid = False
                    break
            elif color == "Y":
                if w_c == g_c:          # cannot be in that spot …
                    valid = False
                    break
                if g_c not in word:     # … but must be elsewhere
                    valid = False
                    break

        if not valid:
            continue

        # 2. gray letters cannot appear anywhere (unless that letter was also G/Y)
        # we ban each gray letter unless it appears in the word (double-letter rule)
        for ch in grays:
            if ch not in must_have and ch in word:
                valid = False
                break
        if not valid:
            continue

        # 3. duplicate‑letter count check
        # For each unique letter in the guess, the candidate word must contain
        # at least as many occurrences as the number of G+Y for that letter.
        from collections import Counter
        gcount = Counter([c for c, col in zip(guess, guessColors) if col in "GY"])
        wcount = Counter(word)
        for letter, need in gcount.items():
            if wcount[letter] < need:
                valid = False
                break
        if valid:
            newWordList.append(word)

    return newWordList

def infoPrune(guess, currentWordList, guessColors):
    #start pruning process
    newWordList = []
    greens  = [c for c, g in zip(guess, guessColors) if g == "G"]
    yellows = [c for c, g in zip(guess, guessColors) if g == "Y"]
    grays   = [c for c, g in zip(guess, guessColors) if g == "B"]

    for word in currentWordList:
        if len(set(word)) < 5:          # any repeated char → next word
            continue
        valid = True

        # 1. Position checks (greens / yellows)
        for i in range(5):
            g_c = guess[i]
            w_c = word[i]
            color = guessColors[i]

            # if there is a green character in the word, remove from list
            if color == "G":
                if w_c == g_c:
                    valid = False
                    break
            # if there is a yellow char in word, it can stay if in diff loc
            elif color == "Y":
                if w_c == g_c:          # cannot be in same spot …
                    valid = False
                    break

        if not valid:
            continue

        # 2. forbid all grays outright
        # --- ❷  CHANGE: simpler gray test
        for ch in grays:
            if ch in word:                   # any gray ⇒ reject
                valid = False
                break
        if not valid:
            continue


        if valid:
            newWordList.append(word)

    return newWordList



def load_words(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]


