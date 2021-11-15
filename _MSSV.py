import numpy as np
from math import inf
import copy
from state import State

opp_site = {0: 8, 8: 0, 1: 7, 7: 1, 2: 6, 6: 2, 3: 5, 5: 3}


def heuristic(state):
    valid_moves = state.get_valid_moves
    max_score = float(-inf)
    min_score = float(inf)
    for move in valid_moves:
        state_copy = copy.deepcopy(state)
        state_copy.act_move(move)
        score = 0
        win_game_score = 25
        two_in_sq_score1 = 5
        two_in_sq_score2 = 2
        win_board_score = 5
        win_center_board_score = 10
        win_corner_board_score = 3
        global_block = state_copy.global_cells.reshape(3, 3)

        def cal_2_in_sq_score(board, sq_score):
            val = 0
            for id in range(0, 3):
                # two board win in seq add 4 (row, col, dig)
                if (board[:, id][board[:, id] == 1].sum() == 2) \
                        and (board[:, id][board[:, id] == -1].sum() == 0):
                    val += sq_score
                if (board[:, id][board[:, id] == -1].sum() == -2) \
                        and (board[:, id][board[:, id] == 1].sum() == 0):
                    val += -sq_score
                if (board[id, :][board[id, :] == 1].sum() == 2) \
                        and (board[id, :][board[id, :] == -1].sum() == 0):
                    val += sq_score
                if (board[id, :][board[id, :] == -1].sum() == -2) \
                        and (board[id, :][board[id, :] == 1].sum() == 0):
                    val += -sq_score

            diag_left = np.diag(board)
            diag_right = np.diag(board[::-1])

            if (diag_left[diag_left == 1].sum() == 2) \
                    and (diag_left[diag_left == -1].sum() == 0):
                val += sq_score
            if (diag_left[diag_left == -1].sum() == -2) \
                    and (diag_left[diag_left == 1].sum() == 0):
                val += -sq_score
            if (diag_right[diag_right == 1].sum() == 2) \
                    and (diag_right[diag_right == -1].sum() == 0):
                val += sq_score
            if (diag_right[diag_right == -1].sum() == -2) \
                    and (diag_right[diag_right == 1].sum() == 0):
                val += -sq_score
            return val

        if State.game_result(state_copy, global_block) == 1:
            score += win_game_score
        elif State.game_result(state_copy, global_block) == -1:
            score += -win_game_score
        else:
            score += cal_2_in_sq_score(global_block, two_in_sq_score1)

            block = state_copy.blocks[state_copy.previous_move.index_local_board]
            id_local = state_copy.previous_move.index_local_board
            is_win = False

            # one board win add 5
            if State.game_result(state_copy, block) == 1:
                score += win_board_score
                is_win = True

            elif State.game_result(state_copy, block) == -1:
                score += -win_board_score
                is_win = True

            # win center board add 10
            if State.game_result(state_copy, block) == 1 and id_local == 4:
                score += win_center_board_score
                is_win = True

            elif State.game_result(state_copy, block) == -1 and id_local == 4:
                score += -win_center_board_score
                is_win = True

            # win corner board add 3
            elif State.game_result(state_copy, block) == 1 and id_local in [0, 2, 6, 8]:
                score += win_corner_board_score
                is_win = True

            elif State.game_result(state_copy, block) == -1 and id_local in [0, 2, 6, 8]:
                score += -win_corner_board_score
                is_win = True

            if not is_win:
                if id_local == 4:
                    # getting a square in center board is worth 3
                    if state_copy.player_to_move == -1:
                        score += 3
                    else:
                        score += -3

                # two tiles win in seq in small board add 2 (row, col, dig)
                score += cal_2_in_sq_score(block,two_in_sq_score2)
        if state.player_to_move == 1:
            if score > max_score:
                max_score = score
        else:
            if score < min_score:
                min_score = score
    return max_score if state.player_to_move == 1 else min_score


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
    score, path = minimax(cur_state, 2, float(-inf), float(inf), True)
    if cur_state in path:
        return path[cur_state]
    return np.random.choice(cur_state.get_valid_moves)


def minimax(state, depth, alpha, beta, maximizingPlayer):
    valid_moves = state.get_valid_moves
    if depth == 0 or len(valid_moves) == 0:
        return heuristic(state), {}

    path = {}
    if maximizingPlayer:
        max_score = float(-inf)

        for succ in valid_moves:
            state_copy = copy.deepcopy(state)
            state_copy.act_move(succ)
            value = minimax(state_copy, depth - 1, alpha, beta, False)[0]
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
            state_copy = copy.deepcopy(state)
            state_copy.act_move(succ)
            value = minimax(state_copy, depth - 1, alpha, beta, True)[0]
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
        validMoves = cur_state.get_valid_moves
        if len(validMoves) > 0:
            return np.random.choice(validMoves)
        return None
