import sys
import random
import copy

gameOver = False
turn=1
moves=0
specifiedDepth=0

def setupboard():
	state= []
	state.append(['*','*','*','*','*','*','*',])
	state.append(['*','*','*','*','*','*','*',])
	state.append(['*','*','*','*','*','*','*',])
	state.append(['*','*','*','*','*','*','*',])
	state.append(['*','*','*','*','*','*','*',])
	state.append(['*','*','*','*','*','*','*',])
	state.append(['1','2','3','4','5','6','7',])
	return state

def printboard(state):
	for row in state:
		for entry in row:
			 print(entry),
		print

def humanMove(state):
	global turn
	try:
		col = raw_input("Player " + str(turn) +"'s turn. Player " + str(turn) +" select a column: ")
		if col is 'q':
			print("Thanks for playing!")
			exit()
		col = int(col)
		y = len(state[col-1])-1
		madeMove=False
		while y >= 0:
			if (state[y][col-1]=='*'):
				if turn==1:
					state[y][col-1]='R'
				elif turn==2:
					state[y][col-1]='B'
				madeMove=True
				global gameOver
				gameOver=checkBoard(state)
				break
			else:
				y-=1
		if madeMove:
			turn = switchPlayer(turn)
		else:
			print("Invalid move still"),
			state = humanMove(state)
	except (SyntaxError, NameError, IndexError, ValueError):
		print("Invalid move still"),
		state = humanMove(state)
	return state

def computerMove(state):
	global gameOver
	state = alphabeta(state)
	gameOver = checkBoard(state)
	global turn
	turn = switchPlayer(turn)
	return state

def alphabeta(s):
	global turn
	depth =1
	newdepth = copy.copy(depth)
	alpha, s = abmax(turn, s, -100, 100, newdepth +1)
	return s

def abmax(turn, s, a, b, depth):
	st = []
	if depth==2:
		for row in s:
			st.append(list(row))
	global specifiedDepth
	if checkBoard(s):
		return 10, s
	elif depth > int(specifiedDepth):
		#print "gothere"
		return findPoints(s, turn), s
	else:
		for child in generateChildren(turn, s):
			turn = switchPlayer(turn)
			#global specifiedDepth
			newdepth = copy.copy(depth)+1
			v, state = abmin(turn, child, a, b, newdepth)
			if v > a:
				a = v
				s = state
			if b <= a:
				return a,s
		else:
			return a, s

def abmin(turn, s, a, b, depth):
	global specifiedDepth
	if checkBoard(s):
		return -10, s
	elif depth > int(specifiedDepth):
		#print "got here"
		return findPoints(s, turn), s
	else:
		for child in generateChildren(turn, s):
			turn = switchPlayer(turn)
			newdepth = copy.copy(depth)+1
			v, state = abmax(turn, child, a, b, newdepth)
			if v < b:
				b = v
				s = state
			if b <=a:
				return b,s
		return b, s

def findPoints(state, turn):
	x = 0
	y = 5
	maxR = 0
	maxB = 0
	while y >= 0:
		x = 0
		while x < 7:
			sideCount = 1
			upcount = 1
 			piece = state[y][x]
			# Tests for possible moves up
			if piece != '*':
				if y-3>= 0 and state[y-1][x] == piece:
					upcount+=2
					if state[y-2][x] == piece:
						upcount+=2
					elif state[y-2][x] == '*':
						upcount+=1
				elif y-3 >= 0 and state[y-1][x] == '*':
					upcount+=1
				if piece == 'R':
					maxR = copy.copy(upcount)
				else:
					maxB = copy.copy(upcount)
			#test for across
			if x+3 < 7:
				if piece == '*' and state[y][x+1] != '*':
					piece = state[y][x+1]
				elif piece == '*' and state[y][x+2] != '*':
					piece = state[y][x+2]
				elif piece == '*' and state[y][x+3] != '*':
					piece = state[y][x+3] 
				if (state[y][x+1] == piece or state[y][x+1] == '*') and (state[y][x+2] == piece or state[y][x+2] == '*') and (state[y][x+3] == piece or state[y][x+3] == '*'):
					if state[y][x+1] == piece:
						sideCount+=2
						if state[y][x+2] == piece:
							sideCount+=2
							if state[y][x+3]==piece:
								sideCount+=2
							else:
								sideCount+=1
						else:
							sideCount+=1
					else:
						sideCount+=1
						if state[y][x+2] == piece:
							sideCount+=2
							if state[y][x+3] == piece:
								sideCount+=2
							else:
								sideCount+=1
						else:
							sideCount+=1
				if piece == 'R':
					if sideCount > maxR:
						maxR = copy.copy(sideCount)
				else:
					if sideCount > maxB:
						maxB = copy.copy(sideCount)
			#test for right diagonal
			if x+3 < 7 and y-3>=0 and state[y][x] != '*':
				piece = state[y][x]
				count = 0
				if y+1 < 6 and x-1 > 0 and state[y+1][x-1] == '*':
					count+=1
					if y+2<6 and x-2 >0 and state[y+2][x-2] == '*':
						count+=1
						if y+3<6 and x-3>0 and state[y+3][x-3] == '*':
							count+=1
				if state[y-1][x+1] == piece:
					count+=2
					if state[y-2][x+2] == piece:
						count+=2
					elif state[y-2][x+2] == '*':
						count+=1
				elif state[y-1][x+1] == '*':
					count+=1
				if piece == 'R':
					if count > maxR:
						maxR = copy.copy(count)
				else:
					if count > maxB:
						maxB = copy.copy(count)
			#test for left diagonal
			if x-3 >= 0 and y-3 >= 0 and state[y][x] != '*':
				piece = state[y][x]
				count = 0
				if y+1 < 6 and x+1 < 7 and state[y+1][x+1] == '*':
                                        count+=1
                                        if y+2<6 and x+2 <7 and state[y+2][x+2] == '*':
                                                count+=1
                                                if y+3<6 and x+3<7 and state[y+3][x+3] == '*':
                                                        count+=1
                                if state[y-1][x-1] == piece:
                                        count+=2
                                        if state[y-2][x-2] == piece:
                                                count+=2
                                        elif state[y-2][x-2] == '*':
                                                count+=1
                                elif state[y-1][x-1] == '*':
                                        count+=1
                                if piece == 'R':
                                        if count > maxR:
                                                maxR = copy.copy(count)
                                else:
                                        if count > maxB:
                                                maxB = copy.copy(count)
			x+=1
		y-=1
	if turn == 1:
		return maxR
	else:
		return maxB
 
