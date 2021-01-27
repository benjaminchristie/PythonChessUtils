import chess
from chess import engine
import stockfish
import os, time, sys
import lichess
import lichess.api
from lichess.format import PYCHESS
import traceback
import requests
import chess.pgn

from gameAnalyzer import GameAnalyzer


class ManyGameAnalyser(GameAnalyzer):
	pass

class SimpleGame():

	def __init__(self, result=None, acplW=None, acplB=None, pgn=None, blackName='', whiteName=''):
		self.result = result
		self.acplW = acplW
		self.acplB = acplB
		self.pgn = pgn
		self.whiteName = whiteName
		self.blackName = blackName

	def getACPLW(self):
		return self.acplW

	def getACPLB(self):
		return self.acplB

	def getPGN(self):
		return self.pgn

	def getBlack(self):
		return self.blackName

	def getWhite(self):
		return self.whiteName


def main(username="threeisthree"):
	games = []
	totalaverage = 0
	c = 0
	userGames = list(lichess.api.user_games(str(username), max=50, format=PYCHESS, auth=str(os.getenv("LICHESSAUTH"))))
	for game in userGames:
		ga = GameAnalyzer(game=game, enginePath="/home/benjamin/personal/stockfish_20090216_x64_avx2", time=5, depth=20)
		acplw, acplb = ga.analyzeself()
		sg = SimpleGame(result=game.headers["Result"], acplW=acplw, acplB=acplb, pgn=game, blackName=game.headers["Black"], whiteName=game.headers["White"])
		games.append(sg)
		totalaverage = totalaverage + (acplw if game.headers["White"]==str(username) else acplb)
		c+=1
	return totalaverage / c

if __name__== "__main__":
	print(main())
	os._exit(os.EX_OK)

else:
	pass
