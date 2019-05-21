

import sys
import copy

ALPHABET = ['a', 'b', 'c', '1', '.', '+', '*']
SYMBOLS = ['a', 'b', 'c']


def error():
    print("ERROR")
    sys.exit()


def infinity():
    print("INF")
    sys.exit()


def success(value):
    print(value)
    sys.exit()


class State(object):
    def __init__(self, start_v, finish_v):
        self.start = start_v
        self.finish = finish_v


class Edge(object):
    def __init__(self, to, sym):
        self.to = to
        self.sym = sym


class Automaton(object):
    def __init__(self, gr, start, finish):
        self.gr = gr
        self.start = start
        self.finish = finish


def build_automaton(s):
    s = list(s)
    gr = []
    stack = []

    v_now = 0
    for i in range(len(s)):
        if s[i] not in ALPHABET:
            error()
        elif s[i] == '*':
            if len(stack) < 1:
                error()
            gr.append([])
            gr[v_now].append(Edge(stack[-1].start, ''))
            v_now += 1
            gr.append([])
            gr[stack[-1].finish].append(Edge(v_now, ''))
            v_now += 1
            gr[stack[-1].start].append(Edge(stack[-1].finish, ''))
            gr[stack[-1].finish].append(Edge(stack[-1].start, ''))
            stack[-1].start = v_now - 2
            stack[-1].finish = v_now - 1
        elif s[i] == '+':
            if len(stack) < 2:
                error()
            gr.append([])
            gr[v_now].append(Edge(stack[-2].start, ''))
            gr[v_now].append(Edge(stack[-1].start, ''))
            stack[-2].start = v_now
            v_now += 1
            gr[stack[-2].finish].append(Edge(v_now, ''))
            gr[stack[-1].finish].append(Edge(v_now, ''))
            stack[-2].finish = v_now
            v_now += 1
            gr.append([])
            stack.pop()
        elif s[i] == '1':
            stack.append(State(v_now, v_now + 1))
            gr.extend([[Edge(v_now + 1, '')], []])
            v_now += 2
        elif s[i] == '.':
            if len(stack) < 2:
                error()
            gr[stack[-2].finish].append(Edge(stack[-1].start, ''))
            stack[-2].finish = stack[-1].finish
            stack.pop()
        else:
            stack.append(State(v_now, v_now + 1))
            gr.extend([[Edge(v_now + 1, s[i])], []])
            v_now += 2
    if len(stack) != 1:
        error()
    return Automaton(gr, stack[-1].start, stack[-1].finish)


def build_reverse_automaton(automaton):
    rev_gr = [[] for _ in range(len(automaton.gr))]
    rev_start = automaton.finish
    rev_finish = automaton.start
    for i in range(len(automaton.gr)):
        for e in automaton.gr[i]:
            rev_gr[e.to].append(Edge(i, e.sym))
    return Automaton(rev_gr, rev_start, rev_finish)


def dfs(v, gr, used):
    used[v] = True
    ret_set = set()
    ret_set.add(v)
    for e in gr[v]:
        if used[e.to]:
            continue
        if e.sym == '':
            ret_set.update(dfs(e.to, gr, used))
    return ret_set


def traversal_by_empty_edges(gr, start_poses):
    used = [False for _ in range(len(gr))]
    for v in start_poses:
        used[v] = True
    ret_set = copy.deepcopy(start_poses)
    for v in start_poses:
        ret_set.update(dfs(v, gr, used))
    return ret_set


def find_suf_by_len(gr, start_poses, allowed_transitions):  # one iteration of bfs
    new_start_poses = set()
    for v in start_poses:
        for e in gr[v]:
            if e.sym in allowed_transitions:
                new_start_poses.add(e.to)
    return traversal_by_empty_edges(gr, new_start_poses)


def solve():
    data = input()
    # data = "acb..bab.c.*.ab.ba.+.+*a. a 2"
    # data = "ab+c.aba.*.bac.+.+* b 2"
    # data = "ab.c*. c 2"
    # data = "bcca..*.* c 0"
    data = data.split(' ')
    data = [value for value in data if value != '']
    if len(data) < 3:
        error()
    s = data[0]
    x = data[1]
    if len(x) != 1 or x not in SYMBOLS:
        error()
    k = int(data[2])
    automaton = build_automaton(s)
    rev_auto = build_reverse_automaton(automaton)
    suf_poses = set()
    suf_poses.add(rev_auto.start)
    suf_poses = traversal_by_empty_edges(rev_auto.gr, suf_poses)
    ans_len = 0
    for _ in range(k):
        ans_len += 1
        suf_poses = find_suf_by_len(rev_auto.gr, suf_poses, [x])
        if len(suf_poses) == 0:
            infinity()

    while len(suf_poses) > 0:
        if rev_auto.finish in suf_poses:
            success(ans_len)
        suf_poses = find_suf_by_len(rev_auto.gr, suf_poses, SYMBOLS)
        ans_len += 1
    infinity()


if __name__ == "__main__":
    solve()
