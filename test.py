import unittest
import client
import socket
import json


empty = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
four_turns = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[2,2,0,0,0,0,0],[1,1,0,0,0,0,0]]
player_one_close = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[2,2,2,0,0,0,0],[0,1,1,1,0,0,0]]
almost_full = [[1,2,1,2,2,1,0],[2,2,1,1,2,1,2],[1,2,2,1,1,2,1],[2,1,2,1,1,2,2],[2,2,2,0,0,0,0],[1,1,1,0,0,0,0]]


class TestPrepareResponse(unittest.TestCase):
  def test_prepare_response_returns_a_valid_response(self):
    self.assertEqual(client.prepare_response({"column": 1}), '{"column": 1}\n')

class TestValidMoves(unittest.TestCase):
  def test_get_valid_moves(self):
    self.assertEqual(len(client.determine_valid_moves(empty)), 7)
    self.assertEqual(len(client.determine_valid_moves(almost_full)), 1)
    self.assertEqual(len(client.determine_valid_moves(four_turns)), 7)

class TestWinningMove(unittest.TestCase):
  def test_prepare_response_returns_a_valid_response(self):
    self.assertEqual(client.get_move(1, player_one_close), {"column": 4})

if __name__ == '__main__':
  unittest.main()