def generateChildren(turn, state):
	childStates = []
	y = 5
	recMoves = []
	global moves
	if moves == 1:
                if state[5][3] != '*':
			move = 5,4
                        recMoves.append(move)
			move = 5,2
                        recMoves.append(move)
                else:
                        move = 5,3
			recMoves.append(move)
	else:
		while y >= 0:
			x = 6
			while x >= 0:		        	
				if turn == 2 and  state[y][x] == 'B':
					recMoves.extend(checkAround(turn, state, y, x))
				elif turn == 1 and state[y][x] == 'R':
                                	recMoves.extend(checkAround(turn, state, y, x))
				x-=1
			y-=1
	if len(recMoves) == 0:
		for x in range(0, 7):
			for y in range(5, -1, -1):
				if (y== 5 and state[y][x] == '*'):
					move = y,x
					recMoves.append(move)
				elif state[y][x] != '*' and state[y-1][x] == '*':
					move = y-1,x
					recMoves.append(move)
	revMoves = set(recMoves)
	print("Player " + str(turn) + "'s recomended move " + str(recMoves))
	for move in recMoves:
		newstate=[]
		for row in state:
			newstate.append(list(row))
                childStates.append(makeMove(newstate, move, turn))
	return childStates

def checkAround(turn, state, y, x):
	if (turn == 2 and state[y][x] == 'B') or (turn == 1 and state[y][x] == 'R'):
		goodMoves = []
		if not x+1 > 6:
			if not y+2 > 7 and state[y+1][x+1] == '*' and state[y+2][x+1] != '*':
				move = y+1, x+1
				goodMoves.append(move)
			if state[y][x+1] == '*' and state[y+1][x+1] != '*':
				move = y, x+1
                                goodMoves.append(move)
			if not y-1>=0 and state[y-1][x+1] == '*' and state[y][x+1] != '*':
				move = y-1, x+1
                                goodMoves.append(move)
		if not y-1<0 and state[y-1][x] == '*':
				move = y-1, x
                                goodMoves.append(move)
		if not x-1 < 0:
			if not y+2 > 7 and state[y+1][x-1] == '*' and state[y+2][x-1] != '*':
				move = y+1, x-1
                                goodMoves.append(move)
			if state[y][x-1] == '*' and state[y+1][x-1] != '*':
				move = y, x-1
                                goodMoves.append(move)
			if not y-1 < 0 and state[y-1][x-1] == '*' and state[y][x-1] != '*':
				move = y-1, x-1
                                goodMoves.append(move)
		recommendedMoves = set(goodMoves)
	return recommendedMoves

def makeMove(state, child, turn):
	newState = []
	for row in state:
		newState.append(list(row))
	if turn == 2:
		newState[child[0]][child[1]] = 'B'
	else:
		newState[child[0]][child[1]] = 'R'
        return newState

def switchPlayer(turn):
	global moves
	moves+=1
	if (turn == 1 ):
		return 2 
	elif turn == 2:
		return 1

def checkBoard(state):
	for idx, row in enumerate(state):
		for idy, entry in enumerate(row):
			if not state[idx][idy]=='*':
				try:
					color = state[idx][idy]
					if state[idx][idy-1]==color and state[idx][idy-2]==color and state[idx][idy-3]==color:
						return True
					elif state[idx-1][idy-1]==color and state[idx-2][idy-2]==color and state[idx-3][idy-3]==color:
						return True
					elif state[idx-1][idy]==color and state[idx-2][idy]==color and state[idx-3][idy]==color:
                				return True
					elif state[idx-1][idy+1]==color and state[idx-2][idy+2]==color and state[idx-3][idy+3]==color:
                                        	return True
				except IndexError:
					i="oops"	
	return False

def winner(color):
	print(color + " won the game!!!!!!!!!")

def main():
        currentboard = setupboard()
	print("Enter 'q' at any time to quit")
	typeOfGame = raw_input("Enter an 'h' for human players or 'c' to play against a computer: ")
	if typeOfGame == 'h':
		print('You are playing a human game')
        	printboard(currentboard)
		while(not gameOver):
			currentboard = humanMove(currentboard)
			printboard(currentboard)
	elif typeOfGame == 'c':
		print("You are playing against a computer")
		global specifiedDepth
		specifiedDepth = str(sys.argv[1])
		printboard(currentboard)
		global turn
		turn = 1
		while(not gameOver):
			currentboard = humanMove(currentboard)
			printboard(currentboard)
			if not gameOver:
				currentboard = computerMove(currentboard)
				printboard(currentboard)
				if gameOver:
					print("The superior computer got you, better luck next time!")
			else:
				print("You beat the computer!")

if __name__ == "__main__":
	main()
