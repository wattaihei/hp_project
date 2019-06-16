from django.shortcuts import render
from . import sudoku_make
import csv
import time


def question(request):
    t0 = time.time()
    sudoku_set = sudoku_make.create()
    t1 = time.time()
    delta = round(t1 - t0, 2)
    Question = sudoku_set['question']
    Answer = sudoku_set['answer']
    
    params = {
            'title': 'Question',
            'msg':'数独の問題です。更新すると問題が変わります。',
            'time': '{0} seconds to create question'.format(delta),
            'msg2':'注意：読み込みに10秒ほどかかることがあります。ボタンを押してから問題を作っているので。本当はデータベースに収納して〜ってやりたい。',
            'goto':'answer',
            'state':Question,
            }
    with open('answer_memory', 'wt') as f:
        csvout = csv.writer(f)
        csvout.writerows(Answer)
    return render(request, 'sudoku/index.html', params)

def answer(request):
    with open('answer_memory', 'rt') as f:
        cin = csv.reader(f)
        Answer = [row for row in cin]
    params = {
            'title': 'Answer',
            'msg':'解答です。',
            'msg2':'注意：読み込みに10秒ほどかかることがあります。ボタンを押してから問題を作っているので。本当はデータベースに収納して〜ってやりたい。',
            'goto':'next question',
            'state':Answer,
            }
    return render(request, 'sudoku/index.html', params)
 