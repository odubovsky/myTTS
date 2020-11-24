import os
import random

class randomReader:
    def __init__(self, inputFile):
        self.words = [line.strip() for line in open(inputFile, 'r')]
        self.testArr = {}
        self.testGrade = {}

    def welcome(self, name):
        os.system("say 'hello '" + name)
        os.system("say 'How are you?'")
        os.system("say '...Are you ready for your test?'")
        os.system("Say 'Lets begin!...'")

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
                self.engine.say(w)
        if (source == "test"):
            for w in range(len(self.testArr)):
                self.engine.say(self.testArr[w])
        self.engine.runAndWait()

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
            os.system("say 'Lets try again'")

        wc = 0
        for w in range(len(self.testArr)):
            wc += 1
            # Only test words that were spelled incorrectly
            if (self.testGrade[self.testArr[w]] == 0):
                os.system("say ''" + self.testArr[w])
                answer = input("[Word " + str(wc) + "] Please type your answer: ")
                if (answer.lower() == self.testArr[w].lower()):
                    print ("Awesome! that correct :)")
                    os.system("say 'Thats right!'")
                    os.system("say '...Lets move on to the next word'")
                    self.testGrade[self.testArr[w]] = 1
                else:
                    print ("That's wrong :( Here's how it should be spelled:")
                    os.system("say 'Oooops...that was wrong'")
                    os.system("say ' '" + self.testArr[w] + " is spelled:")
                    for char in range(len(self.testArr[w])):
                        os.system("say ''" + self.testArr[w][char])
                    os.system("say '...Lets move on to the next word'")

        grade = self.giveGrade()
        print ("Your grade is " + str(int(grade)))

        os.system("say 'Your grade is '" + str(int(grade)))
        return grade

if (__name__ == "__main__"):
    rr = randomReader ("/Users/odeddubovsky/Desktop/words.txt")
    rr.welcome("Jonathan")

    grade = rr.test("reset")
    while (int(grade) < 100):
        grade = rr.test("continue")

    os.system("say 'Well done'")