import unittest
import client
import socket
import json


empty = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
four_turns = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[2,2,0,0,0,0,0],[1,1,0,0,0,0,0]]
player_one_close = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[2,2,2,0,0,0,0],[0,1,1,1,0,0,0]]
player_one_win = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[2,2,2,0,0,0,0],[0,1,1,1,1,0,0]]
almost_full = [[1,2,1,2,2,1,0],[2,2,1,1,2,1,2],[1,2,2,1,1,2,1],[2,1,2,1,1,2,2],[2,2,2,0,0,0,0],[1,1,1,0,0,0,0]]


class TestPrepareResponse(unittest.TestCase):
  def test_prepare_response_returns_a_valid_response(self):
    self.assertEqual(client.prepare_response({"column": 1}), '{"column": 1}\n')

class TestValidMoves(unittest.TestCase):
  def test_get_valid_moves(self):
    self.assertEqual(len(client.determine_valid_moves(empty)), 7)
    self.assertEqual(len(client.determine_valid_moves(almost_full)), 1)
    self.assertEqual(len(client.determine_valid_moves(four_turns)), 7)
    self.assertEqual(client.determine_valid_moves(almost_full), [[0, 6]])

class TestWinningMove(unittest.TestCase):
  def check_for_winner(self):
    self.assertEqual(client.is_won_board(1, player_one_win), True)
    self.assertEqual(client.is_won_board(2, player_one_win), False)
    self.assertEqual(client.is_won_board(1, empty), False)

class TestIsEmpty(unittest.TestCase):
  def test_prepare_response_returns_a_valid_response(self):
    self.assertEqual(client.check_empty(empty), True)
    self.assertEqual(client.check_empty(four_turns), False)

class TestSeanScore(unittest.TestCase):
  def test_sean_score(self):
    self.assertEqual(client.sean_score(empty, 1), 138)
    self.assertEqual(client.sean_score(four_turns, 1), 135)
    self.assertEqual(client.sean_score(player_one_win, 1), 141)

class TestNoahScore(unittest.TestCase):
  def test_sean_score(self):
    self.assertEqual(client.noah_score(empty, 1), 138)
    self.assertEqual(client.noah_score(four_turns, 1), 138)
    self.assertEqual(client.noah_score(player_one_win, 1), 143)
    self.assertEqual(client.noah_score(player_one_close, 1), 143)

class TestBlockWinner(unittest.TestCase):
  def test_block_winner(self):
    self.assertEqual(client.get_move(1, player_one_close), {"column": 4})



if __name__ == '__main__':
  unittest.main()