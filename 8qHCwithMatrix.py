from datetime import datetime
import random
import time
import numpy as np
import pandas as pd


def main():
    global keySwitchesCounter
    randomRestarts = []
    keySwitches = []
    times = []
    for i in range(15):
        print("\n", "-"*30, "\n")
        print("\nITERATION", i+1)
        print()
        start = time.time()
        keySwitchesCounter = 0
        n = 8
        state = [0]*n
        board = [list([0]*8) for i in range(n)]
        randomConfiguration(board, state)
        print("Initial State")
        printBoard(board)  # initial state
        print("\nFinal State\n")
        hillClimb = hillClimbing(board, state)
        randomRestarts.append(hillClimb)
        keySwitches.append(keySwitchesCounter)
        end = time.time()
        t = (end-start)
        times.append(t)

    print()
    data = {"RandomRestarts": randomRestarts,
            "KeySwitches": keySwitches,
            "Time": times
            }
    df = pd.DataFrame(data)
    print(df)


def randomConfiguration(board, state):
    random.seed(None)

    for i in range(8):
        state[i] = random.randint(0, 7)
        board[state[i]][i] = 1


def printBoard(board):
    print(np.matrix(board), end="")
    """for i in range(8):
        print(" ", end="")
        for j in range(8):
            print(board[i][j], " ", end="")
        print("\n")"""


def printState(state):
    for i in range(8):
        print(" ", state[i], " ")


def compareStates(state1, state2):
    for i in range(8):
        if(state1[i] != state2[i]):
            return False
    return True


# istege gore tahtayi tamamen verilen deger ile kaplamak icin
def fill(board, value):
    for i in range(8):
        for j in range(8):
            board[i][j] = value


"""this function calculates the objective value of state(queens attacking each other)
    using the board by the following logic
"""


def calculateObjective(board, state):
    attacking = 0

    row = 0
    col = 0

    for i in range(8):
        # to the left of the same row
        row = state[i]
        col = i-1
        while col >= 0 and board[row][col] != 1:
            col -= 1
        if col >= 0 and board[row][col] == 1:
            attacking += 1
        # to the right of the same row
        row = state[i]
        col = i+1
        while col < 8 and board[row][col] != 1:
            col += 1
        if col < 8 and board[row][col] == 1:
            attacking += 1
        # diagonally to the left up
        row = state[i] - 1
        col = i - 1
        while col >= 0 and row >= 0 and board[row][col] != 1:
            col -= 1
            row -= 1
        if col >= 0 and row >= 0 and board[row][col] == 1:
            attacking += 1
        # diagonally to the right down
        row = state[i] + 1
        col = i + 1
        while col < 8 and row < 8 and board[row][col] != 1:
            col += 1
            row += 1
        if col < 8 and row < 8 and board[row][col] == 1:
            attacking += 1
        # diagonally to the left down
        row = state[i] + 1
        col = i - 1
        while col >= 0 and row < 8 and board[row][col] != 1:
            col -= 1
            row += 1
        if col >= 0 and row < 8 and board[row][col] == 1:
            attacking += 1
        # diagonally to the right up
        row = state[i] - 1
        col = i + 1
        while col < 8 and row >= 0 and board[row][col] != 1:
            col += 1
            row -= 1
        if col < 8 and row >= 0 and board[row][col] == 1:
            attacking += 1

    return int(attacking / 2)


def generateBoard(board, state):
    fill(board, 0)
    for i in range(8):
        board[state[i]][i] = 1


def copyState(state1, state2):
    for i in range(8):
        state1[i] = state2[i]


def getNeighbour(board, state):
    global keySwitchesCounter
    opState = [0]*8
    n = 8
    opBoard = [list([0]*8) for i in range(n)]

    copyState(opState, state)
    generateBoard(opBoard, opState)

    opObjective = calculateObjective(opBoard, opState)

    neighbourState = [0]*8
    n = 8
    neighbourBoard = [list([0]*8) for i in range(n)]

    copyState(neighbourState, state)
    generateBoard(neighbourBoard, neighbourState)

    for i in range(8):
        for j in range(8):
            if j != state[i]:
                neighbourState[i] = j
                neighbourBoard[neighbourState[i]][i] = 1
                neighbourBoard[state[i]][i] = 0
                temp = calculateObjective(neighbourBoard, neighbourState)
                if temp <= opObjective:
                    keySwitchesCounter += 1
                    opObjective = temp
                    copyState(opState, neighbourState)
                    generateBoard(opBoard, opState)
                neighbourBoard[neighbourState[i]][i] = 0
                neighbourState[i] = state[i]
                neighbourBoard[state[i]][i] = 1
    copyState(state, opState)
    fill(board, 0)
    generateBoard(board, state)


def hillClimbing(board, state):
    randomRestartCounter = 0
    neighbourState = [0]*8
    n = 8
    neighbourBoard = [list([0]*8) for i in range(n)]
    copyState(neighbourState, state)
    generateBoard(neighbourBoard, neighbourState)
    while True:
        copyState(state, neighbourState)
        generateBoard(board, state)
        getNeighbour(neighbourBoard, neighbourState)
        if compareStates(state, neighbourState):
            printBoard(board)
            break
        elif calculateObjective(board, state) == calculateObjective(neighbourBoard, neighbourState):
            randomRestartCounter += 1
            neighbourState[random.randint(0, 7)] = random.randint(0, 7)
            generateBoard(neighbourBoard, neighbourState)
    return randomRestartCounter


main()
