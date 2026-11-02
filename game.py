from position import Position
from math import inf
from time import time
from copy import deepcopy


class bcolors:
    GREEN = "\u001b[32m"
    RED = "\u001b[31m"
    CYAN = "\u001b[36m"
    BLACK = "\u001b[30;1m"
    WHITE = "\u001b[37;1m"
    BG_BLUE = "\u001b[44;1m"
    BG_WHITE = "\u001b[47;1m"
    BG_PINK = "\u001b[45m"
    END = "\033[0m"


def print_table(table, selected=None, valid_moves=None):
    for i in range(len(table)):
        if i == 0:
            print("    0    1    2    3    4    5    6    7")
            print("  __________________________________________")
        for j in range(len(table[i])):
            if j == 0:
                print(i, end=" |")
            if table[i][j] == "w" or table[i][j] == "W":
                if selected and ((i, j) in selected or (i, j) == selected):
                    print(
                        bcolors.BG_BLUE
                        + bcolors.BLACK
                        + " "
                        + str(table[i][j])
                        + " "
                        + bcolors.END,
                        end="  ",
                    )
                else:
                    print(
                        bcolors.GREEN + " " + str(table[i][j]) + " " + bcolors.END,
                        end="  ",
                    )
            elif table[i][j] == "b" or table[i][j] == "B":
                if selected and ((i, j) in selected or (i, j) == selected):
                    print(
                        bcolors.BG_BLUE
                        + bcolors.BLACK
                        + " "
                        + str(table[i][j])
                        + " "
                        + bcolors.END,
                        end="  ",
                    )
                else:
                    print(
                        bcolors.RED + " " + str(table[i][j]) + " " + bcolors.END,
                        end="  ",
                    )

            elif valid_moves and (i, j) in valid_moves:
                print(
                    bcolors.BG_WHITE
                    + bcolors.BLACK
                    + str(i)
                    + " "
                    + str(j)
                    + bcolors.END,
                    end="  ",
                )
            else:
                if selected and ((i, j) in selected or (i, j) == selected):
                    print(
                        bcolors.BG_PINK
                        + bcolors.BLACK
                        + " "
                        + str(table[i][j])
                        + " "
                        + bcolors.END,
                        end="  ",
                    )
                else:
                    print(" " + str(table[i][j]) + " ", end="  ")
        print("| " + str(i))
    print("  ------------------------------------------")
    print("    0    1    2    3    4    5    6    7")


# MIN MAX simple implementation


def min_max(position, depth, max_player):
    if depth == 0 or position.get_game_end():
        return position.evaluate_state()
    if max_player:
        max_evaluation = -inf
        for child in position.get_next_moves():
            eval = min_max(child, depth - 1, False)
            max_evaluation = max(max_evaluation, eval)
        position.set_evaluation(max_evaluation)
        return max_evaluation
    else:
        min_evaluation = inf
        for child in position.get_next_moves():
            eval = min_max(child, depth - 1, True)
            min_evaluation = min(min_evaluation, eval)
        position.set_evaluation(min_evaluation)
        return min_evaluation


# MIN MAX with ALPHA-BETA pruning


