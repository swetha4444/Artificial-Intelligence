#global variavble
points = [] #set of all given points

class point:

    def __init__(self,x,y):
        self.x = x
        self.y = y


    def __str__(self): #(0,0)
        return "("+str(self.x)+","+str(self.y)+")"



class centre:

    def __init__(self,point = point(0,0),man_dist = 0):
        self.point = point
        self.man_dist = self.obj_func()


    def obj_func(self):
        sum = 0
        for i in range(len(points)):
            sum += abs((self.point).x - points[i].x) + abs((self.point).y - points[i].y)
        return sum

    
    def move_up(self):
        pt = point((self.point).x,(self.point).y+1)
        return centre(pt)

    
    def move_down(self):
        pt = point((self.point).x,(self.point).y-1)
        return centre(pt)


    def move_left(self):
        pt = point((self.point).x-1,(self.point).y)
        return centre(pt)

    
    def move_right(self):
        pt = point((self.point).x+1,(self.point).y)
        return centre(pt)


    def generate_centre(self,init):
        currState = init
        prevValue = 100
        currValue = currState.man_dist
        i=0
        while(prevValue > currValue):
            i += 1
            prevvalue = currValue
            manVal = [(currState.move_up()).man_dist,(currState.move_down()).man_dist,(currState.move_left()).man_dist,(currState.move_right()).man_dist]
            minpos = manVal.index(min(manVal))

            if (manVal.count(min(manVal)) == len(manVal)):
              break

            if (minpos == 0):
                currState = currState.move_up()
                currvalue = currState.man_dist
                currState.print_centre("Moved Up:\n")
                

            elif (minpos == 1):
                currState = currState.move_down()
                currvalue = currState.man_dist
                currState.print_centre("Moved Down:\n")

            elif (minpos == 2):
                currState = currState.move_left()
                currvalue = currState.man_dist
                currState.print_centre("Moved Left:\n")

            elif (minpos == 3):
                currState = currState.move_right()
                currvalue = currState.man_dist
                currState.print_centre("Moved Right:\n")
        
        print("\nNo. of iterations:",i)
        print("")
        return currState

    def print_centre(self,direction = ""):
        print(direction,"Point:",self.point,"\tManhattan Distance:",self.man_dist)
        print("")


def main():
    points.append(point(0, 6))
    points.append(point(1, 2))
    points.append(point(3, 1))
    points.append(point(7, 0))
    points.append(point(9, 3))

    print("\nGiven Points:")
    for pt in points:
        print(pt)

    initState = centre()
    print("\n-------------------------------------------------")
    print("\nAssumed Initial Centre:")
    initState.print_centre()
    print("-------------------------------------------------\n")
    print("\n-------------")
    print("Trace:")
    print("-------------\n")
    finalState = initState.generate_centre(initState)
    print("\n-------------------------------------------------")
    print("\nFinal Centre Found:")
    finalState.print_centre()
    print("-------------------------------------------------\n")


if __name__=="__main__":
    main()




'''
OUTPUT:
C:\Users\Sweth\Desktop\Semester-V\AI Lab\Assign 3>python centre.py

Given Points:
(0,6)
(1,2)
(3,1)
(7,0)
(9,3)

-------------------------------------------------

Assumed Initial Centre:
 Point: (0,0)   Manhattan Distance: 32

-------------------------------------------------


-------------
Trace:
-------------

Moved Up:
 Point: (0,1)   Manhattan Distance: 29

Moved Right:
 Point: (1,1)   Manhattan Distance: 26

Moved Up:
 Point: (1,2)   Manhattan Distance: 25

Moved Right:
 Point: (2,2)   Manhattan Distance: 24

Moved Right:
 Point: (3,2)   Manhattan Distance: 23


No. of iterations: 6


-------------------------------------------------

Final Centre Found:
 Point: (3,2)   Manhattan Distance: 23

-------------------------------------------------
'''