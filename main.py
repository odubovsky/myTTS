import os
import pyttsx3
import random
from sys import platform
from pathlib import Path

class randomReader:
    def __init__(self, inputFile):
        self.words = [line.strip() for line in open(inputFile, 'r')]
        self.testArr = {}
        self.testGrade = {}
        self.engine = pyttsx3.init()

        # Alternate voices
        #voices = self.engine.getProperty('voices')
        #self.engine.setProperty('voice', voices[1].id)

    def tts(self, text):
        if (platform == "darwin"):
            # iOS
            os.system("say " + text)
        else:
            # Windows
            self.engine.say(text)
            self.engine.runAndWait()

    def welcome(self, name):
        self.tts('hello ' + name)
        self.tts('How are you?')
        self.tts('...Are you ready for your test?')
        self.tts('Lets begin!...')

    def printWords(self, source):
        print("Total number of words: " + str(len(self.words)))
        if (source == "file"):
            for w in self.words:
                print (w)
        if (source == "test"):
            for w in range(len(self.testArr)):
                print (self.testArr[w])

    def sayWords(self, source):
        if (source == "file"):
            for w in self.words:
                self.tts(w)
        if (source == "test"):
            for w in range(len(self.testArr)):
                self.tts(self.testArr[w])

    def randomiser (self):
        index = 0
        testOrder = {}

        while len(testOrder) < len(self.words):
            # Get a random number between 0 and number of words
            word = random.randint(0, len(self.words)-1)

            # Continue if key already set
            if (testOrder.get(word, "exists") != "exists"):
                continue

            testOrder[word] = index
            index += 1

        for pos in testOrder:
            self.testArr[testOrder[pos]] = self.words[pos]

    def resetGrades(self):
        for w in self.words:
            self.testGrade[w] = 0

    def giveGrade(self):
        correctAnswers = 0
        for w in range(len(self.testArr)):
            if (self.testGrade[self.testArr[w]] == 1):
                correctAnswers += 1
        return (100 * correctAnswers / len(self.testArr))

    def test(self, reset):
        self.randomiser()
        # Reset grades if requested
        if reset == "reset":
            self.resetGrades()
        else:
            self.tts('Lets try again')

        wc = 0
        for w in range(len(self.testArr)):
            wc += 1
            # Only test words that were spelled incorrectly
            if (self.testGrade[self.testArr[w]] == 0):
                self.tts('' + self.testArr[w])
                answer = input("[Word " + str(wc) + "] Please type your answer: ")
                if (answer.lower() == self.testArr[w].lower()):
                    print ("Awesome! that correct :)")
                    self.tts('Thats right!')
                    self.testGrade[self.testArr[w]] = 1
                else:
                    print ("That's wrong :( Here's how it should be spelled:")
                    self.tts('Oooops...that was wrong')
                    self.tts(' ' + self.testArr[w] + ' is spelled:')
                    for char in range(len(self.testArr[w])):
                        if (self.testArr[w][char] == " "):
                            self.tts("space")
                        else:
                            self.tts('' + self.testArr[w][char])

                if (w < len(self.testArr) - 1):
                    self.tts('...Lets move on to the next word')

        grade = self.giveGrade()
        print ("Your grade is " + str(int(grade)))

        self.tts('Your grade is ' + str(int(grade)))
        return grade

if (__name__ == "__main__"):
    rr = randomReader(str(Path.home()) + "/Desktop/words.txt")
    rr.welcome("Jonathan")

    grade = rr.test("reset")
    while (int(grade) < 100):
        grade = rr.test("continue")

    rr.tts('Well done')