def alpha_beta(position, depth, alpha, beta, max_player):
    if depth == 0 or position.get_game_end():
        return position.evaluate_state()
    if max_player:
        max_evaluation = -inf
        for child in position.get_next_moves():
            eval = alpha_beta(child, depth - 1, alpha, beta, False)
            max_evaluation = max(max_evaluation, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        position.set_evaluation(max_evaluation)
        return max_evaluation
    else:
        min_evaluation = inf
        for child in position.get_next_moves():
            eval = alpha_beta(child, depth - 1, alpha, beta, True)
            min_evaluation = min(min_evaluation, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        position.set_evaluation(min_evaluation)
        return min_evaluation


# Alpha beta pruning minmax that calls a different function. It can be changed to take the function as a parameter


def alpha_beta_ending(position, depth, alpha, beta, max_player):
    if depth == 0 or position.get_game_end():
        return position.evaluate_state_ending()
    if max_player:
        max_evaluation = -inf
        for child in position.get_next_moves():
            eval = alpha_beta_ending(child, depth - 1, alpha, beta, False)
            max_evaluation = max(max_evaluation, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        position.set_evaluation(max_evaluation)
        return max_evaluation
    else:
        min_evaluation = inf
        for child in position.get_next_moves():
            eval = alpha_beta_ending(child, depth - 1, alpha, beta, True)
            min_evaluation = min(min_evaluation, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        position.set_evaluation(min_evaluation)
        return min_evaluation


def determine_dynamic_depth(time_previous_move, depth, num_moves):
    if time_previous_move < 0.5 and num_moves <= 6:
        return depth + 1
    if depth > 6 and (time_previous_move > 4 or num_moves > 6):
        return depth - 1
    return depth


def ending_conditions(position, figure_counter):
    moves = position.get_next_moves()

    num_figures = position.count_pieces()
    if num_figures[0] == 0:
        print("Black won!")
        return True
    if num_figures[1] == 0:
        print("White won!")
        return True
    if num_figures[0] + num_figures[1] == figure_counter[0]:
        figure_counter[1] += 1
        if figure_counter[1] == 50:
            print("Tie!")
            return True
    else:
        figure_counter[0] = num_figures[0] + num_figures[1]
        figure_counter[1] = 0
    if not moves:
        print("There are no possible moves left! Game is finished!")
        return True
    return False


def main():
    table = [
        [".", "b", ".", "b", ".", "b", ".", "b"],
        ["b", ".", "b", ".", "b", ".", "b", "."],
        [".", "b", ".", "b", ".", "b", ".", "b"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["w", ".", "w", ".", "w", ".", "w", "."],
        [".", "w", ".", "w", ".", "w", ".", "w"],
        ["w", ".", "w", ".", "w", ".", "w", "."],
    ]

    position = Position(table, True)
    time_previous_move = 4.5
    time_previous_moveB = 4.5
    depthB = 6
    depthW = 8

    without_capture = [0, 0]

    while True:
        if ending_conditions(position, without_capture):
            break

        num_moves = len(position.get_next_moves())
        depthW = determine_dynamic_depth(time_previous_moveB, depthW, num_moves)
        previous_table = deepcopy(position.get_table())
        print("depth of white is", str(depthW))
        inputDepthW = input("do you want to change the depth? ")
        if inputDepthW != "":
            depthW = int(inputDepthW)
        print("White player THINKING.....................................")
        t1 = time()

        num_figures = position.count_pieces()
        if num_figures[0] + num_figures[1] > 6:
            alpha_beta(position, depthW, -inf, inf, True)

            position = max(position.get_next_moves())
        else:
            alpha_beta_ending(position, depthW + 2, -inf, inf, True)

            position = max(position.get_next_moves())

        t2 = time()
        time_previous_moveB = t2 - t1

        differences = position.find_move_played(previous_table)
        print_table(position.get_table(), differences)
        print("White played the move displayed on the table above.\n\n\n")

        if ending_conditions(position, without_capture):
            break
        num_moves = len(position.get_next_moves())
        depthB = determine_dynamic_depth(time_previous_move, depthB, num_moves)
        print("depth of black is", str(depthB))

        previous_table = deepcopy(position.get_table())
        print("Black player THINKING.....................................")
        t1 = time()
        num_figures = position.count_pieces()
        if num_figures[0] + num_figures[1] > 6:
            alpha_beta(position, depthB, -inf, inf, True)

            position = max(position.get_next_moves())
        else:
            alpha_beta_ending(position, depthB + 2, -inf, inf, True)

            position = max(position.get_next_moves())
        t2 = time()
        time_previous_move = t2 - t1
        differences = position.find_move_played(previous_table)
        print(time_previous_move)

        print_table(position.get_table(), differences)
        print("Black played a move displayed on the table above.\n\n")


if __name__ == "__main__":
    main()
