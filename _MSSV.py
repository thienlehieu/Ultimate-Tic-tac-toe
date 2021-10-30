import numpy as np
from collections import deque
from math import inf
import copy
from state import State

opp_site = {0: 8, 8: 0, 1: 7, 7: 1, 2: 6, 6: 2, 3: 5, 5: 3}


def heuristic(state, player=1):
    score = 0
    global_block = state.global_cells.reshape(3, 3)

    # print(global_block)
    for id in range(0, 3):
        if global_block[:, id][global_block[:, id] == 1].sum() == 2:
            score += 4
        if global_block[:, id][global_block[:, id] == -1].sum() == -2:
            score += -4
        if global_block[id, :][global_block[id, :] == 1].sum() == 2:
            score += 4
        if global_block[id, :][global_block[id, :] == -1].sum() == -2:
            score += -4

    for ind, block in enumerate(state.blocks):
        if block[1, 1] == 1:
            score += 3

        if block[1, 1] == -1:
            score += -3

        if State.game_result(state, block) == 1:
            score += 5

        if State.game_result(state, block) == -1:
            score += -5

        if State.game_result(state, block) == 1 and ind == 4:
            score += 10

        if State.game_result(state, block) == -1 and ind == 4:
            score += -10

        for id in range(0, 3):
            if block[:, id][block[:, id] == 1].sum() == 2:
                score += 2
            if block[:, id][block[:, id] == -1].sum() == -2:
                score += -2
            if block[id, :][block[id, :] == 1].sum() == 2:
                score += 2
            if block[id, :][block[id, :] == -1].sum() == -2:
                score += -2
    return score


def heuristic2(state):
    score = 0
    global_block = state.global_cells.reshape(3, 3)

    # print("global block:", global_block)
    for id in range(0, 3):
        if State.game_result(state, global_block) == 1:
            score += 15
        elif State.game_result(state, global_block) == -1:
            score += -15
        else:
            if global_block[:, id][global_block[:, id] == 1].sum() == 2:
                score += 4
            if global_block[:, id][global_block[:, id] == -1].sum() == -2:
                score += -4
            if global_block[id, :][global_block[id, :] == 1].sum() == 2:
                score += 4
            if global_block[id, :][global_block[id, :] == -1].sum() == -2:
                score += -4

            diag_left = np.diag(global_block)
            diag_right = np.diag(global_block[::-1])

            if diag_left[diag_left == 1].sum() == 2:
                score += 4
            if diag_left[diag_left == -1].sum() == -2:
                score += -4
            if diag_right[diag_right == 1].sum() == 2:
                score += 4
            if diag_right[diag_right == -1].sum() == -2:
                score += -4

    for ind, block in enumerate(state.blocks):
        is_win = False
        if State.game_result(state, block) == 1:
            score += 5
            is_win = True

        elif State.game_result(state, block) == -1:
            score += -5
            is_win = True

        if State.game_result(state, block) == 1 and ind == 4:
            score += 10
            is_win = True

        elif State.game_result(state, block) == -1 and ind == 4:
            score += -10
            is_win = True

        elif State.game_result(state, block) == 1 and ind in [0, 2, 6, 8]:
            score += 3
            is_win = True

        elif State.game_result(state, block) == -1 and ind in [0, 2, 6, 8]:
            score += -3
            is_win = True

        if not is_win:
            if state.previous_move.index_local_board == 4:
                # getting a square in center board is worth 3
                score += block[block == 1].sum() * 3
                score += block[block == -1].sum() * -3

            # getting a center square in any board is worth 3
            if block[1, 1] == 1:
                score += 3

            if block[1, 1] == -1:
                score += -3

            for id in range(0, 3):
                if block[:, id][block[:, id] == 1].sum() == 2:
                    score += 2
                if block[:, id][block[:, id] == -1].sum() == -2:
                    score += -2
                if block[id, :][block[id, :] == 1].sum() == 2:
                    score += 2
                if block[id, :][block[id, :] == -1].sum() == -2:
                    score += -2

            diag_topleft = np.diag(block)
            diag_topright = np.diag(block[::-1])

            if diag_topleft[diag_topleft == 1].sum() == 2:
                score += 2
            if diag_topleft[diag_topleft == -1].sum() == -2:
                score += -2
            if diag_topright[diag_topright == 1].sum() == 2:
                score += 2
            if diag_topright[diag_topright == -1].sum() == -2:
                score += -2
    return score


