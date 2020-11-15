#!/usr/bin/python

import sys
import json
import socket
import math
import numpy as np
from copy import deepcopy

NUM_ROWS = 6
NUM_COLS = 7

evaluationTable = [[3, 4, 5, 7, 5, 4, 3], 
                  [4, 6, 8, 10, 8, 6, 4],
                  [5, 8, 11, 13, 11, 8, 5], 
                  [5, 8, 11, 13, 11, 8, 5],
                  [4, 6, 8, 10, 8, 6, 4],
                  [3, 4, 5, 7, 5, 4, 3]]

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


def minimax(board, depth, alpha, beta, maximizePlayer, player):
  opp = 2
  if player == 2:
    opp = 1

  valid_moves = determine_valid_moves(board)
  player_win = is_won_board(player, board)
  opp_win = is_won_board(opp, board)

  if player_win:
    return None, math.inf
  elif opp_win:
    return None, -math.inf
  elif len(valid_moves) == 0:
    return None, 0
  if depth == 0:
    turn = np.count_nonzero(np.array(board))
    if turn >= 15:
      return None, noah_score(board, player)
    else:
      return None, sean_score(board, player)

  if maximizePlayer:
    value = -math.inf
    column = valid_moves[0][1]
    for row, col in valid_moves:
      temp_board = deepcopy(board)
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
      temp_board = deepcopy(board)
      temp_board[row][col] = opp
      new_score = minimax(temp_board, depth - 1, alpha, beta, True, player)[1]
      if new_score < value:
        value = new_score
        column = col
      beta = min(beta, value)
      if beta <= alpha:
        break
    return column, value


def sean_score(board, player):
  opp = 2
  if player == 2:
    opp = 1

  score = 138
  total = 0
  for i in range(NUM_ROWS):
    for j in range(NUM_COLS):
      if (board[i][j] == player):
        total += evaluationTable[i][j]
      elif (board[i][j] == opp):
        total -= evaluationTable[i][j]
  # check if the move will win and if so give it a huge score
  return score + total


def noah_score(board, player):
  score = 0
  normalizing_factor = 138

  for c in range(NUM_COLS-3):
    for r in range(NUM_ROWS):
      player_count = 0
      opp_count = 0
      empty_count = 0
      for i in range(4):
        if board[r][c + i] == 0:
          empty_count += 1
        elif board[r][c + i] == player:
          player_count += 1
        else:
          opp_count += 1

      if player_count == 3 and empty_count == 1:
        score += 5
      if player_count == 2 and empty_count == 2:
        score += 2
      if opp_count == 3 and empty_count == 1:
        score -= 5
      if opp_count == 2 and empty_count == 2:
        score -= 2
      

  for c in range(NUM_COLS):
    for r in range(NUM_ROWS-3):
      for i in range(4):
        player_count = 0
        opp_count = 0
        empty_count = 0
        for i in range(4):
          if board[r + i][c] == 0:
            empty_count += 1
          elif board[r + i][c] == player:
            player_count += 1
          else:
            opp_count += 1

        if player_count == 3 and empty_count == 1:
          score += 5
        if player_count == 2 and empty_count == 2:
          score += 2
        if opp_count == 3 and empty_count == 1:
          score -= 5
        if opp_count == 2 and empty_count == 2:
          score -= 2

  for c in range(NUM_COLS-3):
    for r in range(NUM_ROWS-3):
      for i in range(4):
        player_count = 0
        opp_count = 0
        empty_count = 0
        for i in range(4):
          if board[r + i][c + i] == 0:
            empty_count += 1
          elif board[r + i][c + i] == player:
            player_count += 1
          else:
            opp_count += 1

        if player_count == 3 and empty_count == 1:
          score += 5
        if player_count == 2 and empty_count == 2:
          score += 2
        if opp_count == 3 and empty_count == 1:
          score -= 5
        if opp_count == 2 and empty_count == 2:
          score -= 2

  for c in range(NUM_COLS-3):
    for r in range(3, NUM_ROWS):
      for i in range(4):
        player_count = 0
        opp_count = 0
        empty_count = 0
        for i in range(4):
          if board[r - i][c + i] == 0:
            empty_count += 1
          elif board[r - i][c + i] == player:
            player_count += 1
          else:
            opp_count += 1

        if player_count == 3 and empty_count == 1:
          score += 5
        if player_count == 2 and empty_count == 2:
          score += 2
        if opp_count == 3 and empty_count == 1:
          score -= 5
        if opp_count == 2 and empty_count == 2:
          score -= 2

  return score + normalizing_factor


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


def get_move(player, board):
  # Determine if board is empty
  if check_empty(board):
    return {"column": 3}

  # Determine valid moves
  valid_moves = determine_valid_moves(board)

  # Determine if any of the valid moves are winning moves
  for row, col in valid_moves:
    board[row][col] = player
    if is_won_board(player, board):
      return {"column": col}
    else:
      board[row][col] = 0

  opp = 2
  if player == 2:
    opp = 1

  for row, col in valid_moves:
    board[row][col] = opp
    if is_won_board(opp, board):
      return {"column": col}
    else:
      board[row][col] = 0

  # Looking depth turns ahead
  turn = np.count_nonzero(np.array(board))
  depth = 4
  if turn > 10 and turn < 20:
    depth = 5
  elif turn >= 20:
    depth = 6

  column, score = minimax(board, depth, -math.inf, math.inf, True, player)
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
      # print(player, maxTurnTime, board)

      move = get_move(player, board)
      response = prepare_response(move)
      sock.sendall(response.encode('utf-8'))
  finally:
    sock.close()
