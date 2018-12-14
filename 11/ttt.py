import re
import json
import socket
import http.client
from http import HTTPStatus
from urllib import parse
from urllib import request as rq
from urllib.error import HTTPError, URLError
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
from sys import argv


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


class TicTacToeHandler(BaseHTTPRequestHandler):
    """handle TicTacToe"""
 
    mimetype = 'application/json'
    games = dict()
    index = -1 

    def do_GET(self):
        url = self.path
        print(url)

        mode, params = url.split('?')
        mode = re.sub('^\W*', '', mode)  
        params = parse.parse_qs(params)  
        try:
            request = getattr(self, mode) 
            request(params)
        except AttributeError:
            self.send_error(HTTPStatus.BAD_REQUEST, f"Asking for a non-existent request '{mode}'.")

    def start(self, params):
        try:
            if 'name' not in params:
                raise KeyError
            name = params['name'][0]
            new_game = {'name': name,
                        'board': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                        'next': 1,
                        'winner': None}
            TicTacToeHandler.index += 1  
            TicTacToeHandler.games[TicTacToeHandler.index] = new_game
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-type', self.mimetype)
            self.end_headers()
            self.wfile.write(bytes(json.dumps({'id': TicTacToeHandler.index}), 'utf-8'))
        except KeyError:
            self.send_error(HTTPStatus.BAD_REQUEST, "Unknown parameter, expecting 'name'.")

    def status(self, params):
        try:
            if 'game' not in params:
                raise KeyError
            try:
                idx = int(params['game'][0])
                game = self.games[idx]
                self.send_response(HTTPStatus.OK)
                self.send_header('Content-type', self.mimetype)
                self.end_headers()
                if game['winner']:
                    result = {'winner': game['winner']}
                else:
                    result = {'board': game['board'], 'next': game['next']}
                self.wfile.write(bytes(json.dumps(result), 'utf-8'))
            except ValueError:
                self.send_error(HTTPStatus.BAD_REQUEST, "The game parameter expects its value ID to be numeric.")
            except (KeyError, IndexError):
                self.send_error(HTTPStatus.BAD_REQUEST, "Entered an ID of a non-existent game.")
        except KeyError:
            self.send_error(HTTPStatus.BAD_REQUEST, "Unknown parameter, expecting 'game'.")
    def decide_winner(board):
        """Who won"""

        for i in range(3):
            row = board[i]
            player = row[0]  
            if row[1] == player and row[2] == player:
                return player  
        
        for i in range(3):
            col = board[:, i]
            player = col[0]  
            if col[1] == player and col[2] == player:
                return player  
        
        dia1 = [board[0][0], board[1][1], board[2][2]]
        dia2 = [board[0][2], board[1][1], board[2][0]]
        for dia in [dia1, dia2]:
            player = dia[0]  
            if dia[1] == player and dia[2] == player:
                return player  
        flatten = lambda l: [item for sublist in l for item in sublist]
        if 0 in flatten(board):
            return None  
        else:
            return 0  


if len(argv) != 2:
    exit("The program expects to be called with one command-line argument:\n"
         "./ttt.py 9001")
PORT = argv[1]
try:
    PORT = int(PORT)
except ValueError:
    exit("The PORT number must be a valid integer.")

server = ThreadedHTTPServer(('', PORT), TicTacToeHandler)  
try:
    print(f'Started httpserver on port {PORT}.')
    server.serve_forever() 

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()

    def play(self, params):
        try:
            idx = int(params['game'][0])
            player = int(params['player'][0])
            row = int(params['x'][0])
            column = int(params['y'][0])
            game = TicTacToeHandler.games[idx]

            result = dict()
            result['status'] = 'bad'  
            result['message'] = 'Unknown state.'
            if game['next'] != player:
                result['message'] = f"It's not currently player {player}'s turn.'"
            elif game['board'][row][column] != 0:
                result['message'] = f"The required field is not blank."
            elif row not in range(0, 2) or column not in range(0, 2):
                result['message'] = "The given coordinates are out of the game board."
            elif game['winner'] is not None:
                result['message'] = "The game already has a winner."
            else:
                result['status'] = 'ok'
                game['board'][row][column] = player
                game['next'] = 1 if player == 2 else 2 
                game['winner'] = self.decide_winner(game['board'])

            self.send_response(HTTPStatus.OK)
            self.send_header('Content-type', self.mimetype)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(result), 'utf-8'))
        except ValueError:
            self.send_error("Some of the passed parameters aren't numeric.")
        except TypeError:
            self.send_error("Some of the required parameters for 'play' are missing.")
        except (KeyError, IndexError):
            self.send_error(HTTPStatus.BAD_REQUEST, "Entered an ID of a non-existent game.")



