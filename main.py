import re
import json
import random

def init():
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

def search(filtered_keys:list[str], **kwargs) -> tuple[str, str, list[str]]:
    
        
    print("Type words in the following format: --x-x")
    print("Example, searching for 'blunt' the word 'plant' would yield: -l-nt")
    running = True
    st_try = "-----"
    while running:
        st_try = input("Please type the correct letters of your first guess (if any): ")
        if(len(st_try) == 5):
            running = False
    for el in kwargs.keys():
        if el == 'toDelete':
            theTuple = list(kwargs['toDelete'])
            theTuple[1] = st_try
            filtered_keys = deleter(tuple(theTuple), filtered_keys)

    print("Searching for matches...")
    matcher = st_try.replace('-', '[a-z]{1}')
    possible_matches = []
    for el in filtered_keys:
        possible_matches += re.findall(matcher, el)
    if(len(possible_matches) > 1):
        elchoice = possible_matches[random.randint(0, len(possible_matches)-1)]
    else: elchoice = possible_matches[0]
    print(f"Try: {elchoice}")
    return (elchoice, st_try, filtered_keys)

def deleter(theTuple:tuple, words:list) -> list:
    toRemovePattern = []
    word_tried = theTuple[0]
    pattern = theTuple[1]
    L = re.findall("-", pattern)
    for i in range(len(L)):
        L[i] = pattern
    for i in range(len(L)):
        newList = list(pattern)
        r = 0
        num = 0
        for char in pattern:
            if char == "-":
                if(r != i):
                    newList[num] = "[a-z]{1}"
                else:
                    newList[num] = word_tried[num]
                r += 1
            num += 1
        newString = ""
        for el in newList:
            newString += el
        toRemovePattern.append(newString)
    words = list(words)
    print(len(words))
    toRemove = []
    for patt in toRemovePattern:
        for el in words:
            werd = re.findall(patt, el)
            if(len(werd) > 0):
                toRemove += werd
    for el in toRemove:
        try:
            words.remove(el)
        except Exception:
            pass
    print(len(words))
    return words


def main():
    init()
    running = True
    filtered_keys = filtered_words.keys()
    filtered_keys = list(filtered_keys)
    theTuple = search(filtered_keys)
    i = 0
    while running:
        i += 1
        ch = input('Did that work ? (y/n/ne)')
        if ch == 'y':
            running = False
            print(f"Yay! Found word successfully in \033[7m{i}\033[0m tries, word was: \033[7m{theTuple[0]}\033[0m")
        elif ch == 'ne':
            i -=1
            print(len(theTuple[2]))
            theTuple[2].remove(theTuple[0])
            print(len(theTuple[2]))
            theTuple = search(theTuple[2])
        else:
            theTuple = search(theTuple[2] ,toDelete=theTuple)

def deepCopy(liste:list) -> list:
    newList = []
    for el in liste:
        newList.append(el)
    return newList

if __name__ == '__main__':
    main()