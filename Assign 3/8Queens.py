#global variable
size = 8 #8 Queens

class Board:
    
    def __init__(self, config):
        self.config = config
        self.cost = self.obj_func()
    

    def __str__(self):
        string = ""
        for pos in self.config:
            for row in range(1,size+1):
                if (row == pos):
                    string += "Q\t"
                else:
                    string += "x\t"
            string += "\n\n"
        return string


    def obj_func(self):
        violations = 0
        for i in range(size):
            for j in range(i+1,size):
                #same row
                if self.config[i] == self.config[j]: 
                    violations += 1
                #same diagonal
                elif self.config[i]+i == self.config[j]+j:   
                    violations += 1
                #same other diagonal
                elif self.config[i]-i == self.config[j]-j:
                    violations += 1
        return violations



class HillClimbing:

    def find_child(self,board):
        #currState     - Given state with its configuration for which we need to find next best state
        #nextConfig    - Configuration of any possible next state
        #nextState     - Any possible next state with its respective configuration
        #nextBestState - Out of all possible best states what ever has least cost
        #costToBeat    - To fins a next state such that the cost is lesser

        currState = board
        nextBestState = currState
        costToBeat = currState.cost

        for row in range(size):
            for i in range(1, size + 1):
                if i !=currState.config[row]:
                    nextConfig = (currState.config).copy()
                    nextConfig[row] = i
                    nextState = Board(nextConfig)
                    if (nextState.cost < costToBeat):
                        costToBeat = nextState.cost
                        nextBestState = nextState

        return nextBestState

    
    def solver(self,initState):
        currState = initState
        i = 0
        while (True):
            i += 1
            nextState = self.find_child(currState)
            if (nextState.cost == currState.cost):
                break
            else:
                currState = nextState
        print("\nNumber of Iterations:",i)
        return currState

    def print_state(self,board,state=""):
      print(state,"Board Configuration:",board.config)
      print(board)
      print("Cost:",board.cost," violations")
      print("\n")



def main():
    obj = HillClimbing()

    initState = Board([1, 2, 4, 3, 6, 5, 8, 8])
    finalState = obj.solver(initState)
    obj.print_state(initState,"\nInitial")
    obj.print_state(finalState,"Final")

    print("------------------------------------------------------------")
    print("------------------------------------------------------------")

    initState = Board([2, 5, 6, 1, 3, 2, 8, 7])
    finalState = obj.solver(initState)
    obj.print_state(initState,"\nInitial")
    obj.print_state(finalState,"Final")
    

if __name__=="__main__":
    main()




'''
OUTPUT:
C:\Users\Sweth\Desktop\Semester-V\AI Lab\Assign 3>python 8Queens.py

Number of Iterations: 6

Initial Board Configuration: [1, 2, 4, 3, 6, 5, 8, 8]
Q       x       x       x       x       x       x       x       

x       Q       x       x       x       x       x       x       

x       x       x       Q       x       x       x       x       

x       x       Q       x       x       x       x       x       

x       x       x       x       x       Q       x       x

x       x       x       x       Q       x       x       x

x       x       x       x       x       x       x       Q

x       x       x       x       x       x       x       Q


Cost: 10  violations


Final Board Configuration: [6, 2, 7, 1, 3, 5, 8, 4]
x       x       x       x       x       Q       x       x

x       Q       x       x       x       x       x       x

x       x       x       x       x       x       Q       x

Q       x       x       x       x       x       x       x

x       x       Q       x       x       x       x       x

x       x       x       x       Q       x       x       x

x       x       x       x       x       x       x       Q

x       x       x       Q       x       x       x       x


Cost: 0  violations


------------------------------------------------------------
------------------------------------------------------------

Number of Iterations: 3

Initial Board Configuration: [2, 5, 6, 1, 3, 2, 8, 7]
x       Q       x       x       x       x       x       x

x       x       x       x       Q       x       x       x

x       x       x       x       x       Q       x       x

Q       x       x       x       x       x       x       x

x       x       Q       x       x       x       x       x

x       Q       x       x       x       x       x       x

x       x       x       x       x       x       x       Q

x       x       x       x       x       x       Q       x


Cost: 5  violations


Final Board Configuration: [1, 4, 6, 1, 3, 2, 8, 7]
Q       x       x       x       x       x       x       x

x       x       x       Q       x       x       x       x

x       x       x       x       x       Q       x       x

Q       x       x       x       x       x       x       x

x       x       Q       x       x       x       x       x

x       Q       x       x       x       x       x       x

x       x       x       x       x       x       x       Q

x       x       x       x       x       x       Q       x


Cost: 3  violations
'''