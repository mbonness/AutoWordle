import bs4, subprocess, textMyself, time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Wordle playing automaton
# can be used to maintain your wordle streak while on vacation

def read_from_clipboard():
    return subprocess.check_output(
        'pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')

class SolutionsList:
    def __init__(self):
        # read word list from file
        # 3/31 switch from 2k to 12k dictionary because of new words
        # added by NYT editor
        f = open("wordle-all_2022-02-15.txt", "r")
        self.__wordlist = f.readlines()

    def getwordlist(self):
        return self.__wordlist

class PreviousSolutions:
    def __init__(self):
        self.__pastanswers = []

        # download previous solutions
        browser.get("https://www.rockpapershotgun.com/wordle-past-answers")
        html = browser.page_source
        answersoup = bs4.BeautifulSoup(html, 'html.parser')

        # parse the "all wordle answers" list
        answerlinks = answersoup.select('ul.inline li')
        for answerlink in answerlinks[1:]:
            self.__pastanswers.append(answerlink.text)

    def getprevioussolutions(self):
        return self.__pastanswers

class LetterRanker:
    def __init__(self, wordlist):
        self.__charsCountDict = {}
        for word in wordlist:
            word = word[:5] # strip newlines
            # get letters in word
            chars = list(word)
            charsDict = {}
            for char in chars:
                charsDict[char] = char
            uniqueChars = charsDict.keys()
            for uniqueChar in uniqueChars:
                if uniqueChar in self.__charsCountDict:
                    charCount = self.__charsCountDict[uniqueChar]
                    self.__charsCountDict[uniqueChar] = charCount + 1
                else:
                    self.__charsCountDict[uniqueChar] = 1

    def getlettersranked(self):
        sorted_letters = sorted(self.__charsCountDict.items(), key=lambda kv: kv[1])
        return sorted_letters[::-1]

class WordRanker:
    def __init__(self, wordlist, charsRanked):
        charsRankedDict = dict(charsRanked)
        self.__wordsRankedDict = {}
        for word in wordlist:
            word = word[:5] # strip newlines
            wordScore = 0
            # get letters in word
            chars = list(word)
            charsDict = {}
            for char in chars:
                charsDict[char] = char
            uniqueChars = charsDict.keys()
            for uniqueChar in uniqueChars:
                # get score for letter
                charScore = charsRankedDict[uniqueChar]
                wordScore = wordScore + charScore
            self.__wordsRankedDict[word] = wordScore

    def getwordsranked(self):
        sortedwords = sorted(self.__wordsRankedDict.items(), key=lambda kv: kv[1])
        return sortedwords[::-1]

class RemainingSolutions:
    def __init__(self, guess, cubes, remainingWordsRanked):
        guessletters = list(guess)
        wordstoremove = []
        for cube in cubes:
            #print(cube)
            if cube.getcolor() == 'black':
                for remainingword in remainingWordsRanked:
                    if cube.getletter() in remainingword[0] and self.nogreencubeshaveletter(cube.getletter(), cubes):
                        #print("remaining word " + remainingword[0] + " has black letter " + cube.getletter() + ", removing")
                        wordstoremove.append(remainingword)
            elif cube.getcolor() == 'yellow':
                for remainingword in remainingWordsRanked:
                    # for yellow letters, remove if not in word or in the same position
                    if cube.getletter() not in remainingword[0]:
                        wordstoremove.append(remainingword)
                    if cube.getletter() == remainingword[0][cube.getposition()-1]:
                        wordstoremove.append(remainingword)
            elif cube.getcolor() == 'green':
                for remainingword in remainingWordsRanked:
                    if cube.getletter() != remainingword[0][cube.getposition()-1]:
                        wordstoremove.append(remainingword)

        self.__updatedremainingwords = []
        for remainingword in remainingWordsRanked:
            wordistoberemoved = False
            for wordtoremove in wordstoremove:
                if wordtoremove[0] == remainingword[0] or guess == remainingword[0]:
                    wordistoberemoved = True
            if not wordistoberemoved:
                self.__updatedremainingwords.append(remainingword)

    def nogreencubeshaveletter(self, letter, cubes):
        for cube in cubes:
            if cube.getcolor() == 'green' and cube.getletter() == letter:
                return False
        return True

    def getremainingsolutions(self):
        return self.__updatedremainingwords

