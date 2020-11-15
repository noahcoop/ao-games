#!/usr/bin/python

import sys
import json
import socket
import math
import numpy as np

NUM_ROWS = 6
NUM_COLS = 7

evaluationTable = [[3, 4, 5, 7, 5, 4, 3], 
                  [4, 6, 8, 10, 8, 6, 4],
                  [5, 8, 11, 13, 11, 8, 5], 
                  [5, 8, 11, 13, 11, 8, 5],
                  [4, 6, 8, 10, 8, 6, 4],
                  [3, 4, 5, 7, 5, 4, 3]];

def check_empty(board):
  """Checks if no moves have been made on the board"""
  board = np.array(board)
  return board.max() == 0

def determine_valid_moves(board):
  """Returns a list of up to 7 moves a player can make"""
  valid_moves = []
  for col in range(NUM_COLS):
    if board[0][col] == 0:
      for row in range(NUM_ROWS):
        if board[row][col] != 0:
          valid_moves.append([row - 1, col])
          break
        if row == NUM_ROWS - 1 and board[row][col] == 0:
          valid_moves.append([row,col])

            
  return valid_moves


def is_won_board(player, board):
  for c in range(NUM_COLS-3):
	  for r in range(NUM_ROWS):
		  if board[r][c:c+4] == [player, player, player, player]:
			  return True

  for c in range(NUM_COLS):
	  for r in range(NUM_ROWS-3):
		  if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player and board[r+3][c] == player:
			  return True

  for c in range(NUM_COLS-3):
    for r in range(NUM_ROWS-3):
      if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player:
        return True

  for c in range(NUM_COLS-3):
    for r in range(3, NUM_ROWS):
      if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player:
        return True

  return False

def find_score(board, player):
  
        if player == 1:
          opp = 2
        else:
          opp = 1
        score = 128;
        sum = 0;
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                if (board[i][j] == player):
                    sum += evaluationTable[i][j];
                elif (board[i][j] == opp):
                    sum -= evaluationTable[i][j];
        return score + sum;

def minimax(board, depth, alpha, beta, maximizePlayer, player):
  opp = 2
  if player == 2:
    opp = 1

  valid_moves = determine_valid_moves(board)
  current_winner = is_won_board(player, board)
  if len(valid_moves) == 0 or current_winner != 0:
    # TODO - base case, return the score of the current board
    return None, 0
  if depth == 0:
    # TODO - return the score of the current board
    return None, 0

  if maximizePlayer:
    value = -math.inf
    column = valid_moves[0][1]
    for row, col in valid_moves:
      temp_board = board.copy()
      temp_board[row][col] = player
      new_score = minimax(temp_board, depth - 1, alpha, beta, False, player)[1]
      if new_score > value:
        value = new_score
        column = col
      alpha = max(alpha, value)
      if alpha >= beta:
        break
    return column, value
  else:
    value = math.inf
    column = valid_moves[0][1]
    for row, col in valid_moves:
      temp_board = board.copy()
      temp_board[row][col] = opp
      new_score = minimax(temp_board, depth - 1, alpha, beta, True, player)[1]
      if new_score > value:
        value = new_score
        column = col
      beta = min(beta, value)
      if beta <= alpha:
        break
    return column, value




def is_winning_move(player, board, row, column):
    '''Checks move to see if it is a winning move'''

    #Horizontal
    if column <= 3 and board[row][column + 1] == player and board[row][column + 2] == player and board[row][column + 3] == player:
      return True
          
    elif column >= 3 and board[row][column - 1] == player and board[row][column - 2] == player and board[row][column - 3] == player:
      return True
          
    elif (column >= 1 and column <= 4) and board[row][column - 1] == player and board[row][column + 1] == player and board[row][column + 1] == player:
      return True
    
    elif (column >= 2 and column <= 5) and board[row][column + 1] == player and board[row][column - 1] == player and board[row][column - 2] == player:
      return True
    
    #Vertical
    elif (row <= 2) and board[row + 1][column] == player and board[row + 2][column] == player and board[row + 3][column] == player:
      return True
  
    #Diagonal
    elif column <= 3 and row <= 2 and board[row + 1][column + 1] == player and board[row + 2][column + 2] == player and board[row + 3][column + 3] == player:
      return True
  
    elif column >= 3 and row >= 2 and board[row - 1][column - 1] == player and board[row - 2][column - 2] == player and board[row - 3][column - 3] == player:
      return True

    # TODO - Add remaining diagonal cases
    return False
  
    
def get_move(player, board):
  # Determine if board is empty
  if check_empty(board):
    return {"column": 3}

  # Determine valid moves
  valid_moves = determine_valid_moves(board)

  # Determine if any of the valid moves are winning moves
  for row, col in valid_moves:
    temp_board = board.copy()
    temp_board[row][col] = player
    if is_won_board(player, temp_board):
      return {"column": col}

  opp = 2
  if player == 2:
    opp = 1

  for row, col in valid_moves:
    temp_board = board.copy()
    temp_board[row][col] = opp
    if is_won_board(opp, temp_board):
      return {"column": col}
  
  # Looking 5 turns ahead
  column, score = minimax(board, 10, -math.inf, math.inf, True, player)
  print(score)
  return {"column": column}


def prepare_response(move):
  response = '{}\n'.format(json.dumps(move))
  print('sending {!r}'.format(response))
  return response

if __name__ == "__main__":
  port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 1337
  host = sys.argv[2] if (len(sys.argv) > 2 and sys.argv[2]) else socket.gethostname()

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    sock.connect((host, port))
    while True:
      data = sock.recv(1024)
      if not data:
        print('connection to server closed')
        break
      json_data = json.loads(str(data.decode('UTF-8')))
      board = json_data['board']
      maxTurnTime = json_data['maxTurnTime']
      player = json_data['player']
      print(player, maxTurnTime, board)

      move = get_move(player, board)
      response = prepare_response(move)
      sock.sendall(response.encode('utf-8'))
  finally:
    sock.close()
