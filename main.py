from data import *

import random
import os
import sys

def generateQuestion(difficultyMinimum, difficultyMaximum, allowedCommands):
    """
    The difficulty of a question determines what kind of question could be asked.
    0: Convert command to corresponding hexadecimal or binary.
    1: Convert hexadecimal or binary opcode to command.
    2: Given a command, give its structure (R, I, or J).
    3: Given a structure and one of its sections, give the order that section apperas in or its size.
    4: Given a structure, enter either the sizes of its sections, or the names of its sections.
    5: Given a full command, translate it to its corresponding binary.
    6: Given a string of binary, translate it to its corresponding command.

    Each temple uses a different difficulty list:
    Temple #1: 0 - 1
    Temple #2: 2 - 3
    Temple #3: 0 - 4
    Temple #4: 5

    Final Challenge: 6
    """

    if difficultyMinimum > difficultyMaximum or difficultyMinimum < 0 or difficultyMaximum > 6:
        return ["", ""]
    
    chosenDifficulty = random.choice(range(difficultyMinimum, difficultyMaximum + 1))

    # Used for difficulties 5 and 6.
    def randomBinary(length):
        output = ""

        while len(output) < length:
            output += str(random.randint(0, 1))
        
        return output

    match chosenDifficulty:
        case 0:
            chosenCommand = random.choice(allowedCommands)
            useBinary = random.choice([True, False])

            if useBinary:
                binaryValue = bin(int(hex(codes[chosenCommand]), 16))[2:].zfill(6)

                return [f"Convert the command \"{chosenCommand}\" to binary. Your answer should be in the form of six binary bits, e.g. \"010110\".", str(binaryValue)]
            
            hexadecimal = hex(codes[chosenCommand]).upper()[2:]
            if len(hexadecimal) <= 1:
                hexadecimal = "0" + hexadecimal

            return [f"Convert the command \"{chosenCommand}\" to hexadecimal. Your answer should be in the form of two hexadecimal bits, e.g. \"03\" or \"A5\".", hexadecimal]


        case 1:
            chosenCommand = random.choice(allowedCommands)
            useBinary = random.choice([True, False])
            usingFunction = chosenCommand in usesFunction

            if useBinary:
                binaryValue = bin(int(hex(codes[chosenCommand]), 16))[2:].zfill(6)

                return [f"Convert the binary code \"0b{binaryValue}\" into its corresponding MIPS command in lowercase. " + ("Note that this binary code is used for the function parameter." if usingFunction else ""), chosenCommand]
            
            hexadecimal = hex(codes[chosenCommand]).upper()[2:]
            if len(hexadecimal) <= 1:
                hexadecimal = "0" + hexadecimal

            return [f"Convert the hexadecimal code \"0x{hexadecimal}\" into its corresponding MIPS command in lowercase. " + ("Note that the binary code is used for the function parameter." if usingFunction else ""), chosenCommand]


        case 2:
            chosenCommand = random.choice(allowedCommands)
            structure = commandTypes[chosenCommand]

            return [f"Give the correct type of structure the command \"{chosenCommand}\" uses (R, I, or J).", structure]


        case 3:
            chosenStructure = random.choice(allowedCommands)
            chosenSection = random.choice(structures[chosenStructure])
            giveSize = random.choice([False, True])

            if giveSize:
                return [f"Give the number of bits used to represent the section {chosenSection[0]} in the structure {chosenStructure}.", str(chosenSection[1])]

            index = structures[chosenStructure].index(chosenSection) + 1
            return [f"Give the order in which the section {chosenSection[0]} shows up in the structure {chosenStructure}, counting from one.", str(index)]


        case 4:
            chosenStructure = random.choice(allowedCommands)
            giveSize = random.choice([True, False])

            if giveSize:
                sizeList = ""

                for section in structures[chosenStructure]:
                    sizeList += str(section[1]) + " "
                
                return [f"Give the sizes of the sections in structure {chosenStructure}, seperating each size with a space.", sizeList[:-1]]

            sectionList = ""

            for section in structures[chosenStructure]:
                sectionList += str(section[0]) + " "
            
            return [f"Give the names of the sections in structure {chosenStructure}, seperating each name with a space.", sectionList[:-1]]


        case 5:
            chosenCommand = random.choice(allowedCommands)
            print(chosenCommand)
            template = templates[chosenCommand]

            binaryCommandKey = bin(int(hex(codes[chosenCommand]), 16))[2:].zfill(6)

            command = template[0]
            binary = template[1].replace("[C]", binaryCommandKey)

            while command.find("[") != -1:
                commandID = command[command.index("[") + 1:command.index("]")]

                if not commandID.isnumeric():
                    length = int(commandID[:-1])
                    newBinary = randomBinary(length)

                else:
                    newBinary = randomBinary(int(commandID))

                newHex = hex(int(newBinary, 2))[2:]

                command = command[:command.find("[" + commandID + "]")] + newHex.upper() + command[command.find("[" + commandID + "]") + len("[" + commandID + "]"):]
                binary = binary[:binary.find("[" + commandID + "]")] + newBinary + binary[binary.find("[" + commandID + "]") + len("[" + commandID + "]"):]

            return [f"Give the binary representation of the command \"{command}\", where all of the numbers are represented in hexadecimal.", binary]

        case 6:
            chosenCommand = random.choice(allowedCommands)
            template = templates[chosenCommand]

            binaryCommandKey = bin(int(hex(codes[chosenCommand]), 16))[2:].zfill(6)

            command = template[0]
            binary = template[1].replace("[C]", binaryCommandKey)

            while command.find("[") != -1:
                commandID = command[command.index("[") + 1:command.index("]")]

                if not commandID.isnumeric():
                    length = int(commandID[:-1])
                    newBinary = randomBinary(length)

                else:
                    newBinary = randomBinary(int(commandID))

                newHex = hex(int(newBinary, 2))[2:]

                command = command[:command.find("[" + commandID + "]")] + newHex.upper() + command[command.find("[" + commandID + "]") + len("[" + commandID + "]"):]
                binary = binary[:binary.find("[" + commandID + "]")] + newBinary + binary[binary.find("[" + commandID + "]") + len("[" + commandID + "]"):]

            return [f"Convert the binary line \"0b{binary}\" to its corresponding MIPS line, representing any numbers as its hexadecimal value.", command]


