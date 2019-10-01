from django.shortcuts import render, redirect
from . import sudoku_make
from .models import Sudoku
from .forms import SudokuForm
import datetime

# 基本画面
def home(request):
    if (request.method == 'POST'):
        sudoku_set = sudoku_make.create()
        Question = sudoku_set['question']
        Answer = sudoku_set['answer']
        Q_d = ','.join([''.join(map(str, row)) for row in Question])
        A_d = ','.join([''.join(map(str, row)) for row in Answer])
        # 時差
        DIFF_JST_FROM_UTC = 9
        Now_d = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
        sudoku = Sudoku(answer=A_d, question=Q_d, time=Now_d)
        sudoku.save()

    data = Sudoku.objects.all()
    params = {
        'title':'数独プロジェクト',
        'msg':'数独の問題です。createボタンで問題が追加されます。ただし10秒くらいかかることもあるので注意。そのときは読み込み中止してください。',
        'data': data,
    }
    return render(request, 'sudoku/home.html', params)

# 削除するか確かめる
def check_delete(request):
    password = 'isaka'
    params = {'title': 'Confirmation'}
    if (request.method == 'POST'):
        inputword = request.POST['inputword']
        print(inputword)
        if password == inputword:
            return render(request, 'sudoku/delete.html', params)
        else:
            print('error')
            params['error'] = 'パスワードが違います。'
            params['hint'] = 'ヒント：私の好きな作家の苗字です。'
    return render(request, 'sudoku/checkdelete.html', params)


# 削除
def delete(request):
    data = Sudoku.objects.all()
    if (request.method == 'POST'):
        data.delete()
        return redirect(to='/sudoku')
    param = {'title': 'Really Delete?'}
    return render(request, 'sudoku/delete.html', param)


# 問題を表から取ってきて表示
def question(request, num):
    Q_d = Sudoku.objects.get(id=num).question
    Question = [[int(num) for num in list(row_s)] for row_s in Q_d.split(',')]
    if (request.method == 'POST'):
        nums = request.POST.getlist('num')
        ind = 0
        print(nums)
        for r in range(9):
            for c in range(9):
                if Question[r][c] == 0:
                    Question[r][c] = int(nums[ind])
                    ind += 1
        return answer(request, num, Question)

    params = {
            'title': 'Question' + str(num),
            'msg':'問題です。一応人間が解けるような難易度ではあるはず。',
            'goto':'answer',
            'num': num,
            'next_num': num+1,
            'form': SudokuForm(),
            'q': True,
            'next': 'answer',
            'state':Question,
            'not_max': num+1 < Sudoku.objects.all().last().id,
            }
    return render(request, 'sudoku/index.html', params)


# 回答表示
def answer(request, num, state):
    A_d = Sudoku.objects.get(id=num).answer
    Answer = [[int(num) for num in list(row_s)] for row_s in A_d.split(',')]
    judge = True
    for i in range(9):
        for j in range(9):
            if state[i][j] != Answer[i][j]:
                judge = False
    not_Max = num < Sudoku.objects.all().last().id
    params = {
            'title': 'Answer' + str(num),
            'q': False,
            'state':Answer,
            'not_max': not_Max,
            'num': num,
        }
    if judge is False:
        params['msg'] = '間違いです！残念でした〜'
    else:
        params['msg'] = '正解です！すごい！天才！！'
    if not_Max:
        params['goto'] = 'question'
        params['next_num'] = num + 1
        params['next'] = 'next question'
    return render(request, 'sudoku/index.html', params)