def heuristic1(state):
    score = 0
    global_block = state.global_cells.reshape(3, 3)

    # print("global block:", global_block)
    for id in range(0, 3):
        if State.game_result(state, global_block) == 1:
            score += 15
        elif State.game_result(state, global_block) == -1:
            score += -15
        else:
            if global_block[:, id][global_block[:, id] == 1].sum() == 2:
                score += 4
            if global_block[:, id][global_block[:, id] == -1].sum() == -2:
                score += -4
            if global_block[id, :][global_block[id, :] == 1].sum() == 2:
                score += 4
            if global_block[id, :][global_block[id, :] == -1].sum() == -2:
                score += -4

            diag_left = np.diag(global_block)
            diag_right = np.diag(global_block[::-1])

            if diag_left[diag_left == 1].sum() == 2:
                score += 4
            if diag_left[diag_left == -1].sum() == -2:
                score += -4
            if diag_right[diag_right == 1].sum() == 2:
                score += 4
            if diag_right[diag_right == -1].sum() == -2:
                score += -4

    block = state.blocks[state.previous_move.index_local_board]
    id_local = state.previous_move.index_local_board
    is_win = False

    if State.game_result(state, block) == 1:
        score += 5
        is_win = True

    elif State.game_result(state, block) == -1:
        score += -5
        is_win = True

    if State.game_result(state, block) == 1 and id_local == 4:
        score += 10
        is_win = True

    elif State.game_result(state, block) == -1 and id_local == 4:
        score += -10
        is_win = True

    elif State.game_result(state, block) == 1 and id_local in [0, 2, 6, 8]:
        score += 3
        is_win = True

    elif State.game_result(state, block) == -1 and id_local in [0, 2, 6, 8]:
        score += -3
        is_win = True
    if not is_win:
        if state.previous_move.index_local_board == 4:
            # getting a square in center board is worth 3
            score += block[block == 1].sum() * 3
            score += block[block == -1].sum() * -3

        # getting a center square in any board is worth 3
        if block[1, 1] == 1:
            score += 3

        if block[1, 1] == -1:
            score += -3

        for id in range(0, 3):
            if block[:, id][block[:, id] == 1].sum() == 2:
                score += 2
            if block[:, id][block[:, id] == -1].sum() == -2:
                score += -2
            if block[id, :][block[id, :] == 1].sum() == 2:
                score += 2
            if block[id, :][block[id, :] == -1].sum() == -2:
                score += -2

        diag_topleft = np.diag(block)
        diag_topright = np.diag(block[::-1])

        if diag_topleft[diag_topleft == 1].sum() == 2:
            score += 2
        if diag_topleft[diag_topleft == -1].sum() == -2:
            score += -2
        if diag_topright[diag_topright == 1].sum() == 2:
            score += 2
        if diag_topright[diag_topright == -1].sum() == -2:
            score += -2
    return score


