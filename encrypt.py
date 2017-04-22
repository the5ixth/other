from life import Board
import binascii
import sys
import os


def keygen(board, turns):
	count = 0
	while count != turns:
		board.live()
		board.change_board()
		count += 1
	lst = [ board.board[j][i] for j in range(board.height) for i in range(board.width) ]
	key_list = [ 1 if char == 'X' else 0 for char in lst ]
	key = ''
	for i in key_list:
		key += str(i)
	return key

def encrypt(fle, board, key):
	fle_obj = open(fle, 'r')
	txt = fle_obj.read()

	b = ''
	for line in txt:
		for char in line:
			b += bin(ord(char))
	#print( b )
	enc_stream = b & key
	os.system('touch file2')
	file2 = open('file2' , 'w')
	file2.write(enc_strem)
	fle_obj.close()
	file2.close()
	
	
	
#def decrypt(fle):


if __name__ == "__main__":
	file1 = sys.argv[1]
	b = Board()
	turns = 5
	key = keygen(b, turns)
	print( key )
	encrypt( file1, b, key )
	
