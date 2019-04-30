from . import sudoku_solve
import random
import copy
import time


def blank_state():
    # make a state with all blank 0
    state = []
    for _ in range(9):
        state.append([0] * 9)
    return state


def create_completed_state():
    # make a comleted state
    # takes a few seconds
    state = blank_state()
    row = 0
    while row in range(7):
        num_list = random.sample(UP_LIST, 9)
        check = True
        for num in num_list:
            check = check and sudoku_solve.follow_rules(state, row, num_list.index(num), num)
        if check:
            state[row] = num_list
            row += 1
    # complete remained blanks
    state = complete_last2_row(state)
    
    return state


def complete_last2_row(state):
    # complete the last row
    search_list = []
    for column in range(9):
        column_list = UP_LIST[:]
        for row_list in state:
            if row_list[column] != 0:
                column_list.remove(row_list[column])
        search_list.append({'row': 7 ,'column': column, 'num_prob': column_list})
        search_list.append({'row': 8 ,'column': column, 'num_prob': column_list})   
    return sudoku_solve.simulate(state, search_list)



def delete_nums(state, remain_list, keep_count=0, count_lim=10):
    # delete numbers from state
    pre_state = copy.deepcopy(state)
    
    delete = random.choice(remain_list)
    row = delete['row']
    column = delete['column']
    state[row][column] = 0
    
    com_state = copy.deepcopy(state)
    up_answer_dic = sudoku_solve.solve(state, UP_LIST)
    down_answer_dic = sudoku_solve.solve(state, DOWN_LIST)
    
    up_answer = up_answer_dic['state']
    down_answer = down_answer_dic['state']
    simulated = up_answer_dic['simulated']

    if up_answer == down_answer and not simulated:
        # if only one pattern can be answer
        remain_list.remove(delete)
        for_return = delete_nums(com_state, remain_list)
    elif keep_count > count_lim:
        for_return = pre_state
    else:
        for_return = delete_nums(pre_state, remain_list, keep_count + 1)
        
    return for_return




UP_LIST = list(range(1, 10))
DOWN_LIST = list(range(9, 0, -1))


def create():
    
    start_time = time.time()
    
    answer = create_completed_state()
            
    create_time = time.time()
    print(create_time - start_time, 'seconds to create answer')
    
    remain_list = []
    for row in range(9):
        for column in range(9):
            remain_list.append({'row': row, 'column': column})
            
    question = delete_nums(answer, remain_list)
    
    question_time = time.time()
    print(question_time - create_time, 'seconds to make question')
    
    return {'question': question, 'answer': answer}
        
        
    
if __name__ == '__main__':
    
    sudoku_set = create()
    
    question = sudoku_set['question']
    answer = sudoku_set['answer']
    
    print('question is:')
    for row in question:
        print(row)
    
    print('answer is:')
    for row in answer:
        print(row)