#global variables
start=(8,0,0) 
goal=4
jugCap = [8,5,3]
finalStates = []
parent = dict()

def fillOut(i,j,currState):

    currState = list(currState)

    if (currState[i] + currState[j] >= jugCap[j]): 
        
        total = currState[i] + currState[j]

        currState[j] = jugCap[j]
        
        currState[i] = total - currState[j]
    
    else:                                                    
       
        currState[j] += currState[i]
       
        currState[i] = 0

    return tuple(currState)


def nextState(currState):
    
    nextStates = []
    
    visited=list()

    for i in range(len(jugCap)):

        for j in range(len(jugCap)):
        
            if (currState[i] != 0 and currState[j] != jugCap[j] and (i-j != 0)):
        
                next = fillOut(i,j,currState)

                if (next not in visited):

                    parent[next] = currState

                    nextStates.append(next)

                    visited.append(next)

    return nextStates


def BFS():

    front = [] #Queue

    visited = []

    path = []

    parent[start] = start

    front.append(start)

    visited.append(start)

    currState = start
    print(currState)

    while (len(front)!=0):

        currState = front[0] #dequeue

        path.append(currState)

        if (goal in currState): #if its a final state
            
            finalStates.append()

        nextStates = nextState(currState)

        front = front + nextStates

        front.pop(0)

        return path


def trace(finalState):
    print("Hi")

    path = [finalState]
    print("Hi")

    currState = finalState
    print("Hi")

    while (currState != start):
        print("Hi")

        path.append(parent[currState])
        
        currState = parent[currState]

        reverse(path)

        return path


#main 

path=BFS()

print("TOTAL STATES EXPLORED: ",len(path))

print("NUMBER OF SOLUTIONS FOUND: ",len(finalStates))

print("TRACE OF EACH SOLUTION")


for final in finalStates:

    pathTrace = trace(final)

    #print trace
    for state in pathTrace:

        print("(",state[0]," ",state[1]," ",state[2],")","--->")
