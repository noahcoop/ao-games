#!/usr/bin/python

import sys
import json
import socket
import numpy as np

NUM_ROWS = 6
NUM_COLS = 7

def check_empty(board):
  """Checks if no moves have been made on the board"""
  board = np.array(board)
  return board.min() == 0

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

def get_optimal_move(player, board, valid_moves):
  # If we can win, return the column that makes us win
  # If opponent can win next turn, then try to block opponent
  pass

def is_winning_move(player, board, row, column):
    #check valid moves to see if any are winning moves
    #vertical/horizon/diagonal
    #Horizontal
    #need to handle out of bounds
    if column <= 3 and [row][column + 1] == player and [row][column + 2] == player and [row][column + 3] == player:
      return True
          
    elif column >= 3 and [row][column - 1] == player and [row][column - 2] == player and [row][column - 3] == player:
      return True
          
    elif (column >= 1 and column <= 4) and [row][column - 1] == player and [row][column + 1] == player and [row][column + 1] == player:
      return True
    
    elif (column >= 2 and column <= 5) and [row][column + 1] == player and [row][column - 1] == player and [row][column - 2] == player:
      return True
    
    #Vertical
    elif (row >= 2) and [row + 1][column] == player and [row + 2][column] == player and [row + 3][column] == player:
      return True
    #Diagonal
    elif column <= 3 and row >= 2 and [row + 1][column + 1] == player and [row + 2][column + 2] == player and [row + 3][column + 3] == player:
      return True
    elif column <= 3 and row >= 2 and [row - 1][column - 1] == player and [row - 2][column - 2] == player and [row - 3][column - 3] == player:
      return True
    #to do 2 or more cases for diagonal
  
    
def get_move(player, board):
  # TODO determine if board is empty
  if check_empty(board):
    return {"column": 3}

  # TODO determine valid moves
  valid_moves = determine_valid_moves(board)
  
  # TODO determine best move
  return {"column": 1}

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
