import os
import pyttsx3
import random
from sys import platform
from pathlib import Path


class RandomReader:
    def __init__(self, inputfile):
        # Verify that file exists or create one with one word (Welcome)
        if os.path.exists(my_file) == False:
            print("File does not exists. Creating new words.txt file.")
            f = open(my_file, "w+")
            f.write("Welcome")
            f.close()

        self.words = [line.strip() for line in open(inputfile, 'r')]
        self.testArr = {}
        self.testGrade = {}
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 170)

        # Alternate voices
        # voices = self.engine.getProperty('voices')
        # self.engine.setProperty('voice', voices[1].id)

    def tts(self, text):
        if platform == "darwin":
            # iOS
            os.system("say " + text)
        else:
            # Windows
            self.engine.say(text)
            self.engine.runAndWait()

    def welcome(self, name):
        self.tts('hello ' + name + '. How are you?' + '...Are you ready for your test?' + 'Lets begin!...')

    def printwords(self, source):
        print("Total number of words: " + str(len(self.words)))
        if source == "file":
            for w in self.words:
                print(w)
        if source == "test":
            for w in range(len(self.testArr)):
                print(self.testArr[w])

    def saywords(self, source):
        if source == "file":
            for w in self.words:
                self.tts(w)
        if source == "test":
            for w in range(len(self.testArr)):
                self.tts(self.testArr[w])

    def randomizer(self):
        index = 0
        testorder = {}

        while len(testorder) < len(self.words):
            # Get a random number between 0 and number of words
            word = random.randint(0, len(self.words)-1)

            # Continue if key already set
            if testorder.get(word, "exists") != "exists":
                continue

            testorder[word] = index
            index += 1

        for pos in testorder:
            self.testArr[testorder[pos]] = self.words[pos]

    def resetgrades(self):
        for w in self.words:
            self.testGrade[w] = 0

    def givegrade(self):
        correctanswers = 0
        for w in range(len(self.testArr)):
            if self.testGrade[self.testArr[w]] == 1:
                correctanswers += 1
        return 100 * correctanswers / len(self.testArr)

    def test(self, reset):
        self.randomizer()
        # Reset grades if requested
        if reset == "reset":
            self.resetgrades()
        else:
            self.tts('Lets try again')

        wc = 0
        for w in range(len(self.testArr)):
            wc += 1
            # Only test words that were spelled incorrectly
            if self.testGrade[self.testArr[w]] == 0:
                print("[Word " + str(wc) + "] Please type your answer: ")
                self.tts('' + self.testArr[w])
                answer = input("")
                # answer = input("[Word " + str(wc) + "] Please type your answer: ")
                if answer.lower() == self.testArr[w].lower():
                    print("Awesome! that correct :)")
                    self.tts('Thats right!')
                    self.testGrade[self.testArr[w]] = 1
                else:
                    print("That's wrong :( Here's how it should be spelled:")
                    self.tts('Oooops...that was wrong')
                    self.tts(' ' + self.testArr[w] + ' is spelled:')
                    for char in range(len(self.testArr[w])):
                        if self.testArr[w][char] == " ":
                            self.tts("space")
                        else:
                            self.tts('' + self.testArr[w][char])

                if w < len(self.testArr) - 1:
                    self.tts('...Lets move on to the next word')

        gradecalc = self.givegrade()
        print("Your grade is " + str(int(gradecalc)))

        self.tts('Your grade is ' + str(int(gradecalc)))
        return gradecalc


if __name__ == "__main__":
    my_file = str(Path.home()) + "/Desktop/words.txt"
    rr = RandomReader(my_file)
    rr.welcome("Jonathan")

    grade = rr.test("reset")
    while int(grade) < 100:
        grade = rr.test("continue")

    rr.tts('Well done')
