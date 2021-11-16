'''
MIT License

Copyright (c) 2019 Eric C. Joyce

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

##############################################################################
###                          O  T  H  E  L  L  O                           ###
##############################################################################

# Indices
#  56  57  58  59  60  61  62  63
#  48  49  50  51  52  53  54  55
#  40  41  42  43  44  45  46  47
#  32  33  34  35  36  37  38  39
#  24  25  26  27  28  29  30  31
#  16  17  18  19  20  21  22  23
#   8   9  10  11  12  13  14  15
#   0   1   2   3   4   5   6   7

class GameState:
	#  GameState constructor. If not given a list, default to the starting position.
	def __init__(self, board=None, whoAmI=None):
		if board == None:
			self.board = ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', \
	                      'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', \
	                      'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', \
	                      'e', 'e', 'e', 'B', 'W', 'e', 'e', 'e', \
	                      'e', 'e', 'e', 'W', 'B', 'e', 'e', 'e', \
	                      'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', \
	                      'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', \
	                      'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e']
		else:
			self.board = board

		if whoAmI == None:
			self.whoAmI = 'b'
		else:
			self.whoAmI = whoAmI

	#  Make the move and apply all the flips.
	#  A move is bipartite: an index and a character, 'B' or 'W'
	def makeMove(self, move, team=None, b=None):
		if b == None:
			b = self.board
		if team == None:
			team = self.whoAmI

		b[move] = team.upper()
		victims = self.getVictims(move, b)
		for v in victims:
			b[v] = team.upper()

		return b

	#  Assuming that the offending disc has already been placed
	def getVictims(self, move, b=None):
		if b == None:
			b = self.board

		victims = []

		victims += self.uSet(move, 'STOP_SAME', b)
		victims += self.dSet(move, 'STOP_SAME', b)
		victims += self.lSet(move, 'STOP_SAME', b)
		victims += self.rSet(move, 'STOP_SAME', b)
		victims += self.ulSet(move, 'STOP_SAME', b)
		victims += self.urSet(move, 'STOP_SAME', b)
		victims += self.dlSet(move, 'STOP_SAME', b)
		victims += self.drSet(move, 'STOP_SAME', b)

		return victims

	#  Return a list of indices where 'team' can place a disc
	def getMoves(self, team=None, b=None):
		if team == None:
			team = self.whoAmI
		if b == None:
			b = self.board

		moves = []

		for ctr in range(0, 64):
			if (self.isBlack(ctr, b) and team == 'b') or (self.isWhite(ctr, b) and team == 'w'):
				buff = self.uSet(ctr, 'STOP_EMPTY', b)
				if len(buff) > 0 and buff[-1] not in moves:
					moves.append( buff[-1] )
				buff = self.dSet(ctr, 'STOP_EMPTY', b)
				if len(buff) > 0 and buff[-1] not in moves:
					moves.append( buff[-1] )
				buff = self.lSet(ctr, 'STOP_EMPTY', b)
				if len(buff) > 0 and buff[-1] not in moves:
					moves.append( buff[-1] )
				buff = self.rSet(ctr, 'STOP_EMPTY', b)
				if len(buff) > 0 and buff[-1] not in moves:
					moves.append( buff[-1] )
				buff = self.ulSet(ctr, 'STOP_EMPTY', b)
				if len(buff) > 0 and buff[-1] not in moves:
					moves.append( buff[-1] )
				buff = self.urSet(ctr, 'STOP_EMPTY', b)
				if len(buff) > 0 and buff[-1] not in moves:
					moves.append( buff[-1] )
				buff = self.drSet(ctr, 'STOP_EMPTY', b)
				if len(buff) > 0 and buff[-1] not in moves:
					moves.append( buff[-1] )
				buff = self.dlSet(ctr, 'STOP_EMPTY', b)
				if len(buff) > 0 and buff[-1] not in moves:
					moves.append( buff[-1] )

		return moves

	################################################  Game end testing
	#  Black wins:  1
	#  White wins: -1
	#  Neither:     0
	#  Draw:     	2
	def isWin(self, b=None):
		if b == None:
			b = self.board

		if self.terminal(b):
			bc = len(self.getBlack(b))
			wc = len(self.getWhite(b))

			if bc > wc:
				return 1
			elif wc > bc:
				return -1
			return 2

		return 0

	#  Is the board in an end-state, regardless of who won?
	def terminal(self, b=None):
		if b == None:
			b = self.board

		return len(self.getMoves('w', b)) == 0 and len(self.getMoves('b', b)) == 0

	################################################  Board identities
	def isEmpty(self, index, b=None):
		if b == None:
			b = self.board
		return b[index] == 'e'

	def isBlack(self, index, b=None):
		if b == None:
			b = self.board
		return b[index] == 'B'

	def isWhite(self, index, b=None):
		if b == None:
			b = self.board
		return b[index] == 'W'

	#  Return a list of all indices occupied by Black discs
	def getBlack(self, b=None):
		if b == None:
			b = self.board
		return [x for x in range(0, 64) if self.isBlack(x, b)]

	#  Return a list of all indices occupied by White discs
	def getWhite(self, b=None):
		if b == None:
			b = self.board
		return [x for x in range(0, 64) if self.isWhite(x, b)]

	#  Do the discs at 'i' and 'j' belong to the same team?
	#  (Notice that empties are ignored)
	def sameSide(self, i, j, b=None):
		if b == None:
			b = self.board
		if (self.isBlack(i, b) and self.isBlack(j, b)) or (self.isWhite(i, b) and self.isWhite(j, b)):
			return True
		return False

	#  Do the discs at 'i' and 'j' belong to opposite teams?
	#  (Notice that empties are ignored)
	def opposed(self, i, j, b=None):
		if b == None:
			b = self.board
		if (self.isBlack(i, b) and self.isWhite(j, b)) or (self.isWhite(i, b) and self.isBlack(j, b)):
			return True
		return False

	#  Return a symbol indicating the team of the given index
	def getTeam(self, i, b=None):
		if b == None:
			b = self.board
		if isBlack(i, b):
			return 'b'
		if isWhite(i, b):
			return 'w'
		return 'e'

	#  Return a list of all Black discs occupying non-edge and non-X squares
	def getBlackCenter(self, b=None):
		if b == None:
			b = self.board
		return [x for x in self.getBlack(b) if not self.isX(x) and self.row(x) != 0 and self.row(x) != 7 and self.col(x) != 0 and self.col(x) != 0]

	#  Return a list of all White discs occupying non-edge and non-X squares
	def getWhiteCenter(self, b=None):
		if b == None:
			b = self.board
		return [x for x in self.getWhite(b) if not self.isX(x) and self.row(x) != 0 and self.row(x) != 7 and self.col(x) != 0 and self.col(x) != 0]

	#  Return a list of all Black discs occupying edge or X squares
	def getBlackEdges(self, b=None):
		if b == None:
			b = self.board
		return [x for x in self.getBlack(b) if self.isX(x) or self.row(x) == 0 or self.row(x) == 7 or self.col(x) == 0 or self.col(x) == 0]

	#  Return a list of all White discs occupying edge or X squares
	def getWhiteEdges(self, b=None):
		if b == None:
			b = self.board
		return [x for x in self.getWhite(b) if self.isX(x) or self.row(x) == 0 or self.row(x) == 7 or self.col(x) == 0 or self.col(x) == 0]

	################################################  Set Builders
	def uSet(self, index, validStop, b=None):
		if b == None:
			b = self.board

		buff = []
		validSet = False
		dst = self.u(index)

		while dst >= 0:
			if self.opposed(index, dst, b):
				buff.append(dst)
				dst = self.u(dst)
			elif validStop == 'STOP_SAME' and self.sameSide(index, dst, b):
				validSet = True
				break
			elif validStop == 'STOP_EMPTY' and self.isEmpty(dst, b):
				if len(buff) > 0:
					buff.append(dst)
					validSet = True
				break
			else:
				break

		if not validSet:
			buff = []

		return buff

	def dSet(self, index, validStop, b=None):
		if b == None:
			b = self.board

		buff = []
		validSet = False
		dst = self.d(index)

		while dst >= 0:
			if self.opposed(index, dst, b):
				buff.append(dst)
				dst = self.d(dst)
			elif validStop == 'STOP_SAME' and self.sameSide(index, dst, b):
				validSet = True
				break
			elif validStop == 'STOP_EMPTY' and self.isEmpty(dst, b):
				if len(buff) > 0:
					buff.append(dst)
					validSet = True
				break
			else:
				break

		if not validSet:
			buff = []

		return buff

	def lSet(self, index, validStop, b=None):
		if b == None:
			b = self.board

		buff = []
		validSet = False
		dst = self.l(index)

		while dst >= 0:
			if self.opposed(index, dst, b):
				buff.append(dst)
				dst = self.l(dst)
			elif validStop == 'STOP_SAME' and self.sameSide(index, dst, b):
				validSet = True
				break
			elif validStop == 'STOP_EMPTY' and self.isEmpty(dst, b):
				if len(buff) > 0:
					buff.append(dst)
					validSet = True
				break
			else:
				break

		if not validSet:
			buff = []

		return buff

	def rSet(self, index, validStop, b=None):
		if b == None:
			b = self.board

		buff = []
		validSet = False
		dst = self.r(index)

		while dst >= 0:
			if self.opposed(index, dst, b):
				buff.append(dst)
				dst = self.r(dst)
			elif validStop == 'STOP_SAME' and self.sameSide(index, dst, b):
				validSet = True
				break
			elif validStop == 'STOP_EMPTY' and self.isEmpty(dst, b):
				if len(buff) > 0:
					buff.append(dst)
					validSet = True
				break
			else:
				break

		if not validSet:
			buff = []

		return buff

	def ulSet(self, index, validStop, b=None):
		if b == None:
			b = self.board

		buff = []
		validSet = False
		dst = self.ul(index)

		while dst >= 0:
			if self.opposed(index, dst, b):
				buff.append(dst)
				dst = self.ul(dst)
			elif validStop == 'STOP_SAME' and self.sameSide(index, dst, b):
				validSet = True
				break
			elif validStop == 'STOP_EMPTY' and self.isEmpty(dst, b):
				if len(buff) > 0:
					buff.append(dst)
					validSet = True
				break
			else:
				break

		if not validSet:
			buff = []

		return buff

	def urSet(self, index, validStop, b=None):
		if b == None:
			b = self.board

		buff = []
		validSet = False
		dst = self.ur(index)

		while dst >= 0:
			if self.opposed(index, dst, b):
				buff.append(dst)
				dst = self.ur(dst)
			elif validStop == 'STOP_SAME' and self.sameSide(index, dst, b):
				validSet = True
				break
			elif validStop == 'STOP_EMPTY' and self.isEmpty(dst, b):
				if len(buff) > 0:
					buff.append(dst)
					validSet = True
				break
			else:
				break

		if not validSet:
			buff = []

		return buff

	def drSet(self, index, validStop, b=None):
		if b == None:
			b = self.board

		buff = []
		validSet = False
		dst = self.dr(index)

		while dst >= 0:
			if self.opposed(index, dst, b):
				buff.append(dst)
				dst = self.dr(dst)
			elif validStop == 'STOP_SAME' and self.sameSide(index, dst, b):
				validSet = True
				break
			elif validStop == 'STOP_EMPTY' and self.isEmpty(dst, b):
				if len(buff) > 0:
					buff.append(dst)
					validSet = True
				break
			else:
				break

		if not validSet:
			buff = []

		return buff

	def dlSet(self, index, validStop, b=None):
		if b == None:
			b = self.board

		buff = []
		validSet = False
		dst = self.dl(index)

		while dst >= 0:
			if self.opposed(index, dst, b):
				buff.append(dst)
				dst = self.dl(dst)
			elif validStop == 'STOP_SAME' and self.sameSide(index, dst, b):
				validSet = True
				break
			elif validStop == 'STOP_EMPTY' and self.isEmpty(dst, b):
				if len(buff) > 0:
					buff.append(dst)
					validSet = True
				break
			else:
				break

		if not validSet:
			buff = []

		return buff

	################################################  Board logic
	def u(self, index):
		if index >= 0:
			if self.row(index + 8) == self.row(index) + 1:
				return index + 8
		return -1

	def d(self, index):
		if index >= 0:
			if (self.row(index - 8) == self.row(index) - 1) and self.row(index) > 0:
				return index - 8
		return -1

	def l(self, index):
		if index >= 0:
			if self.row(index - 1) == self.row(index):
				return index - 1
		return -1

	def r(self, index):
		if index >= 0:
			if self.row(index + 1) == self.row(index):
				return index + 1
		return -1

	def ul(self, index):
		if index >= 0:
			if self.row(index + 7) == self.row(index) + 1:
				return index + 7
		return -1

	def ur(self, index):
		if index >= 0:
			if self.row(index + 9) == self.row(index) + 1:
				return index + 9
		return -1

	def dl(self, index):
		if index >= 0:
			if self.row(index - 9) == self.row(index) - 1:
				return index - 9
		return -1

	def dr(self, index):
		if index >= 0:
			if self.row(index - 7) == self.row(index) - 1:
				return index - 7
		return -1

	def col(self, a):
		if (a >= 0) and (a < 64):
			return a % 8
		return -1

	def row(self, a):
		if (a >= 0) and (a < 64):
			return (a - (a % 8)) / 8
		return -1

	#  Return a sorted list of indices along a lower-left to upper-right line
	#  through the given index.
	def getForwardSlash(self, index):
		buff = []

		a = self.dl(index)
		while a >= 0:
			buff.append(a)
			a = self.dl(a)

		a = self.ur(index)
		while a >= 0:
			buff.append(a)
			a = self.ur(a)

		return sorted(buff)

	#  Return a sorted list of indices along a lower-right to upper-left line
	#  through the given index.
	def getBackSlash(self, index):
		buff = []

		a = self.dr(index)
		while a >= 0:
			buff.append(a)
			a = self.dr(a)

		a = self.ul(index)
		while a >= 0:
			buff.append(a)
			a = self.ul(a)

		return sorted(buff)

	#  Return a sorted list of indices along the column of the given index.
	def getCol(self, index):
		c = self.col(index)
		if c == 0:
			i = 0
			j = 57
		elif c == 1:
			i = 1
			j = 58
		elif c == 2:
			i = 2
			j = 59
		elif c == 3:
			i = 3
			j = 60
		elif c == 4:
			i = 4
			j = 61
		elif c == 5:
			i = 5
			j = 62
		elif c == 6:
			i = 6
			j = 63
		else:
			i = 7
			j = 64

		return [x for x in range(i, j, 8)]

	#  Return a sorted list of indices along the row of the given index.
	def getRow(self, index):
		r = self.row(index)
		if r == 0:
			i = 0
			j = 8
		elif r == 1:
			i = 8
			j = 16
		elif r == 2:
			i = 16
			j = 24
		elif r == 3:
			i = 24
			j = 32
		elif r == 4:
			i = 32
			j = 40
		elif r == 5:
			i = 40
			j = 48
		elif r == 6:
			i = 48
			j = 56
		else:
			i = 56
			j = 64

		return [x for x in range(i, j)]

	################################################  Square types
	#      . C A B B A C .
	#      C X . . . . X C
	#      A . . . . . . A
	#      B . . . . . . B
	#      B . . . . . . B
	#      A . . . . . . A
	#      C X . . . . X C
	#      . C A B B A C .

	def X(self):
		return [9, 14, 49, 54]

	def isX(self, index):
		return index in self.X()

	def C(self):
		return [1, 6, 8, 15, 48, 55, 57, 62]

	def isC(self, index):
		return index in self.C()

	def B(self):
		return [3, 4, 24, 31, 32, 39, 59, 60]

	def isB(self, index):
		return index in self.B()

	def A(self):
		return [2, 5, 16, 23, 40, 47, 58, 61]

	def isA(self, index):
		return index in self.A()

	def isEdge(self, index):
		r = self.row(index)
		c = self.col(index)
		return r == 0 or r == 7 or c == 0 or c == 7

	def isCorner(self, index):
		return index == 0 or index == 7 or index == 56 or index == 63

	#  No square roots, no lookup tables: on a square game board,
	#  when it is possible to move diagonally, two pieces are always
	#  only as far apart as the greater of rise and run!
	def distance(self, a, b):
		ra = self.row(a)
		ca = self.col(a)

		rb = self.row(b)
		cb = self.col(b)

		if ra >= 0 and ca >= 0 and rb >= 0 and cb >= 0:
			difrow = abs(ra - rb)
			difcol = abs(ca - cb)
			return max(difrow, difcol)
		return 0

	################################################  Notation and display
	def FEN(self, b=None, slashes=False):
		if b == None:
			b = self.board

		if self.whoAmI == 'w':
			staticstring = 'w'
		else:
			staticstring = 'b'

		emptyFound = False
		emptyCtr = 0
		x = 0
		y = 0

		for y in range(0, 8):
			for x in range(0, 8):
				if self.isEmpty(y * 8 + x, b):
					if emptyFound == False:
						emptyFound = True
					emptyCtr += 1
				else:
					if emptyFound == True:
						emptyFound = False
						if emptyCtr > 0:
							staticstring += str(emptyCtr)
							emptyCtr = 0
						staticstring += b[y * 8 + x]
					else:
						staticstring += b[y * 8 + x]
			if emptyFound == True:
				emptyFound = False
				if emptyCtr > 0:
					staticstring += str(emptyCtr)
					emptyCtr = 0
			if y < 7 and slashes:
				staticstring += '/'
		return staticstring

	def readFEN(self, fen):
		f = list(fen)
		self.whoAmI = f[0]
		ctr = 1
		bctr = 0
		while ctr < len(f):
			if f[ctr].isdigit():
				for i in range(0, int(f[ctr])):
					self.board[bctr] = 'e'
					bctr += 1
			elif f[ctr].isalpha():
				self.board[bctr] = f[ctr]
				bctr += 1
			ctr += 1

	def draw(self, b=None):
		if b == None:
			b = self.board
		for ctr in range(56, -1, -8):
			outputstring = ''
			for ctr2 in range(ctr, ctr + 8):
				if self.isEmpty(ctr2, b):
					outputstring += '. '
				else:
					outputstring += b[ctr2] + ' '
			print outputstring

	def algebraic(self, index):
		c = self.col(index)
		r = self.row(index)

		if c == 0:
			alg = 'a'
		elif c == 1:
			alg = 'b'
		elif c == 2:
			alg = 'c'
		elif c == 3:
			alg = 'd'
		elif c == 4:
			alg = 'e'
		elif c == 5:
			alg = 'f'
		elif c == 6:
			alg = 'g'
		else:
			alg = 'h'

		alg += str(r + 1)

		return alg

	def label(self):
		return 'othello'