def neatPrint(text):
    buffer = ""

    for character in text:
        buffer += character

        if len(buffer) >= 120 or (len(buffer) >= 80 and character == " "):
            print(buffer)
            buffer = ""
    
    if buffer != "":
        print(buffer)


class GameInstance:
    def __init__(self):
        self.points = 0
        self.combo = 0

        self.lives = 3
        self.mistakesLeft = 5

        self.lastCompleted = 0
        self.highscore = 0
        self.highscoreStart = 0
        self.highscoreEnd = 0
    
    def loadSave(self):
        f = open("save.txt", "r")

        data = []

        for line in f.readlines():
            data.append(int(line.strip()))
        
        self.lastCompleted = data[0]
        self.highscore = data[1]
        self.highscoreStart = data[2]
        self.highscoreEnd = data[3]

        f.close()

    def saveGame(self):
        f = open("save.txt", "w")

        f.write(f"{self.lastCompleted}\n{self.highscore}\n{self.highscoreStart}\n{self.highscoreEnd}")

        f.close()

    def reset(self):
        self.points = 0
        self.combo = 0
        self.lives = 3
        self.mistakesLeft = 5

    def startRound(self, floorName, minQuestions, maxQuestions, minDifficulty, maxDifficulty):
        questionsLeft = random.choice(range(minQuestions, maxQuestions + 1))

        while questionsLeft > 0:
            os.system("cls")
            print("----- " + floorName + " -----")
            print(f"Lives Left: {self.lives}")
            print(f"Points: {self.points}" + ("" if self.combo < 2 else f" (COMBO X{self.combo})") + "\n")

            print(f"Questions Left: {questionsLeft}")

            mistakeString = ""

            for i in range(0, 5):
                if i < (5 - self.mistakesLeft):
                    mistakeString += "X "
                else:
                    mistakeString += "_ "
            print("Mistakes Made: [ " + mistakeString[:-1] + " ]")
            print("-------------------------------------------------")

            question = generateQuestion(minDifficulty, maxDifficulty, list(codes.keys()))
            neatPrint(question[0])

            answer = input("\n> ")

            if answer == question[1]:
                questionsLeft -= 1
                
                self.combo += 1
                self.points += 100 + ((self.combo - 1) * 10)
                
            
            else:
                print("\nIncorrect answer. The correct answer was:")
                print(question[1])

                input("\nPress enter to continue...")
                self.combo = 0
                self.mistakesLeft -= 1
            
            if self.mistakesLeft <= 0:
                return False
        
        return True
    
    def handleGame(self, levelID):
        rounds = [
            ["Zuga's Temple - Floor 1", 10, 15, 0, 0],
            ["Zuga's Temple - Floor 2", 10, 15, 1, 1],
            ["Zuga's Temple - Floor 3", 15, 20, 0, 1],
            ["Mati's Temple - Floor 3", 12, 20, 2, 2],
            ["Mati's Temple - Floor 3", 15, 20, 2, 3],
            ["Mati's Temple - Floor 3", 20, 25, 2, 3],
            ["Quarata's Temple - Floor 1", 15, 25, 4, 4],
            ["Quarata's Temple - Floor 2", 20, 30, 2, 4],
            ["Quarata's Temple - Floor 3", 25, 30, 0, 4],
            ["Zuma's Temple - Floor 1", 20, 30, 5, 5],
            ["Zuma's Temple - Floor 2", 30, 40, 3, 5],
            ["Zuma's Temple - Floor 3", 50, 50, 0, 5],
            ["The Final Barrier", 20, 20, 6, 6],
            ["The Ultimate Test", 250, 250, 0, 6]
        ]

        startLevel = levelID + 1
        currentLevel = levelID
        self.reset()

        gameActive = True

        while gameActive:
            round = rounds[currentLevel]

            result = self.startRound(*round)
            self.mistakesLeft = 5

            if result:
                os.system("cls")

                print("LEVEL COMPLETE.")
                print(round[0])
                print(f"\nLives Left: {self.lives}")
                print(f"Points: {self.points}")
                input("\nPress enter to continue...")

                currentLevel += 1
                self.lives += 1
                self.lastCompleted = max(self.lastCompleted, currentLevel)
                self.saveGame()

                if currentLevel >= 13:
                    os.system("cls")

                    self.points += self.lives * 25000

                    print("YOU WIN!")
                    print(f"Final Points: {self.points}")

                    if self.points > self.highscore:
                        print("\nNew highscore achieved!")

                        self.highscore = self.points
                        self.highscoreStart = startLevel
                        self.highscoreEnd = currentLevel - 1
                    
                    else:
                        print(f"\nPrevious highscore: {self.highscore} (achieved from \"{rounds[self.highscoreStart - 1][0]}\" to \"{rounds[self.highscoreEnd - 1][0]}\")")

                    self.saveGame()
                    input("\nPress enter to continue...")
                    gameActive = False

            else:
                os.system("cls")
                self.lives -= 1

                if self.lives <= 0:
                    print("GAME OVER.")
                    print(f"Points: {self.points}")
                    print(f"Final Level: {round[0]}")

                    if self.points > self.highscore:
                        print("\nNew highscore achieved!")

                        self.highscore = self.points
                        self.highscoreStart = startLevel
                        self.highscoreEnd = currentLevel - 1
                    
                    else:
                        print(f"\nPrevious highscore: {self.highscore} (achieved from \"{rounds[self.highscoreStart - 1][0]}\" to \"{rounds[self.highscoreEnd - 1][0]}\")")

                    gameActive = False
                    self.saveGame()

                else:
                    print("LIFE LOST.")
                    print(round[0])
                    print(f"\nLives Left: {self.lives}")
                    print(f"Points: {self.points}")
                
                input("\nPress enter to continue...")

        os.system("cls")

    def play(self):
        isDone = False
        os.system("cls")

        while not isDone:
            print("Select a level, if you dare...")

            choices = [
                ["Zuga's Temple - Floor 1"],
                ["Zuga's Temple - Floor 2"],
                ["Zuga's Temple - Floor 3"],
                ["Mati's Temple - Floor 1"],
                ["Mati's Temple - Floor 2"],
                ["Mati's Temple - Floor 3"],
                ["Quarata's Temple - Floor 1"],
                ["Quarata's Temple - Floor 2"],
                ["Quarata's Temple - Floor 3"],
                ["Zuma's Temple - Floor 1"],
                ["Zuma's Temple - Floor 2"],
                ["Zuma's Temple - Floor 3"],
                ["The Final Barrier"],
                ["The Ultimate Test"]
            ]

            for (i, choice) in enumerate(choices):
                if i <= self.lastCompleted:
                    print(f"{i + 1}: {choice[0]}")
            
            print(f"\n{len(choices) + 1}: Back.")

            op = input("\n> ")
            os.system("cls")

            if op == str(len(choices) + 1):
                isDone = True
            
            elif op.isnumeric() and int(op) >= 1 and int(op) <= (self.lastCompleted + 1):
                self.handleGame(int(op) - 1)

            else:
                print("Invalid choice, please try again.\n")


    def mainMenu(self):
        isDone = False
        os.system("cls")

        self.loadSave()

        while not isDone:
            print("ZUMA BUT BINARY")
            print("An unecessary complicated way to learn MIPS binary.\n")
            print("1: Play")
            print("2: Practice")
            print("3: Quit")

            op = input("\n> ")
            os.system("cls")

            match op:
                case "1":
                    self.play()

                case "2":
                    pass

                case "3":
                    isDone = True

                case _:
                    print("Error: Invalid input, please try again.\n")

game = GameInstance()
game.mainMenu()