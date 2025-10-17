from data import *

import random

def generateQuestion(difficultyMinimum, difficultyMaximum):
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
            chosenCommand = random.choice(list(codes.keys()))
            useBinary = random.choice([True, False])

            if useBinary:
                binaryValue = bin(int(hex(codes[chosenCommand]), 16))[2:].zfill(6)

                return [f"Convert the command \"{chosenCommand}\" to binary. Your answer should be in the form of six binary bits, e.g. \"010110\".", str(binaryValue)]
            
            hexadecimal = hex(codes[chosenCommand]).upper()[2:]
            if len(hexadecimal) <= 1:
                hexadecimal = "0" + hexadecimal

            return [f"Convert the command \"{chosenCommand}\" to hexadecimal. Your answer should be in the form of two hexadecimal bits, e.g. \"03\" or \"A5\".", hexadecimal]


        case 1:
            chosenCommand = random.choice(list(codes.keys()))
            useBinary = random.choice([True, False])

            if useBinary:
                binaryValue = bin(int(hex(codes[chosenCommand]), 16))[2:].zfill(6)

                return [f"Convert the binary code \"0b{binaryValue}\" into its corresponding MIPS command in lowercase.", chosenCommand]
            
            hexadecimal = hex(codes[chosenCommand]).upper()[2:]
            if len(hexadecimal) <= 1:
                hexadecimal = "0" + hexadecimal

            return [f"Convert the hexadecimal code \"0x{hexadecimal}\" into its corresponding MIPS command in lowercase.", chosenCommand]


        case 2:
            chosenCommand = random.choice(list(codes.keys()))
            structure = commandTypes[chosenCommand]

            return [f"Give the correct type of structure the command \"{chosenCommand}\" uses (R, I, or J).", structure]


        case 3:
            chosenStructure = random.choice(list(structures.keys()))
            chosenSection = random.choice(structures[chosenStructure])
            giveSize = random.choice([False, True])

            if giveSize:
                return [f"Give the number of bits used to represent the section {chosenSection[0]} in the structure {chosenStructure}.", str(chosenSection[1])]

            index = structures[chosenStructure].index(chosenSection) + 1
            return [f"Give the order in which the section {chosenSection[0]} shows up in the structure {chosenStructure}, counting from one.", str(index)]


        case 4:
            chosenStructure = random.choice(list(structures.keys()))
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
            chosenCommand = random.choice(list(codes.keys()))
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
            chosenCommand = random.choice(list(codes.keys()))
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


print("")

question = generateQuestion(0, 6)
print(question[0])
print("\nAnswer: " + question[1])