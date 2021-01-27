import chess
from chess import engine
import stockfish
import os, time
import lichess
import lichess.api
from lichess.format import PYCHESS
import traceback
import requests
import chess.pgn

class GameAnalyzer:


	def __init__(self, game=None, file=None, pgn=None, time=2, depth=30, enginePath="C:/Users/Benjamin/Arena_3.5.1/Engines/Stockfish12/stockfish_20090216_x64_bmi2.exe", param=None):
		self.game = str(game)[0:8]
		self.depth = int(depth)
		self.time = time
		self.param = param
		self.auth = str(os.getenv("LICHESSAUTH"))
		#self.engine = stockfish.Stockfish(path=str(enginePath), depth=self.depth, param=self.param)
		self.engine = chess.engine.SimpleEngine.popen_uci(str(enginePath))
		self.playerColor = chess.WHITE


	def analyzeLichessURL(self, url):
		print("Importing game {}...".format(game))
		actualGame = lichess.api.game(str(game), format=PYCHESS, auth=self.auth)
		self.analyze(actualGame)

	def analyzeFile(self, file):
		pgn = open(file)
		self.analyzePGN(pgn)

	def analyzePGN(self, pgn):
		print("Importing game...")
		actualGame = chess.pgn.read_game(pgn)
		self.analyze(actualGame)


	# GAME must be a game object from chess
	def analyze(self, game):
		actualGame = game
		board = actualGame.board()
		ply = 0 # even if it is white's move, odd if black's move
		cpl = 0
		blackCpl = 0
		beforeEval = self.engine.analyse(board, chess.engine.Limit(time=self.time))
		beforeCp = beforeEval["score"].pov(chess.WHITE)
		for move in actualGame.mainline_moves():
			# clear screen
			os.system("cls") if os.name=="nt" else os.system("clear")
			if beforeCp.is_mate():
				print("{} vs. {}".format(actualGame.headers["White"], actualGame.headers["Black"]))
				print("{} | {}".format(actualGame.headers["WhiteElo"], actualGame.headers["BlackElo"]))
				print("\n{}: {}\n".format("White" if board.turn else "Black", str("M" + str(beforeEval["score"].relative.mate()))))
				print("Ply : {}".format(str(ply+1)))
			else:	
				print("{} vs. {}".format(actualGame.headers["White"], actualGame.headers["Black"]))
				print("{} | {}".format(actualGame.headers["WhiteElo"], actualGame.headers["BlackElo"]))
				print("\n{}: {}\n".format("White" if board.turn else "Black", str(beforeEval["score"].relative.cp / 100)))
				print("Ply : {}".format(str(ply+1)))
				print("cpls: " + str(blackCpl) + " " + str(cpl))
			board.push(move)
			print(board)
			afterEval = self.engine.analyse(board, chess.engine.Limit(time=self.time))
			afterCp = afterEval["score"].pov(chess.WHITE)

			if board.turn == chess.WHITE and not afterCp.is_mate() and not beforeCp.is_mate():
				# opponent just moved
				blackCpl = blackCpl + min(beforeCp.cp - afterCp.cp, 0)

			elif board.turn != chess.WHITE and not afterCp.is_mate() and not beforeCp.is_mate():
				# player just moved
				cpl = cpl + max(0, beforeCp.cp - afterCp.cp)
			else:
				pass

			beforeEval = afterEval
			beforeCp = afterCp
			ply+=1

		print("Nice Game!")
		acpl = cpl / (0.5 * ply)
		oppAcpl = -blackCpl / (0.5 * ply)
		print("White ACPL : " + str(acpl))
		print("Black ACPL : " + str(oppAcpl))
		time.sleep(10)
		

if __name__ == "__main__":
	try:
		game = str(input("Enter game url [ex: pwZxxYGly2TD] : "))
		if game=="no":
			game = str(input("Enter full path to pgn with BACK slashes : "))
			Analyzer = GameAnalyzer(pgn=game)
			Analyzer.analyzeFile(game)
		else:
			Analyzer = GameAnalyzer(game=game)
			Analyzer.analyze(game)
	except:
		traceback.print_exc()