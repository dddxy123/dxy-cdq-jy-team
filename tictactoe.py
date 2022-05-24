"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():                                                    #jy  part   基础九宫格生成
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],                                      #九宫格每一行由一个数组生成，board[i][j]代表了九宫格第i行第j列
            [EMPTY, EMPTY, EMPTY],                                      #board[i][j]是第i个数组的第j个元素
            [EMPTY, EMPTY, EMPTY]]


def player(board):                                                      #dxy part   判断当前为哪个玩家回合
    """
    Returns player who has the next turn on a board.
    """
    #计数初始化
    Xcount = 0
    Ocount = 0
    #对X和O进行记数
    for row in board:   # 统计棋盘上X和O的棋子数量
        Xcount += row.count(X)   # 将每行中的X棋子数加起来
        Ocount += row.count(O)   # 同上
    
    if Xcount <= Ocount:   # 若X棋子数量小于等于O，则当前为X的回合
        return X
    else:                  # 若X棋子数量大于O，则当前为O的回合
        return O


def actions(board):                                                     #dxy part   判决棋盘内所有可落子的位置
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possible_moves = set()   # 可以落子的位置，此处设了一个空集合，后续再不断add    set():创建一个无序不重复元素的集合

    for row_index, row in enumerate(board):   # 得到二维列表board中”行“的index(0or1or2)和value(每行有3个value)
        for column_index, item in enumerate(row):   # 得到board中对应行中”列“的index(0or1or2)和value(1个)
            if item == None:   # 如果当前行列下的坐标没有棋子，则 ↓
                possible_moves.add((row_index, column_index))   # 将该位置行与列的index保存到possible_moves集合中
    
    return possible_moves   # 返回棋盘上所有可以落子的位置


def result(board, action):                                              #dxy part   判决当前回合的玩家落子
    """
    Returns the board that results from making move (i, j) on the board.
    """
    player_move = player(board)   # 返回当前回合落子的玩家

    new_board = deepcopy(board)   # 将当前的board复制过来   此处由于board属于复杂对象(二维列表)，因此采用深复制来开辟新的内存空间
    i, j = action   # 当前玩家落子的坐标

    if board[i][j] != None:   # 如果落子位置不为空(有棋子)
        raise Exception       # 引发异常，raise后的语句不会执行，不做任何操作
    else:                     # 如果落子位置为空(无棋子)
        new_board[i][j] = player_move   # 在棋盘的[i,j]处落下当前回合玩家的棋子

    return new_board   # 返回更新后的棋盘


def winner(board):                                                      #jy  part   该函数用于对胜利者所满足的条件进行判决
    
    for player in (X, O):
        
        #第一个循环用于对每一行是否存在三个X/O进行判断
            for row in board:   
                if row == [player] * 3:                                 #row为board的三个数组中的某一个，在游戏中表现为行
                    return player                                       #返回胜利方符号

        #第二个循环用于对每一列是否存在三个X/O进行判断
            for i in range(0, 3):   
                column = [board[x][i] for x in range(3)]                #column为由三个数组的第i项按数组顺序构成的数组，在游戏中表为列
                if column == [player] * 3:
                    return player                                       #返回胜利方符号
        
        #第三个循环用于对对角线是否存在三个X/O进行判断
            if [board[i][i] for i in range(0, 3)] == [player] * 3:      #判断正对角线是否为存在三个X/O
                return player                                           #返回胜利方符号

            elif [board[i][2-i] for i in range(0, 3)] == [player] * 3:  #判断逆对角线是否存在三个X/O
                return player                                           #返回胜利方符号
    return None                                                         #没有胜者条件（游戏未结束或平局）下返回None
                               

def terminal(board):                                                    #jy  part   用于判断游戏是否结束
    """
    Returns True if game is over, False otherwise.
    """
    # game is won by one of the players
    if winner(board) != None:                                           #对winner函数的返回值进行判断，若有胜者则判定游戏结束
        return True

    # moves still possible
    for row in board:
        if EMPTY in row:                                                #存在未下的空，判定对局未结束
            return False

    # no possible moves
    return True                                                         #所有的空都已经下完，判定对局结束


def utility(board):                                                     #jy  part   判决函数，对winner函数的返回值进行判断并返回相应函数值
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    win_player = winner(board)

    if win_player == X:
        return 1
    elif win_player == O:
        return -1
    else:
        return 0

#敌对搜索，X是让value最大，O是让value最小
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
#在X的每个下法action中,找到让O的下法（ation）值(value)最大的那个
    def max_value(board):
        optimal_move = ()
        #两个函数相互嵌套，出口就是游戏结束
        if terminal(board):
            return utility(board), optimal_move
        else:
            v = -5 #X赢的局面定义为-5
            for action in actions(board):
                minval = min_value(result(board, action))[0]
                if minval > v:
                    v = minval
                    optimal_move = action
            return v, optimal_move
#在O的每个下法action中,找到让X的下法（ation）值(value)最小的那个
    def min_value(board):
        optimal_move = ()
        #两个函数相互嵌套，出口就是游戏结束
        if terminal(board):
            return utility(board), optimal_move
        else:
            v = 5 # O赢的局面定义为5
            for action in actions(board):
                maxval = max_value(result(board, action))[0]
                if maxval < v:
                    v = maxval
                    optimal_move = action
            return v, optimal_move

    curr_player = player(board)
#判断游戏是否结束，结束就返回
    if terminal(board):
        return None
#根据当前player选择执行的函数
    if curr_player == X:
        return max_value(board)[1]

    else:
        return min_value(board)[1]