class Cube:
    def __init__(self, color, letter, position):
        self.__color = color
        self.__letter = letter
        self.__position = position

    def __str__(self):
        return "Cube(color=" + self.__color + ", letter=" + self.__letter + ", position=" + str(self.__position) + ")"

    def getcolor(self):
        return self.__color

    def getletter(self):
        return self.__letter

    def getposition(self):
        return self.__position

print()
print("Welcome to AutoWordle v1.0!")
print()

print("Loading list of all Wordle words...")
solutions = SolutionsList()
wordlist = solutions.getwordlist()

letterRanker = LetterRanker(wordlist)
charsRanked = letterRanker.getlettersranked()
#print(charsRanked)

print("Ranking words by letter popularity...")
wordRanker = WordRanker(wordlist, charsRanked)
wordsRanked = wordRanker.getwordsranked()

print("Loading previous answers...")
chrome_options = Options()
chrome_options.add_argument("user-data-dir=selenium8")
browser = webdriver.Chrome(executable_path='/Users/matt/Documents/wordle/chromedriver',options=chrome_options)
previousSolutions = PreviousSolutions()
pastanswers = previousSolutions.getprevioussolutions()
#print(pastanswers)
print()

# remove previous answers from the ranked words list
wordsToRemove = []
for word in wordsRanked:
    for pastanswer in pastanswers:
        if pastanswer == word[0].upper() and word not in wordsToRemove:
            wordsToRemove.append(word)

for wordToRemove in wordsToRemove:
    #print("removing word " + wordToRemove[0])
    if wordToRemove in wordsRanked:
        wordsRanked.remove(wordToRemove)

# now let's go to NYT wordle and solve today's puzzle
browser.get("https://www.nytimes.com/games/wordle/index.html")

done = False
tries = 1
while not done and tries <= 6:
    # type in our best guess
    print(str(len(wordsRanked)) + " solutions remaining")
    print("Playing this word:")
    wordToPlay = wordsRanked[0][0]
    print(wordToPlay.upper())
    print()
    htmlElem = browser.find_element(By.TAG_NAME, 'html')
    htmlElem.send_keys(wordToPlay)
    htmlElem.send_keys(Keys.ENTER)

    # now let's check the greens and yellows
    print("Waiting for cubes to flip over...")
    time.sleep(3)
    print("Checking cubes...")
    html = browser.page_source
    puzzlesoup = bs4.BeautifulSoup(html, 'html.parser')
    currentRowDiv = puzzlesoup.select_one("#wordle-app-game > div.Board-module_boardContainer__TBHNL > div > div:nth-child(" + str(tries) + ")")
    if (currentRowDiv is None):
        print("Could not find rows in puzzle")
        input("Press ENTER to continue")
        done = True
        continue
    cubeDivs = currentRowDiv.select("div.Tile-module_tile__UWEHN")
    cubes = []
    cubesAreAllGreen = True
    for idx, cubeDiv in enumerate(cubeDivs):
        dataState = cubeDiv['data-state']
        print("Cube data state is: " + dataState)
        #cube data states are: absent, present, correct
        guessletters = list(wordToPlay)
        if (dataState == 'absent'):
            cubes.append(Cube("black", guessletters[idx], idx+1))
            cubesAreAllGreen = False
        elif (dataState == 'present'):
            cubes.append(Cube("yellow", guessletters[idx], idx+1))
            cubesAreAllGreen = False
        elif (dataState == 'correct'):
            cubes.append(Cube("green", guessletters[idx], idx+1))
        else:
            print("Unexpected data state")
            input("Press ENTER to continue")
            done = True
            continue

    # check if puzzle is solved
    if (cubesAreAllGreen):
        print("Puzzle solved, we're done")
        done = True
        continue

    # puzzle is not solved, keep going
    print("Calculating remaining solutions...")
    remainingSolutions = RemainingSolutions(wordToPlay, cubes, wordsRanked)
    updatedremainingsolutions = remainingSolutions.getremainingsolutions()
    wordsRanked = updatedremainingsolutions
    if (len(wordsRanked) == 0):
        print("No solutions found, aborting")
        done = True
        continue
    tries = tries + 1

print("Waiting for stats popup...")
time.sleep(3)

print("Clicking share button...")
try:
    shareButton = browser.find_element(By.XPATH, "//button[@type='button']/span[.='Share']")
    shareButton.click()
except NoSuchElementException:
    print("Could not find Share button")

cliptext = read_from_clipboard()
print("Clipboard text = " + cliptext)
print("Texting wordle score to myself...")
textMyself.textmyself("AutoWordle 1.0\n" + cliptext)

# clean up and exit
print("Have a nice day")
browser.quit()