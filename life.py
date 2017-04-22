import random
import time
import sys

class Board():
	def __init__(self, height=10, width=10, represh=.5, board=None, fle=None):
		self.height = height
		self.width = width
		if board:
			self.board = board
		elif fle:
			self.board = self.gen_board(fle)
		else:
			self.board = [[ random.choice(['-', '-', 'X']) for i in range(self.width)] for x in range(self.height) ]
		self.rephresh_rate = represh
		

	def display_board(self):
		print( '\033[2J')
		print( '\033[44m' + '  ' * self.width + '\033[0m' )
		if self.width % 2 == 0:
			print( '\033[44m' + ' ' * int(self.width  - 10) + "\033[30;44mConway's Game of Life" + '\033[44m' + ' ' *int(self.width  - 11) + '\033[0m')
		else:
			print( '\033[44m' + ' ' * int(self.width  - 10) + "\033[30;44mConway's Game of Life" + '\033[44m' + ' ' *int(self.width  - 11) + '\033[0m')
		print( '\033[44m' + '  ' * self.width + '\033[0m')
		for i in self.board:
			for t in i:
				if t == 'X':
					print( '\033[31;41m' + t  , flush=True, end=' ')
				else:
					print( '\033[37;47m' + t, flush=True, end=' ')
			print('\033[0;0m')
		return None

	def live(self):
		self.dead = []
		self.alive = []
		for i in range(self.width):
			for j in range(self.height):
				current = self.board[j][i]
				nb = []				
				for n in range(-1, 2):
					for m in range(-1, 2):
						c = j + n
						d = i + m
						if c >= self.height:
							c = 0
						if d >= self.width:
							d = 0
						try:
							nb.append(self.board[c][d])
						except IndexError:
							pass
				if current == 'X':
					if nb.count('X') < 3 or nb.count('X') > 4:
						self.dead.append((j,i))
					elif nb.count('X') == 3 or nb.count('X') == 4:
						self.alive.append((j, i))
				elif current == '-' and nb.count('X') == 3:
					self.alive.append((j,i))
		return None
				
				
	def change_board(self):
		for j, i in self.dead:
			self.board[j][i] = '-'
		for j, i in self.alive:
			self.board[j][i] = 'X'
		return None

	def gen_board(self, fle):
		fle_obj = open(fle, 'r')
		board = [ [ l.upper() for l in line if l != '\n'] for line in fle_obj ]
		self.height = len(board)
		self.width = len(board[0])
		return board
		
	def run(self):
		while True:
			try:
				self.live()
				time.sleep(self.rephresh_rate)
				self.change_board()
				self.display_board()
			except KeyboardInterrupt:
				exit(1)
		

if __name__ == '__main__':
	#if sys.argv[1] and sys.argv[2]:
	#	height = int(sys.argv[1])
	#	width = int(sys.argv[2])
	#	b = Board(height, width)

	try:
		b = Board(fle=sys.argv[1])

	except:
		b = Board(50, 50)

	b.run()
