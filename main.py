from state import State, State_2
import time
from importlib import import_module

  
def main(player_X, player_O, rule = 1):
    dict_player = {1: 'X', -1: 'O'}
    if rule == 1:
        cur_state = State()
    else:
        cur_state = State_2()
    turn = 1    

    limit = 81
    remain_time_X = 120
    remain_time_O = 120
    
    player_1 = import_module(player_X)
    player_2 = import_module(player_O)
    
    
    while turn <= limit:
        #print("turn:", turn, end='\n\n')
        if cur_state.game_over:
            return cur_state.player_to_move * -1
            # print("winner:", dict_player[cur_state.player_to_move * -1])
            # break
        
        start_time = time.time()
        if cur_state.player_to_move == 1:
            new_move = player_1.select_move(cur_state, remain_time_X)
            elapsed_time = time.time() - start_time
            remain_time_X -= elapsed_time
        else:
            new_move = player_2.select_move(cur_state, remain_time_O)
            elapsed_time = time.time() - start_time
            remain_time_O -= elapsed_time
            
        if new_move == None:
            # break
            return [0, cur_state.count_X, cur_state.count_O]

        
        if remain_time_X < 0 or remain_time_O < 0:
            print("out of time")
            print("winner:", dict_player[cur_state.player_to_move * -1])
            break
                
        if elapsed_time > 10.0:
            print("elapsed time:", elapsed_time)
            print("winner: ", dict_player[cur_state.player_to_move * -1])
            break
        #print("move", new_move)
        cur_state.act_move(new_move)
        #print(cur_state)
        
        turn += 1

    return [0, cur_state.count_X, cur_state.count_O]
    # print("X:", cur_state.count_X)
    # print("O:", cur_state.count_O)
winList = []
num_game = 1000
for i in range(0,num_game):
    result = main('_MSSV','random_agent')
    #result = main('random_agent','_MSSV',)

    if result in [1, -1]:
        winList.append(result)
    else:
        #print(result)
        if result[1] > result[2]:
            winList.append(2)
        elif result[2] > result[1]:
            winList.append(-2)

print("Number of X win:", winList.count(1))
print("Number of O win:", winList.count(-1))
print("win rate X:", winList.count(1)/num_game)
print("win rate O:", winList.count(-1)/num_game)
print("Number of X raw:", winList.count(2))
print("Number of O raw:", winList.count(-2))

#main('random_agent','_MSSV',)

