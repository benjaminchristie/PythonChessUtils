import chess
from chess import engine
import stockfish
import os, time
import lichess
import lichess.api
from lichess.format import PYCHESS
import traceback
import requests

class GameAnalyzer:


	def __init__(self, game, depth=20, enginePath="C:/Users/Benjamin/Arena_3.5.1/Engines/Stockfish12/stockfish_20090216_x64_bmi2.exe", param=None):
		self.game = str(game)
		self.depth = int(depth)
		self.param = param
		self.auth = str(os.getenv("LICHESSAUTH"))
		#self.engine = stockfish.Stockfish(path=str(enginePath), depth=self.depth, param=self.param)
		self.engine = chess.engine.SimpleEngine.popen_uci(str(enginePath))
		self.playerColor = 0 # WHITE, 1 would be BLACK
		self.analyze(game)

	def analyze(self, game):
		actualGame = lichess.api.game(str(game), format=PYCHESS, auth=self.auth)
		board = actualGame.board()
		counter = 0 # even if it is white's move, odd if black's move
		cpl = 0
		ogEval = self.engine.analyze(board, chess.engine.Limit(depth=self.depth))
		ogCp = ogEval["score"].relative.cp
		for move in actualGame.mainline_moves():
			# clear screen
			os.system("cls") if os.name=="nt" else os.system("clear")
			beforeEval = self.engine.analyze(board, chess.engine.Limit(depth=self.depth))
			beforeCp = beforeEval["score"].relative.cp
			board.push(move)
			afterEval = self.engine.analyze(board, chess.engine.Limit(depth=self.depth))
			afterCp = afterEval["score"].relative.cp
			
			if 

			counter+=1
				
			cp = currEval["score"].relative.cp 
			





	def analyzePGN(self, pgn)





if __name__ == "__main__":
	try:
		game = str(input("Enter game url [ex: pwZxxYGly2TD] : "))
		Analyzer = GameAnalyzer(game)
	except:
		traceback.print_tb()