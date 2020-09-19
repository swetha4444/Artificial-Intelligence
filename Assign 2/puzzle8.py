import heapq

class Node:

	goalState=[0,1,2,3,4,5,6,7,8]
	
	def __init__(self,board=[],parent=None,depth=0):
	
		self.state = board
		self.parent = parent
		self.depth = depth
		self.f_n = self.depth + self.heuristic()
		
		
	def __str__(self):
	
		return  "|"+ str(self.state[0]) +" "+ str(self.state[1]) + " "+ str(self.state[2])+"|" +"\n" \
		"|"+ str(self.state[3]) +" "+ str(self.state[4]) + " "+ str(self.state[5]) +"|" +"\n"  \
		"|"+ str(self.state[6]) +" "+ str(self.state[7]) + " "+ str(self.state[8])+"|" +"\n" 
		
		
	def __lt__(self, another_board):
		
		return self.f_n < another_board.f_n
	
	
	def goal_test(self):
	
		if (self.state == self.goalState):
			return True
		return False
	
	
	def find_blank(self):
		#returns index of blank block
		
		blank =  None
		for i in range(0,9):
			if (self.state[i] == 0):
				blank = i
				break
		return blank
		
	
	def swap(self, s1, s2):
	
		new_state = list(self.state)
		new_state[s1], new_state[s2] = new_state[s2], new_state[s1]
		return new_state
	
	
	def move_up(self):
	
		blank = self.find_blank()
		return Node(self.swap(blank, blank-3), self, self.depth + 1)
		
			
	
	def move_down(self):
	
		blank = self.find_blank()
		return Node(self.swap(blank, blank+3),self, self.depth + 1)
				
		
	
	def move_left(self):
	
		blank = self.find_blank()
		return Node(self.swap(blank, blank-1), self, self.depth + 1)
		
			
	def move_right(self):
	
		blank = self.find_blank() 
		return Node(self.swap(blank, blank+1), self,self.depth + 1)
	
	
	def generate_childNodes(self):
	 	
	 	children = []
	 	blank = self.find_blank()
	 	#print(self)
	 	#print("blank= ",blank)

		# move left
		if (blank % 3 != 0):
			new_board=self.move_left()
			children.append(new_board)
			#print("Left")
			#print(new_board)
			

        # move right
		if (blank % 3 != 2):
			new_board=self.move_right()
			children.append(new_board)
			#print("Right")
			#print(new_board)
			
        # move up
		if (blank > 2):
			new_board=self.move_up()
			children.append(new_board)
			#print("Up")
			#print(new_board)

        # move down
		if (blank < 6):
			new_board=self.move_down()
			children.append(new_board)
			#print("Down")
			#print(new_board)
			
		return children
		
		
	def heuristic(self):
        #Calculate h(n) based on the Manhattan Distance |x1-x2|+|y1-y2|
        
		h_n = 0
        
		for i in range(len(self.state)):
			# Horizontal dist 							  Vertical dist
			h_n += abs(self.state[i] // 3 - i // 3) + abs(self.state[i] % 3 - i % 3)

		return h_n




class Searching:

	final_state = None
	current_depth = 0
	nodes = 0
	path = []

	def BFS(self,start):
	
		frontier = [] #Queue
		visited =set() #visited nodes
		explored = set() #Set
		current_depth = 0
		total_moves = 0
    	
		frontier.append(start)
		visited.add(tuple(start.state))
		explored.add(tuple(start.state))
    
		while (len(frontier)!=0):
		
			currState = frontier.pop(0) #dequeue
			explored.add(currState)
			#print("pop")
			
			if (currState.goal_test()): #if its a final state
				visited.add(tuple(currState.state))
				explored.add(tuple(currState.state))
				nodes_found = len(visited)
				self.final_state = currState
				#print("Goal")
				self.nodes = len(visited)
				return len(visited)
		
				
			for child in currState.generate_childNodes():
				if (tuple(child.state) not in visited):
						
					frontier.append(child)
					visited.add(tuple(child.state))
					#print("append")
					self.current_depth = max(self.current_depth, child.depth)
		
		return None
		
		
	def a_star(self,start):
		
		frontier = []
		visited = set()
		explored = set()

		heapq.heappush(frontier,start)
		visited.add(tuple(start.state))

		while (len(frontier) != 0):
			
			currState = heapq.heappop(frontier)
			visited.add(tuple(currState.state))

			if (currState.goal_test()):
				visited.add(tuple(currState.state))
				explored.add(tuple(currState.state))
				self.final_state = currState
				self.nodes = len(visited)
				#print("Goal")
				return len(visited)
            
			for child in currState.generate_childNodes():
				if (tuple(child.state) not in visited) :
					heapq.heappush(frontier, child)
					self.current_depth = max(self.current_depth, child.depth)
                              
		return None
        


	def path_trace(self):
		
		currState = self.final_state
		self.path = [currState]

		while (currState.parent != None):
			(self.path).append(currState.parent)
			currState = currState.parent

		self.path = self.path[::-1]
		
		
	def print_solution(self):
		
		print "No. of nodes visited: ",self.nodes
		print "No. of moves: ",(len(self.path)-1)
		print "Depth of BFS tree: ",self.current_depth
		print"Path:"
		for node in self.path:
			print(node)
			print "   |   "
			print "   V   "
		print "Goal Reached"
		
	
	

# __main function__
puzzle=Searching()
start = Node(board=[7,2,4,5,0,6,8,3,1])

#BFS
print " "
print "                                   BFS Search                                     "
print "--------------------------------------------------------------------------------------"
nodes = puzzle.BFS(start)
path = puzzle.path_trace()
puzzle.print_solution()


#A* Search
print " "
print "                                   A* Search                                     "
print "--------------------------------------------------------------------------------------"
nodes = puzzle.a_star(start)
path = puzzle.path_trace()
puzzle.print_solution()



'''
MacBook-Pro Desktop % python puzzle8.py
 
                                   BFS Search                                     
--------------------------------------------------------------------------------------
No. of nodes visited:  175326
No. of moves:  26
Depth of BFS tree:  27
Path:
|7 2 4|
|5 0 6|
|8 3 1|

   |   
   V   
|7 2 4|
|0 5 6|
|8 3 1|

   |   
   V   
|0 2 4|
|7 5 6|
|8 3 1|

   |   
   V   
|2 0 4|
|7 5 6|
|8 3 1|

   |   
   V   
|2 5 4|
|7 0 6|
|8 3 1|

   |   
   V   
|2 5 4|
|7 6 0|
|8 3 1|

   |   
   V   
|2 5 4|
|7 6 1|
|8 3 0|

   |   
   V   
|2 5 4|
|7 6 1|
|8 0 3|

   |   
   V   
|2 5 4|
|7 6 1|
|0 8 3|

   |   
   V   
|2 5 4|
|0 6 1|
|7 8 3|

   |   
   V   
|2 5 4|
|6 0 1|
|7 8 3|

   |   
   V   
|2 5 4|
|6 1 0|
|7 8 3|

   |   
   V   
|2 5 4|
|6 1 3|
|7 8 0|

   |   
   V   
|2 5 4|
|6 1 3|
|7 0 8|

   |   
   V   
|2 5 4|
|6 1 3|
|0 7 8|

   |   
   V   
|2 5 4|
|0 1 3|
|6 7 8|

   |   
   V   
|2 5 4|
|1 0 3|
|6 7 8|

   |   
   V   
|2 5 4|
|1 3 0|
|6 7 8|

   |   
   V   
|2 5 0|
|1 3 4|
|6 7 8|

   |   
   V   
|2 0 5|
|1 3 4|
|6 7 8|

   |   
   V   
|0 2 5|
|1 3 4|
|6 7 8|

   |   
   V   
|1 2 5|
|0 3 4|
|6 7 8|

   |   
   V   
|1 2 5|
|3 0 4|
|6 7 8|

   |   
   V   
|1 2 5|
|3 4 0|
|6 7 8|

   |   
   V   
|1 2 0|
|3 4 5|
|6 7 8|

   |   
   V   
|1 0 2|
|3 4 5|
|6 7 8|

   |   
   V   
|0 1 2|
|3 4 5|
|6 7 8|

   |   
   V   
Goal Reached
 
                                   A* Search                                     
--------------------------------------------------------------------------------------
No. of nodes visited:  3323
No. of moves:  26
Depth of BFS tree:  27
Path:
|7 2 4|
|5 0 6|
|8 3 1|

   |   
   V   
|7 2 4|
|0 5 6|
|8 3 1|

   |   
   V   
|0 2 4|
|7 5 6|
|8 3 1|

   |   
   V   
|2 0 4|
|7 5 6|
|8 3 1|

   |   
   V   
|2 5 4|
|7 0 6|
|8 3 1|

   |   
   V   
|2 5 4|
|7 3 6|
|8 0 1|

   |   
   V   
|2 5 4|
|7 3 6|
|0 8 1|

   |   
   V   
|2 5 4|
|0 3 6|
|7 8 1|

   |   
   V   
|2 5 4|
|3 0 6|
|7 8 1|

   |   
   V   
|2 5 4|
|3 6 0|
|7 8 1|

   |   
   V   
|2 5 0|
|3 6 4|
|7 8 1|

   |   
   V   
|2 0 5|
|3 6 4|
|7 8 1|

   |   
   V   
|0 2 5|
|3 6 4|
|7 8 1|

   |   
   V   
|3 2 5|
|0 6 4|
|7 8 1|

   |   
   V   
|3 2 5|
|6 0 4|
|7 8 1|

   |   
   V   
|3 2 5|
|6 4 0|
|7 8 1|

   |   
   V   
|3 2 5|
|6 4 1|
|7 8 0|

   |   
   V   
|3 2 5|
|6 4 1|
|7 0 8|

   |   
   V   
|3 2 5|
|6 4 1|
|0 7 8|

   |   
   V   
|3 2 5|
|0 4 1|
|6 7 8|

   |   
   V   
|3 2 5|
|4 0 1|
|6 7 8|

   |   
   V   
|3 2 5|
|4 1 0|
|6 7 8|

   |   
   V   
|3 2 0|
|4 1 5|
|6 7 8|

   |   
   V   
|3 0 2|
|4 1 5|
|6 7 8|

   |   
   V   
|3 1 2|
|4 0 5|
|6 7 8|

   |   
   V   
|3 1 2|
|0 4 5|
|6 7 8|

   |   
   V   
|0 1 2|
|3 4 5|
|6 7 8|

   |   
   V   
Goal Reached
'''




