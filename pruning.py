

# this method prunes the list of possible words from the guess that has been made
# guess - (string) word used to get
# currentWordList - (array) list of words still possible originating from the text file
# guessColor - (string) five letter word containing characters "g" for green, "y" for yellow, and "b" for gray/black
def wordlePrune(guess, currentWordList, guessColors):

    possible_word = [' ']*5
    for index, char in enumerate(guess):
        if guessColors[index] == 'G': 
            possible_word[index] = char
    #print(possible_word)
    #so far, this is the possible word after checking green

    not_possible_letters = [set() for _ in range(5)]
    for index, char in enumerate(guess):
        if guessColors[index] == 'B':  
            not_possible_letters[index].add(char)
    #print(not_possible_letters)
    #get the gray letters and their indexes

    yellow_letters = [set() for _ in range(5)]
    for index, char in enumerate(guess):
        if guessColors[index] == 'Y':  
            yellow_letters[index].add(char)
    #print(yellow_letters)
    #gets the yellows

    #start pruning process
    newWordList = []
    greens  = [c for c, g in zip(guess, guessColors) if g == "G"]
    yellows = [c for c, g in zip(guess, guessColors) if g == "Y"]
    greys   = [c for c, g in zip(guess, guessColors) if g == "B"]

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

        # 2. Grey letters cannot appear anywhere (unless that letter was also G/Y)
        for ch in greys:
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





def load_words(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]


