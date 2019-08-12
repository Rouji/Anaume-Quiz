#!/usr/bin/env python3

from flask import Flask, request, render_template, session, redirect, url_for
from json import load
from collections import defaultdict
from typing import NamedTuple
from random import choice
from os.path import dirname, join

class Question(NamedTuple):
    left: str
    right: str
    top: str
    bottom: str
    answer: str
    difficulty: str
    number: str

app = Flask(__name__)
app.config['SECRET_KEY'] = 'banana'


# load questions
questions = defaultdict(dict)
with open(join(dirname(__file__),'kuizu100.json'),'r') as f:
    for q in load(f):
        starting = [x[:1] for x in q['question'] if x.endswith('◯')]
        ending = [x[1:] for x in q['question'] if x.startswith('◯')]
        question = Question(
            left = starting[0],
            top = starting[1],
            right = ending[0],
            bottom = ending[1],
            answer = q['answer'],
            number = str(q['number']),
            difficulty = q['difficulty']
        )
        questions[question.difficulty][question.number] = question


@app.route('/<difficulty>/<number>', methods=['GET', 'POST'])
@app.route('/', defaults={'difficulty': None, 'number': None})
def index(difficulty, number):
    number = str(number) if number is not None else None

    # set difficulties
    if request.method == 'POST':
        session['difficulties'] = [d for d in questions.keys() if request.values.get('difficulty_'+d) != None]
    if len(session.get('difficulties', [])) < 1:
        session['difficulties'] = list(questions.keys())


    if request.method == 'POST':
        session['total'] = session.get('total', 0) + 1
        answer = request.form.get('answer', None)
        if answer and answer == request.form.get('correct_answer', None):
            session['correct'] = session.get('correct', 0) + 1
        session['last'] = questions[difficulty][number]._asdict()
        session['last_answer'] = answer
        difficulty = None
        number = None

    redir = False
    if not difficulty:
        difficulty = choice(session['difficulties'])
        redir = True
    if not number:
        number = choice(list(questions[difficulty].keys()))
        redir = True
    if redir:
        return redirect(f'/{difficulty}/{number}')

    return render_template(
        'index.html',
        question=questions[difficulty][number],
        difficulties_available=list(questions.keys()),
        session=session,
    )


if __name__ == "__main__":
    app.run(debug=True)
