from django.shortcuts import render
from .forms import SortForm
import random
from urllib.request import urlopen, Request
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import re
import time

def get_words():
    # wikibedia日本語版からランダムでページに飛び、その単語を取得する
    URL = 'https://ja.wikipedia.org/wiki/Special:Random'

    html = urlopen(URL).read().decode('utf-8')

    soup = BeautifulSoup(html, 'html.parser')
    first_passage = soup.p # 最初の説明の部分
    try:
        ans = first_passage.b.string # 最初の太文字になってるところ
    except AttributeError:
        return False, False #'単語習得に失敗しました'
    print(ans)
    try:
        m = re.search('[\(（][\u30A1-\u30F4\u3041-\u3093a-zA-Z 0-9]*[、）\)]', str(first_passage))
        word = m.group()
        return word[1:-1], ans
    except AttributeError:
        if re.match('[\u30A1-\u30F4\u3041-\u3093a-zA-Z 0-9]*', ans): # 太文字がいい感じになってたらこれを問題にしちゃう
            return ans, ans
        return False, False #'綺麗なページじゃなかったよ'
    

def make_question():
    while True:
        word, ans = get_words()
        if word is False: # ダメならもう一回
            print('one more time...')
            time.sleep(1)
        else:
            break
    question_list = list(word)
    random.shuffle(question_list)
    question = ''.join(question_list)
    return word, question, ans


def Question(request):
    if request.method == 'POST':
        # POST時の処理
        input_word = request.POST['text']
        with open('sort_question.txt', 'r', encoding='utf-8') as f:
            # 答えを読み込む
            a = f.read()
            word, question, ans = a.rstrip().split(',')
        params = {
                'question': question,
                'form': SortForm(request.POST),
            }
        print(input_word)
        if word == input_word: # 正解
            params['message'] = 'すごい！天才！'
            params['answer'] = word
            params['kanji'] = ans
            params['URL'] = 'https://ja.wikipedia.org/wiki/' + ans
            return render(request,'sort/answer.html', params)

        params['message'] = 'ざんねーん！'
        return render(request, 'sort/question.html', params)
    
    word, question, ans = make_question()
    # 作ったものを保存しておく
    with open('sort_question.txt', 'w', encoding='utf-8') as fw:
        fw.write(','.join([word, question, ans]))
    
    params = {
        'question': question,
        'form': SortForm(),
    }
    return render(request, 'sort/question.html', params)


def Answer(request):
    with open('sort_question.txt', 'r', encoding='utf-8') as f:
        # 答えを読み込む
        a = f.read()
        word, question, ans = a.rstrip().split(',')
    URL = 'https://ja.wikipedia.org/wiki/' + ans
    params = {
        'question': question,
        'answer': word,
        'kanji': ans,
        'URL': URL,
    }
    return render(request, 'sort/answer.html', params)
