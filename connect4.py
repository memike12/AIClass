import sys


gameOver = False
turn='R'

def setupboard():
	state= []
	#state.append(['*','*','*','*','*','*','*',])
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

def makeMove(state):
	try:
		col = raw_input(turn +"'s turn. " + turn +" select a column: ")
		if col is 'q':
			print("Thanks for playing!")
			exit()
		col = int(col)
		y = len(state[col-1])-1
		madeMove=False
		while y >= 0:
			if (state[y][col-1]=='*'):
				state[y][col-1]=turn
				madeMove=True
				global gameOver
				gameOver =checkBoard(state)
				break
			else:
				y-=1
		if madeMove: 
			switchPlayer()
		else:
			print("Invalid move still"),
			state = makeMove(state)
	except (SyntaxError, NameError, IndexError):
		print("Invalid move still"),
		state = makeMove(state)
	return state

def switchPlayer():
	global turn
	if (turn=='R'):
		turn='B'
	else:
		turn='R'

def checkBoard(state):
	for idx, row in enumerate(state):
		for idy, entry in enumerate(row):
			if not state[idx][idy]=='*':
				try:
					color = state[idx][idy]
					if state[idx][idy-1]==color and state[idx][idy-2]==color and state[idx][idy-3]==color:
						winner(color)
						return True
					elif state[idx-1][idy-1]==color and state[idx-2][idy-2]==color and state[idx-3][idy-3]==color:
						winner(color)
						return True
					elif state[idx-1][idy]==color and state[idx-2][idy]==color and state[idx-3][idy]==color:
                                        	winner(color)
						return True
					elif state[idx-1][idy+1]==color and state[idx-2][idy+2]==color and state[idx-3][idy+3]==color:
                                        	winner(color)
                                        	return True
				except IndexError:
					i="oops"	
	return False

def winner(color):
	print(color + " won the game!!!!!!!!!")

def main():
        currentboard = setupboard()
	print("Enter 'q' at any time to quit")
        printboard(currentboard)
	while(not gameOver):
		currentboard = makeMove(currentboard)
		printboard(currentboard)	


if __name__ == "__main__":
	main()
