#!/usr/bin/env python3
from bs4 import BeautifulSoup as bs
from requests import get
from json import dump
from sys import stderr
import multiprocessing as mp

diffs = {
    'easy': 218,
    'normal': 218,
    'hard': 218,
    'berry_hard': 101
}

def proc_diff(diff: str, n: int):
    print(f'processing {diff}:{n}', file=stderr)
    req=get(f'https://kanji.kuizu100.net/anaume/{diff}/{n}.html')
    soup = bs(req.content.decode('utf-8', 'ignore'), 'html.parser')
    q = soup.find('p', {'class': 'question_text'}).text
    a = soup.find('div', {'class': 'answer_box'}).find('span').text
    # q: "□→質　□→策計→□　絵→□"
    return {
        'difficulty': diff,
        'number': n,
        'question':
        [
            f'◯{q[2]}',
            f'◯{q[6]}',
            f'{q[7]}◯',
            f'{q[11]}◯',
        ],
        'answer': a,
    }


def args(diffs):
    for k, v in diffs.items():
        for n in range(1, v+1):
            yield k,n


with mp.Pool(processes = 10) as p:
    res = p.starmap(proc_diff, args(diffs))
    with open('kuizu100.json', 'w') as f:
        dump([
            r for r in res if r is not None
        ], f)
