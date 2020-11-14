import unittest
import client
import socket
import json

class TestPrepareResponse(unittest.TestCase):
  def test_prepare_response_returns_a_valid_response(self):
    self.assertEqual(client.prepare_response({"column": 1}), '{"column": 1}\n')

if __name__ == '__main__':
  init_test = {
    'player': '1',
    'maxTurnTime': 15000,
    'board': [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
  }
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect(('localhost', 8080))
  sock.sendall(json.loads(init_test).encode('utf-8'))
  unittest.main()
