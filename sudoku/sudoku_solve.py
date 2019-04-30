import copy

def match_row(state, row, column, num):
    # 行に同じ数字なし
    for x in state[row]:
        if x == num:
            return False
    return True


def match_column(state, row, column, num):
    # 列に同じ数字なし
    check_list = []
    for row in state:
        check_list.append(row[column])
    for x in check_list:
        if x == num:
            return False
    return True


def match_block(state, row, column, num):
    # ブロックに同じ数字なし
    block_index = realize_block(row, column)
    for block in block_index:
        if state[block[0]][block[1]] == num:
            return False
    return True


def follow_rules(state, row, column, num):
    # ルールに従うかどうかチェックする
    return match_row(state, row, column, num) \
        and match_column(state, row, column, num) \
        and match_block(state, row, column, num)


def block_index():
    # ブロックを作る
    index_list = []
    block_index = [[0, 1, 2], [3, 4, 5], [6, 7 ,8]]
    for row_index in block_index:
        for column_index in block_index:
            pair = []
            for x in row_index:
                for y in column_index:
                    pair.append([x, y])
            index_list.append(pair)
    return index_list


def realize_block(row, column):
    # どのblockか判断する
    for block_index in BLOCK_INDEX:
        if [row, column] in block_index:
            return block_index
    

def check_block(state, block, num, search_list):
    # blockの数字を決める
    check_index = []
    for index in search_list:
        row = index['row']
        column = index['column']
        if [row, column] in block \
        and match_row(state, row, column, num) \
        and match_column(state, row, column, num):
            check_index.append(index)
    if len(check_index) == 1:
        state[check_index[0]['row']][check_index[0]['column']] = num
        search_list.remove(index)


def simulate(state, search_list, list_index=0 ,num_index=0, simulate_list=[]):
    # substitute number from search_list and simulate
    # remember by simulate_list
    copy_state = copy.deepcopy(state)
    copy_list = copy.deepcopy(search_list)
    
    
    blank = copy_list[list_index]
    
    row = blank['row']
    column = blank['column']
    num_prob = blank['num_prob']
    
    num = num_prob[num_index]
    copy_state[row][column] = num
    
    played = play(copy_state, copy_list)

    if played:
        if not 'search_list' in played.keys():            
            return played['state']
        else:
            # if in infinite loop
            simulate_list.append({'state': state, 'search_list': search_list,
                                  'list_index': list_index, 'num_index': num_index,
                                  'num': num})
            for_return = simulate(played['state'], played['search_list'], 0, 0, simulate_list)
    else:
        # if False back to previous state
        if len(num_prob) > num_index + 1:
            for_return = simulate(state, search_list, list_index, num_index + 1, simulate_list)
        else:
            # derive the previous information
            for_return = back_to_state(simulate_list)
    return for_return


def back_to_state(simulate_list):
    # back to previous state
    pre_list = simulate_list.pop()
            
    state = pre_list['state']
    search_list = pre_list['search_list']
    list_index = pre_list['list_index']
    num_index = pre_list['num_index']

    num_prob = search_list[list_index]['num_prob']
    
    if len(num_prob) > num_index + 1:
        for_return = simulate(state, search_list, list_index, num_index + 1, simulate_list)
    else:
        for_return = back_to_state(simulate_list)
    return for_return




def play(state, search_list):
    # fill in blank if other number cannot
    while search_list:
        pre_search_list = copy.deepcopy(search_list)

        
        for blank in search_list[:]:

            row = blank['row']
            column = blank['column']

            # うまるところは埋め、埋まらなかったら候補のリストを作成
            if state[row][column] != 0:
                search_list.remove(blank)
            
            else:
                true_num = []

                for x in blank['num_prob']:
                    if follow_rules(state, row, column, x):
                        true_num.append(x)

                if len(true_num) == 1:
                    # fill in blank if other number cannot
                    state[row][column] = true_num[0]
                    search_list.remove(blank)
                elif len(true_num) == 0:
                    # if in contradiction
                    return False
                else:
                    # if more than one number can be in blank go to next blank
                    state[row][column] = 0
                    blank['num_prob'] = true_num

                

        if pre_search_list == search_list:
            # if in loop return with search_list
            played_dic = {'state': state, 'search_list': search_list}
            return played_dic
 
    # if completed return without search_list
    played_dic = {'state': state}
    return played_dic
    


UP_LIST = list(range(1, 10))
DOWN_LIST = list(range(9, 0, -1))
BLOCK_INDEX = block_index()

question = [[0, 0, 5, 4, 0, 0, 9, 1, 8],
            [0, 0, 8, 0, 9, 2, 0, 0, 0],
            [3, 0, 0, 0, 0, 8, 0, 0, 0],
            [0, 0, 0, 7, 0, 5, 0, 0, 0],
            [0, 5, 0, 9, 0, 0, 0, 7, 0],
            [4, 0, 0, 0, 0, 1, 5, 2, 0],
            [0, 8, 0, 0, 3, 0, 6, 0, 0],
            [0, 1, 9, 0, 6, 0, 4, 0, 0],
            [2, 0, 0, 0, 0, 0, 8, 0, 0]]




def solve(init_state, num_list):
    state = init_state
    
    search_list = []
    for x in range(9):
        for y in range(9):
            search_list.append({'row': x, 'column': y, 'num_prob': num_list})
    # numbers that can be in (x, y)

    played = play(state, search_list)
    
    answer = {}
    if not 'search_list' in played.keys():
        answer['state'] = played['state']
        answer['simulated'] = False
    else:
        answer['state'] = simulate(played['state'], played['search_list'])
        answer['simulated'] = True
    return answer
    



if __name__ == '__main__':
    up_answer = solve(question, UP_LIST)['state']
    down_answer = solve(question, DOWN_LIST)['state']
    
    if solve(question, UP_LIST)['simulated']:
        print('simulation is used')
    
    if up_answer == down_answer:
        print('answer is:')
        for row in up_answer:
            print(row)
    else:
        print('more than one pattern is possible!!')
