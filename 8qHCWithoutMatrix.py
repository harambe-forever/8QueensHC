from datetime import datetime
import random
import time
import numpy as np
import pandas as pd


def main():
    # board = [6, 2, 2, 1, 2, 7, 4, 5]            # dogru degil ornek
    # board = [3, 1, 6, 2, 5, 7, 0, 4]          # dogru ornek
    random_restarts_list = []
    key_switches_list = []
    times = []
    for i in range(15):
        print("\n", "-"*50, "\nITERATION:", i+1)
        random_restarts = 0
        key_switches = 0
        t = 0
        start = time.time()
        board = return_random_board()
        print("initial board:", board)
        print_board(board)
        board, random_restarts, key_switches = hill_climbing(board)
        end = time.time()
        t = end-start
        print("final board:", board, " random restarts:",
              random_restarts, " key switches:", key_switches)
        print_board(board)
        random_restarts_list.append(random_restarts)
        key_switches_list.append(key_switches)
        times.append(t)
    data = {"RandomRestarts": random_restarts_list,
            "KeySwtiches": key_switches_list,
            "Time": times
            }
    df = pd.DataFrame(data)
    print(df)
    print("Average time spent:", sum(times)/len(board))


def return_random_board():
    board_new = []
    for i in range(0, 8):
        board_new.append(random.randint(0, 7))
    return board_new


def print_board(board):
    matrix = [list([0]*8) for i in range(8)]
    for r in range(8):
        for c in range(8):
            if r != board[c]:
                matrix[r][c] = 0
            else:
                matrix[r][c] = 1
    print(np.matrix(matrix), end="")
    print()


def calculate_threat_horizontally(board):
    t_horizontally = 0
    len_board = len(board)
    for this in range(len_board):
        temp = board[this]
        for rest in range(this + 1, len_board):
            if(board[rest] == temp):
                # print(temp, " ", board[rest])
                t_horizontally += 1
    return t_horizontally


def calculate_threat_diagonally(board):
    t_diagonally = 0
    len_board = len(board)
    for index1 in range(len_board):
        this_index1_value = board[index1]
        for index2 in range(index1 + 1, len_board):
            if (index2 - index1) == abs(this_index1_value - board[index2]):
                # print(index1, ":", this_index1_value,
                #     " ", index2, ":", board[index2])
                t_diagonally += 1
    return t_diagonally


def calculate_threats(board):
    t_horizontally = calculate_threat_horizontally(board)
    t_diagonally = calculate_threat_diagonally(board)
    total_threats_current = t_horizontally + t_diagonally
    return total_threats_current


def get_best_neighbour(current_board):
    if calculate_threats(current_board) == 0:
        return current_board
    temp = calculate_threats(current_board)
    best_yet = current_board
    for i in range(len(current_board)):
        best_neigbour = current_board.copy()
        for j in range(len(best_neigbour) - 1):
            if(j != current_board[i]):
                best_neigbour[i] = j
                t = calculate_threats(best_neigbour)
                if t <= temp:
                    temp = t
                    best_yet = best_neigbour.copy()
                    # print("t:", t, " temp:", temp, " best_yet:", best_yet)
                """print(best_neigbour, " board index: ", i,
                      " board index value: ", j, " t value:", t)"""
    return best_yet


def hill_climbing(board):
    neighbour = []
    current = board.copy()
    tprev = 0
    random_restart_counter = 0
    key_switches_counter = 0
    while True:
        t = calculate_threats(current)
        if t == 0:
            break
        if t == tprev:
            # print("random restart t: ", t)
            random_restart_counter += 1
            current = return_random_board()
        neighbour = get_best_neighbour(current)
        t_neighbour = calculate_threats(neighbour)
        tprev = t
        if t_neighbour <= t:
            current = neighbour.copy()
        key_switches_counter += 1
    # print("Random restarts: ", random_restart_counter,
    #      " key switches: ", key_switches_counter)
    return current, random_restart_counter, key_switches_counter


if __name__ == "__main__":
    main()