def unbeatable_strategy(cur_state):
    valid_moves = cur_state.get_valid_moves

    if len(valid_moves) == 81:
        for move in valid_moves:
            if move.index_local_board == 4 and move.x == 1 and move.y == 1:
                return move

    if len(np.where(cur_state.blocks[4] == 0)[0]) > 0:
        for move in valid_moves:
            if move.x == 1 and move.y == 1:
                return move

    if len(np.where(cur_state.blocks[valid_moves[0].index_local_board] == 0)[0]) == 9:
        for move in valid_moves:
            if (move.x * 3 + move.y) == move.index_local_board:
                return move

    trap_board = []
    for id, block in enumerate(cur_state.blocks):
        if id == 4:
            continue
        if block[block == -1].sum() <= -1:
            trap_board.append(id)

    if len(trap_board) == 1:
        if cur_state.free_move:
            for move in valid_moves:
                if move.index_local_board == opp_site[trap_board[0]]:
                    if (move.x * 3 + move.y) == trap_board[0] and cur_state.blocks[opp_site[trap_board[0]]][
                        move.x, move.y] == 0:
                        return move
            for move in valid_moves:
                if (move.x * 3 + move.y) == opp_site[trap_board[0]] and move.index_local_board == opp_site[
                    trap_board[0]]:
                    return move
        for move in valid_moves:
            if (move.x * 3 + move.y) == trap_board[0]:
                return move
        for move in valid_moves:
            if (move.x * 3 + move.y) == opp_site[trap_board[0]]:
                return move

    if len(trap_board) == 2:
        if len(np.where(cur_state.blocks[trap_board[0]] == -1)[0]) > \
                len(np.where(cur_state.blocks[trap_board[1]] == -1)[0]):
            id1 = 0
        else:
            id1 = 1

        if len(np.where(cur_state.blocks[trap_board[id1]] == 0)[0]) > 0:
            for move in valid_moves:
                if (move.x * 3 + move.y) == trap_board[id1]:
                    return move
            for move in valid_moves:
                if (move.x * 3 + move.y) == opp_site[trap_board[id1]]:
                    return move
        else:
            for move in valid_moves:
                if (move.x * 3 + move.y) == trap_board[1 - id1]:
                    return move

    # if something's wrong, then using minimax ^^
    score, path = minimax1(cur_state, 2, float(-inf), float(inf), True)
    if cur_state in path:
        return path[cur_state]
    return np.random.choice(cur_state.get_valid_moves)


# def minimax(state, depth, player):
#     valid_moves = state.get_valid_moves
#     #print("valid moves:", valid_moves)
#     if depth == 0 or len(valid_moves) == 0:
#         # print("state_leaf:", state.blocks)
#         # print("score:",heuristic(state, player))
#         return heuristic1(state, player), None
#
#     best_score = float(-inf)
#     path = {}
#
#     for succ in valid_moves:
#         #print("state1:",state)
#         state_copy = copy.deepcopy(state)
#         state_copy.act_move(succ)
#         value = -minimax(state_copy, depth - 1, player)[0]
#         print("move:", succ)
#         print("score:", value)
#         if value > best_score:
#             best_score = value
#             path[state] = succ
#     return best_score, path

def minimax(state, depth, alpha, beta, maximizingPlayer):
    valid_moves = state.get_valid_moves
    # print("valid moves:", valid_moves)
    if depth == 0 or len(valid_moves) == 0:
        return heuristic1(state), {}

    path = {}
    if maximizingPlayer:
        max_score = float(-inf)

        for succ in valid_moves:
            # print("state1:",state)
            state_copy = copy.deepcopy(state)
            state_copy.act_move(succ)
            value = minimax(state_copy, depth - 1, alpha, beta, False)[0]
            # print("move:", succ)
            # print("score:", value)
            if value > max_score:
                max_score = value
                path[state] = succ
            alpha = max(alpha, value)
            if beta <= alpha:
                break

        return max_score, path
    else:
        min_score = float(inf)

        for succ in valid_moves:
            # print("state1:",state)
            state_copy = copy.deepcopy(state)
            state_copy.act_move(succ)
            value = minimax(state_copy, depth - 1, alpha, beta, True)[0]
            # print("move1:", succ)
            # print("score1:", value)
            if value < min_score:
                min_score = value
                path[state] = succ
            beta = min(beta, value)
            if beta <= alpha:
                break
        return min_score, path


def select_move(cur_state, remain_time):
    if cur_state.player_to_move == 1:
        return unbeatable_strategy(cur_state)
    else:
        score, path = minimax(cur_state, 2, float(-inf), float(inf), False)
        if cur_state in path:
            return path[cur_state]
        return np.random.choice(cur_state.get_valid_moves)
