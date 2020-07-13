import csv
import math
import sys

class Cell(object):
    def __init__(self, value):
        self.blankDigit = 0
        self.possibilities = {}
        self.setValue(value)

    def getValue(self):
        return int(self.value)

    def setValue(self, value):
        self.value = value

        if self.isBlank():
            self.possibilities = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        else:
            self.possibilities.clear()

    def getPossibilities(self):
        return self.possibilities

    def removePossibility(self, impossibility):

        if impossibility in self.possibilities:
            self.possibilities.remove(impossibility)



    def isBlank(self):
        if self.getValue() == 0:
            return True
        else:
            return False

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)



class Sudoku:
    def __init__(self, inputFile):
        self.size = 9
        self.blankDigit = 0
        self.CellArray = [[Cell(self.blankDigit) for col in range(self.size)] for row in range(self.size)]
        self.fileName = inputFile
        self.blankCellCounter = 0
    # end of def __init__


    def print(self):

        for row in range(self.size):
            rowStr = ""
            for col in range(self.size):
                rowStr = rowStr + " " + str(self.CellArray[row][col].getValue())
            # end of for col

            print(rowStr)
        # end of for row

        print("The number of blank cells are: ", self.blankCellCounter)
    # end of def print

    def initialize(self):
        with open(self.fileName) as csvfile:
            inputFile = csv.reader(csvfile, delimiter=',')

            row = 0

            for fileline in inputFile:
                for col in range(self.size):
                    self.CellArray[row][col].setValue(fileline[col])
                    if self.CellArray[row][col].isBlank():
                        self.blankCellCounter += 1

                row += 1



    def solve(self):


#keep going until one of the following two conditions are met
    #condition A is that all the cells are solved
    #condition B is that the number of all unsolved characters is that same in the next run

        passCount = 0
        prevBlankCellCounter = self.blankCellCounter
        while True:

            passCount += 1

            for i in range(self.size):
                for j in range(self.size):

                    thisCell = self.CellArray[i][j]
                    # Only the blank cell needs solving
                    if thisCell.isBlank():
                        possibilities = thisCell.getPossibilities()

                        ##############################################
                        # remove all the row possibilities
                        for jj in range(self.size):
                            if not self.CellArray[i][jj].isBlank():
                                thisCell.removePossibility(self.CellArray[i][jj].getValue())

                        ###############################################
                        # remove all the column possibilities
                        for ii in range(self.size):
                            if not self.CellArray[ii][j].isBlank():
                                thisCell.removePossibility(self.CellArray[ii][j].getValue())


                        ###############################################
                        # remove all the box possibilities

                        boxStartrow = math.floor(i/3)*3
                        boxStartcol = math.floor(j/3)*3

                        for iii in range(boxStartrow, boxStartrow + 3):
                            for jjj in range(boxStartcol, boxStartcol + 3):
                                if not self.CellArray[iii][jjj].isBlank():
                                    thisCell.removePossibility(self.CellArray[iii][jjj].getValue())


                        possibilities = thisCell.getPossibilities()
                        print('[', i, ']', '[', j, ']', possibilities)
                        #################################################
                        # if there is only one possibility left, that's the value of this cell

                        if len(possibilities) == 1:
                            possibility = possibilities.pop()
                            thisCell.setValue(possibility)

                            self.blankCellCounter -= 1

            if self.blankCellCounter == 0:
                print("The sudoku is solved in", passCount, "passes")
                break
            elif prevBlankCellCounter == self.blankCellCounter:
                print("Sudoku not solved")
                break

            #The Soduko is not solved but this pass solved one or more cells
            prevBlankCellCounter = self.blankCellCounter

    #end of solve function

    def validate(self):

        ######################################
        # validate boxes

        for i in range(0, 8, 3):
            for j in range (0, 8, 3):
                thisdict = {}
                print("Validating box", i, j)

                for ii in range(i, i + 3):

                    for jj in range(j, j + 3):

                        cellValue = self.CellArray[ii][jj].getValue()

                        if cellValue in thisdict:
                            print(cellValue, "The value already found. Current index", ii, jj )
                            return False

                        if 1 > cellValue < 9:
                            print(cellValue, "Value is not between 1-9")
                            return False

                        thisdict[cellValue] = ""

        #end of validating box

        ######################################
        #validate rows
        for i in range(self.size):
            thisdict = {}
            print("Validating row", i)
            for j in range(self.size):

                cellValue = self.CellArray[i][j].getValue()

                if cellValue in thisdict:
                    print(cellValue, "The value already found")
                    return False

                if 1 > cellValue < 9:
                    print(cellValue, "Value is not between 1-9")
                    return False

                thisdict[cellValue] = ""

        #end of validating rows

        ######################################
        # validate cols

        for i in range(self.size):
            thisdict = {}
            print("Validating col", i)
            for j in range(self.size):

                cellValue = self.CellArray[j][i].getValue()

                if cellValue in thisdict:
                    print(cellValue, "The value already found")
                    return False

                if 1 > cellValue < 9:
                    print(cellValue, "Value is not between 1-9")
                    return False

                thisdict[cellValue] = ""







        return True
    #end of validate function



    def writeToFile(self, outputFileName):

        blankCells = 0

        sudokuStr = ""

        for row in range(self.size):

            for col in range(self.size):
                sudokuStr = sudokuStr + " " + str(self.CellArray[row][col].getValue())
            # end of for col

            sudokuStr = sudokuStr + "\n"
        # end of for row
        if self.CellArray[row][col].isBlank():
            blankCells += 1


        with open(outputFileName, 'w') as txtfile:
            txtfile.write(sudokuStr)
            txtfile.write(str(blankCells))

        # end of with open...
    # end of writeToFile



def main():

    inFile = sys.argv[1]

    if inFile == "":
        print("No input file specified")
        return
    #end of if inFile

    s = Sudoku(inFile)

    s.initialize()

    s.print()

    s.solve()

    s.print()

    if s.validate():
        print("Sudoku is valid")
    else:
        print("Sudoku is invalid")


    s.writeToFile(inFile + ".out")


main()
