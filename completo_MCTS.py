# completo_MCTS.py

import numpy as np
import math
import random

class Connect4State:
    def __init__(self, width=7, height=6, board=None):
        self.playerJustMoved = 2
        self.winner = 0
        self.width = width
        self.height = height
        if board is None:
            self.InitializeBoard()
        else:
            self.board = board

    def InitializeBoard(self):
        self.board = np.zeros((self.height, self.width), dtype=int)

    def Clone(self):
        st = Connect4State(self.width, self.height)
        st.playerJustMoved = self.playerJustMoved
        st.winner = self.winner
        st.board = np.copy(self.board)
        return st

    def DoMove(self, movecol):
        assert 0 <= movecol < self.width and self.board[0, movecol] == 0
        row = np.max(np.where(self.board[:, movecol] == 0))
        self.playerJustMoved = 3 - self.playerJustMoved
        self.board[row, movecol] = self.playerJustMoved
        if self.DoesMoveWin(movecol, row):
            self.winner = self.playerJustMoved

    def GetMoves(self):
        if self.winner != 0:
            return []
        return [col for col in range(self.width) if self.board[0, col] == 0]

    def DoesMoveWin(self, col, row):
        me = self.board[row, col]
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for d in directions:
            count = 1
            for step in [-1, 1]:
                for i in range(1, 4):
                    r, c = row + d[0] * i * step, col + d[1] * i * step
                    if 0 <= r < self.height and 0 <= c < self.width and self.board[r, c] == me:
                        count += 1
                    else:
                        break
                if count >= 4:
                    return True
            if count >= 4:
                break
        return False

    def GetResult(self, playerJustMoved):
        return playerJustMoved == self.winner

    def IsGameOver(self):
        return self.GetMoves() == []

class Node:
    def __init__(self, move=None, parent=None, state=None):
        self.move = move
        self.parentNode = parent
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.GetMoves()
        self.playerJustMoved = state.playerJustMoved

    def UCTSelectChild(self):
        s = sorted(self.childNodes, key=lambda c: c.wins / c.visits + math.sqrt(2 * math.log(self.visits) / c.visits))[-1]
        return s

    def AddChild(self, move, state):
        node = Node(move=move, parent=self, state=state)
        self.untriedMoves.remove(move)
        self.childNodes.append(node)
        return node

    def Update(self, result):
        self.visits += 1
        self.wins += result

def UCT(rootstate, itermax, verbose=False):
    rootnode = Node(state=rootstate)
    for i in range(itermax):
        node = rootnode
        state = rootstate.Clone()
        while node.untriedMoves == [] and node.childNodes != []:
            node = node.UCTSelectChild()
            state.DoMove(node.move)
        if node.untriedMoves != []:
            m = random.choice(node.untriedMoves)
            state.DoMove(m)
            node = node.AddChild(m, state)
        while state.GetMoves() != []:
            state.DoMove(random.choice(state.GetMoves()))
        while node is not None:
            node.Update(state.GetResult(node.playerJustMoved))
            node = node.parentNode
    move = sorted(rootnode.childNodes, key=lambda c: c.wins / c.visits)[-1].move

    return move