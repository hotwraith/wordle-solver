import re
import json
import random
import threading

class StoppableThread(threading.Thread): #note: this is unused but funny
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

class ProgressBar():

    def __init__(self) -> None:
        self.task = ''
        self.progress = 0

    def printPercentBar(self) -> None:
        percentage = "["
        for j in range(1, round(self.progress)+1):
            if(j%10 == 0):
                percentage += "█"
        for j in range(len(percentage), 11):
            percentage += "▒"
        percentage += f'] {round(self.progress, 1)}%'
        percentage = self.task +': ' +percentage
        print(percentage, end='\r')
    
    def updateProgress(self, update:float) -> None:
        self.progress += update
        self.printPercentBar()

    def resetProgress(self) -> None:
        self.progress = 0
        #self.printPercentBar()

    def setTask(self, taskName:str) -> None:
        self.task = taskName
        print('')

def main() -> None:
    filtered_keys = init()
    running = True
    i = 0
    while running:
        i += 1
        inputs = takeInput()
        word = inputs[0]
        pattern = inputs[1]
        deletePatterns, lettersToFind = createDeletePatterns(word, pattern)
        filtered_keys = deleter(deletePatterns, filtered_keys)
        searchPattern = createSearchPatterns(word, pattern)
        interesting_stuff = searchValid(filtered_keys, searchPattern, lettersToFind)
        theBar.setTask('')
        if(len(interesting_stuff) > 0):
            print(f"Found {len(interesting_stuff)} relevent words, {round(1/len(interesting_stuff), 3)*100}% of success")
            filtered_keys = result(interesting_stuff, filtered_keys)
        else:
            print("Weird, we didn't find any result, try again ?")
            running = False
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
                allWords = deleter([chosenWord], allWords, update=False)
                interestingList.remove(chosenWord)
            elif(choice == 'n'):
                allWords = deleter([chosenWord], allWords, update=False)
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

def createDeletePatterns(word:str, ptr:str) -> tuple[list[str], list[str]]:
    patternsForDelete = []
    letterstoFind = []
    theBar.setTask('Creating delete patterns')
    for i in range(len(ptr)):
        theBar.updateProgress(1/len(ptr)*100)
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
            letterstoFind.append(char.lower())
        '''
        elif char.lower() == char:
            newPtr = ptr.replace('-', '[a-z]{1}')
            patternsForDelete.append(newPtr)
        '''
    theBar.resetProgress()
    if(ptr.count('-') > 0):
        return (patternsForDelete, letterstoFind)
    else: return ([], [])

def deleter(patterns:list[str], allWords:list[str], **kwargs) -> list[str]:
    barPrint= kwargs.get('update', True)
    toDelete = []
    #print(len(allWords))
    if barPrint: theBar.setTask('Finding all words to remove')
    for el in patterns:
        if barPrint: theBar.updateProgress(1/len(patterns)*100)
        for word in allWords:
            yes = re.findall(el, word)
            if len(yes) > 0:
                toDelete.append(word)
    if barPrint: theBar.resetProgress()
    if barPrint: theBar.setTask('Removing elements')
    for el in toDelete:
        try:
            if barPrint:  theBar.updateProgress(1/len(toDelete)*100)
            allWords.remove(el)
        except Exception:
            pass
    #print(len(allWords))
    if barPrint: theBar.resetProgress()
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

def searchValid(words:list[str], pattern:str, lettersToFind:list[str]):
    interestingWords = []
    secondRound = []
    theBar.setTask('Searching words')
    for el in words:
        theBar.updateProgress(1/len(words)*100)
        yes = re.findall(pattern, el)
        if len(yes) > 0:
            interestingWords += yes
    theBar.resetProgress()
    if(len(lettersToFind) > 0):
        for el in interestingWords:
            i = 0
            for char in lettersToFind:
                i += el.count(char)
            if(i >= len(lettersToFind)):
                secondRound.append(el)
        return secondRound
    else: 
        return interestingWords

if __name__ == '__main__':
    running = True
    while running:
        global theBar
        theBar = ProgressBar()
        #global t1
        #t1 = StoppableThread(target=theBar.printPercentBar)
        #t2 = threading.Thread(target=main)
        #t2.start()
        #t2.join()
        main()
        choice = input("Another one ? y/n ")
        if choice != 'y':
            running = False