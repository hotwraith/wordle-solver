import re
import json
import random

def main() -> None:
    filtered_keys = init()
    running = True
    i = 0
    while running:
        i += 1
        inputs = takeInput()
        word = inputs[0]
        pattern = inputs[1]
        deletePatterns = createDeletePatterns(word, pattern)
        filtered_keys = deleter(deletePatterns, filtered_keys)
        searchPattern = createSearchPatterns(word, pattern)
        interesting_stuff = searchValid(filtered_keys, searchPattern)
        print(f"Found {len(interesting_stuff)} relevent words, {round(1/len(interesting_stuff), 3)*100}% of success")
        filtered_keys = result(interesting_stuff, filtered_keys)
        if(len(filtered_keys) == 0):
            running = False
            print(f"Took \033[7m{i}\033[0m tries")
            input("Press ENTER to continue...")
    

def result(interestingList:list[str], allWords:list[str]):
    running = True
    while running:
        if(len(interestingList) > 0):
            if(len(interestingList) > 1):
                chosenWord = interestingList[random.randint(0, len(interestingList)-1)]
            else:
                chosenWord = interestingList[0]
        else: 
            chosenWord = ''
            print("No matching words sorry !")
        if(len(chosenWord) == 5):
            print(chosenWord)
            choice = input("Worked ? (y/n/ne): ")
            if(choice == 'y'):
                running = False
                allWords = []
                print(f"Word was: \033[7m{chosenWord}\033[0m")
            elif(choice == 'ne'):
                allWords = deleter([chosenWord], allWords)
                interestingList.remove(chosenWord)
            elif(choice == 'n'):
                allWords = deleter([chosenWord], allWords)
                running = False
    return allWords

def init() -> list:
    with open("data/words_dictionary.json", 'r') as f:
        global filtered_words
        filtered_words = json.load(f)
        print(f"Total number of words: {len(filtered_words)}")
        f.close()

    original_keys = filtered_words.keys()
    to_filter = []
    for el in original_keys:
        if(len(el) != 5):
            to_filter.append(el)

    for el in to_filter:
        filtered_words.pop(el)

    print(f"Isolated {len(filtered_words)} 5 letters words")
    return list(filtered_words.keys())

def createDeletePatterns(word:str, ptr:str) -> list[str]:
    patternsForDelete = []
    patternsToSave = []
    for i in range(len(ptr)):
        char = ptr[i]
        if char == '-':
            if ptr.count(word[i]) > 0 or ptr.count(word[i].capitalize()) > 0:
                newStr = ''
                for j in range(len(ptr)):
                    if(j == i):
                        newStr += char
                    else:
                        newStr += '[a-z]{1}'
            else:
                patternsForDelete.append(word[i])

        elif char.capitalize() == char:
            newStr = ''
            newPtr = list('-----')
            newPtr[i] = char.lower()
            for z in newPtr:
                newStr += z
            newStr = newStr.replace('-', '[a-z]{1}')
            patternsForDelete.append(newStr)
        '''
        elif char.lower() == char:
            newPtr = ptr.replace('-', '[a-z]{1}')
            patternsForDelete.append(newPtr)
        '''
    if(ptr.count('-') > 1):
        return patternsForDelete
    else: return []

def deleter(patterns:list[str], allWords:list[str]) -> list[str]:
    toDelete = []
    #print(len(allWords))
    for el in patterns:
        for word in allWords:
            yes = re.findall(el, word)
            if len(yes) > 0:
                toDelete.append(word)
    
    for el in toDelete:
        try:
            allWords.remove(el)
        except Exception:
            pass
    #print(len(allWords))
    return allWords

def createSearchPatterns(word:str, ptr:str):
    pater = list(ptr)
    for i in range(len(pater)):
        char = pater[i]
        if char.capitalize() == char:
            pater[i] = '-'

    ptr = ""
    for char in pater:
        ptr += char
    return ptr.replace('-', '[a-z]{1}')
        
def takeInput() -> list:
    running = True
    word, pattern = '', ''
    while running:
        word = input("Dernier mot mis: ")
        pattern = input("Dernier pattern: ")
        if(len(word) == 5 and len(pattern) == 5):
            running = False
    
    return [word, pattern]

def searchValid(words:list, pattern:str):
    interestingWords = []
    for el in words:
        yes = re.findall(pattern, el)
        if len(yes) > 0:
            interestingWords += yes
    return interestingWords

if __name__ == '__main__':
    running = True
    while running:
        main()
        choice = input("Another one ? y/n ")
        if choice != 'y':
            running = False