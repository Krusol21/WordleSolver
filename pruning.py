

# this method prunes the list of possible words from the guess that has been made
# guess - (string) word used to get
# currentWordList - (array) list of words still possible originating from the text file
# guessColor - (string) five letter word containing characters "g" for green, "y" for yellow, and "b" for gray/black
def wordlePrune(guess, currentWordList, guessColors):

    possible_word = [' ']*5
    for index, char in enumerate(guess):
        if guessColors[index] == 'g': 
            possible_word[index] = char
    #print(possible_word)
    #so far, this is the possible word after checking green

    not_possible_letters = [set() for _ in range(5)]
    for index, char in enumerate(guess):
        if guessColors[index] == 'b':  
            not_possible_letters[index].add(char)
    #print(not_possible_letters)
    #get the gray letters and their indexes

    yellow_letters = [set() for _ in range(5)]
    for index, char in enumerate(guess):
        if guessColors[index] == 'y':  
            yellow_letters[index].add(char)
    #print(yellow_letters)
    #gets the yellows


    #start pruning process
    newWordList = []
    for word in currentWordList:
        validword = True
        for index, char in enumerate(word):
            if not validword:
                break
            
            if guessColors[index] == 'g': 
                if word[index] != possible_word[index]:
                    validword = False
            
            if guessColors[index] == 'b': 
                if word[index] in not_possible_letters[index]:
                    validword = False
            
            if guessColors[index] == 'y': 
                if word[index] == possible_word[index] or word[index] not in guess:
                    validword = False
        
        if validword:
            newWordList.append(word)


    return newWordList





def load_words(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]


