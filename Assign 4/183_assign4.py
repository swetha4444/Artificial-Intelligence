import sys
import copy
import math
import random

#global variables
board_size = 8
#The ideal case can yield upton 28 arrangements of non attacking pairs.
#Therefore max fitness (goal) = 28
goal = 28

class Board:

    def __init__(self,queens=[]):
        self.goal = goal
        self.fitness = 0
        # put first items in baord
        if (len(queens) == 0):
          self.queens=list(range(board_size))
          # switch half of them randomly
          self.switch(board_size/2)
        else:
          self.queens = queens


    def __str__(self):
        string = ""
        for pos in self.queens:
            for row in range(0,board_size):
                if (row == pos):
                    string += "Q\t"
                else:
                    string += "x\t"
            string += "\n\n"
        return string


    def switch(self, count):
        count=int(count)
        for i in range(count):
            j = random.randint(0,board_size-1)
            k = random.randint(0,board_size-1)
            self.queens[j], self.queens[k] = self.queens[k], self.queens[j]
        self.compute_fitness()


    def compute_fitness(self):
        #Fitness val returned will be goal−<number of clashes>
        self.fitness = goal
        for i in range(board_size):
            for j in range(i+1,board_size):
                if math.fabs(self.queens[i] - self.queens[j]) == j - i :
                    # for each queen guarding another one reduce fitness by 1
                    self.fitness-=1


    def crossover(self,parent1,parent2):
        child = [-1]*(board_size)
        # p,q index limiters
        p, q = random.randint(0,board_size //3 - 1), random.randint(board_size //2 + 1, board_size  - 2)
        #substituting from parent 1
        child[p:q+1] = parent1[p:q+1]
        for i in range(p, q+1):
            if parent2[i] not in child:
                t = i
                while p <= t <= q:
                    t = parent2.index(parent1[t])
                child[t] = parent2[i]
        for j in range(board_size):
            if child[j] == -1:
                child[j] = parent2[j]
        #print(child)
        cell = Board(child)

        if (random.uniform(0,1) < 0.25): #Mutate
          cell.switch(len(cell.queens)/2)
        cell.compute_fitness()
        return cell


class GeneticProgram:

    def __init__(self,population_size, generation_size):
        # current population
        self.population = []
        self.population_size = population_size
        self.generation_size = generation_size
        # counts how many generations checked
        self.generation_count = 0
        self.solver()
        self.printSolution()


    def solver(self):
        # creates the first population
        self.first_generation()
        i=0
        while (True):
            # if current population reached goal stop checking
            if (self.is_goal_reached()):
                break
            # don't create more generations if program reached generation_size
            if (-1 < self.generation_size <= self.generation_count):
                break
            # create another generation from last generation
            self.next_generation()
            #self.generation_size +=1
            i+=1



    def first_generation(self):
        for i in range(self.population_size):
            self.population.append(Board())
        self.print_population()

    
    def next_generation(self):
        self.generation_count+=1
        cell = Board()
        # get a list of selections to create next generation
        selections = self.random_selection()
        # creates a new population using given selection
        new_population = []
        while (len(new_population) < self.population_size):
            sel = random.choice(selections)[0]
            new_population.append(copy.deepcopy(self.population[sel])) # copy board
        self.population = []
        # crossover current population
        while (len(self.population) < self.population_size):
            x = random.choice(range(len(selections)))
            if (x < len(selections) -1):
              self.population.append(cell.crossover(new_population[x].queens,new_population[x+1].queens))
        self.print_population(selections)


    def is_goal_reached(self):
        for cell in self.population:
            if (cell.fitness == goal):
                return True
        return False


    def random_selection(self):
        population_list = []
        for  i in range(len(self.population)):
            population_list.append((i, self.population[i].fitness))
        population_list.sort(key=lambda pop_item: pop_item[1], reverse=True) #Select by maximum fitness
        limit = round((len(population_list)/2))
        return population_list[:limit]


    def print_population(self, selections=None):
        print ("Generation #%d" % self.generation_count)
        if (selections == None):
            selections = []
        if(self.generation_count > 0):
          print ("\tCrossover using %s" % str([sel[0] for sel in selections])," from previous generation." )
        count = 1
        for population in self.population:
            print ("%8d : (Fitness: %d) %s" % (count, population.fitness, str(population.queens)))
            count+=1

    
    def printSolution(self):
        # prints program result and exits
        print ("\n\n==================================================================")
        # if couldn't find answer
        if (-1 < self.generation_size <= self.generation_count):
            print ("Couldn't find result in %d generations" % self.generation_count)
        # if there was a result, print it
        elif (self.is_goal_reached()):
            print ("Goal Reached")
            print ("Correct Answer found in Generation %s" % self.generation_count)
            for cell in self.population:
                if (cell.fitness == goal):
                    print ("Configuration: ",cell.queens)
                    print ("Fitness: ",cell.fitness)
                    print("\n")
                    print (cell)
        print ("==================================================================")



def main():
    # size of each generation
    population_size = 10
    # -1 for no generation limit. (search to find a result)
    generation_size = -1

    print ("Given:")
    print ("    Board Size      : ", board_size)
    print ("    Population Size : ", population_size)
    print ("==================================================================")

    GeneticProgram(population_size, generation_size)


if __name__ == '__main__':
    main()

'''
OUTPUT:

C:\Users\Sweth\Desktop>python 183_assign4.py
Given:
    Board Size      :  8
    Population Size :  10
==================================================================
Generation #0
       1 : (Fitness: 24) [0, 4, 1, 6, 2, 7, 3, 5]
       2 : (Fitness: 24) [5, 1, 3, 7, 2, 0, 6, 4]
       3 : (Fitness: 18) [4, 1, 2, 3, 0, 6, 5, 7]
       4 : (Fitness: 24) [7, 5, 2, 6, 3, 1, 4, 0]
       5 : (Fitness: 18) [0, 1, 2, 3, 5, 6, 7, 4]
       6 : (Fitness: 17) [0, 7, 2, 3, 1, 5, 6, 4]
       7 : (Fitness: 18) [0, 2, 1, 4, 3, 5, 6, 7]
       8 : (Fitness: 17) [0, 7, 2, 3, 4, 5, 1, 6]
       9 : (Fitness: 24) [3, 1, 7, 0, 4, 6, 5, 2]
      10 : (Fitness: 21) [0, 6, 2, 3, 7, 1, 5, 4]
Generation #1
        Crossover using [0, 1, 3, 8, 9]  from previous generation.
       1 : (Fitness: 25) [5, 4, 1, 6, 2, 7, 3, 0]
       2 : (Fitness: 24) [5, 1, 3, 7, 2, 0, 6, 4]
       3 : (Fitness: 23) [4, 1, 3, 7, 2, 0, 6, 5]
       4 : (Fitness: 24) [7, 5, 2, 6, 3, 1, 4, 0]
       5 : (Fitness: 25) [5, 4, 1, 6, 2, 7, 0, 3]
       6 : (Fitness: 23) [5, 1, 3, 7, 2, 0, 4, 6]
       7 : (Fitness: 23) [5, 1, 3, 7, 2, 0, 4, 6]
       8 : (Fitness: 25) [5, 4, 1, 6, 2, 7, 3, 0]
       9 : (Fitness: 23) [7, 5, 2, 4, 1, 6, 3, 0]
      10 : (Fitness: 25) [7, 4, 1, 0, 5, 2, 6, 3]
Generation #2
        Crossover using [0, 4, 7, 9, 1]  from previous generation.
       1 : (Fitness: 22) [5, 7, 3, 1, 6, 0, 4, 2]
       2 : (Fitness: 21) [7, 4, 1, 0, 5, 2, 3, 6]
       3 : (Fitness: 24) [5, 1, 3, 7, 2, 0, 6, 4]
       4 : (Fitness: 21) [7, 4, 1, 0, 5, 2, 3, 6]
       5 : (Fitness: 24) [5, 1, 3, 7, 2, 0, 6, 4]
       6 : (Fitness: 25) [7, 4, 1, 0, 5, 2, 6, 3]
       7 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       8 : (Fitness: 24) [5, 1, 3, 7, 2, 0, 6, 4]
       9 : (Fitness: 25) [7, 4, 1, 0, 5, 2, 6, 3]
      10 : (Fitness: 25) [7, 4, 1, 0, 5, 2, 6, 3]
Generation #3
        Crossover using [6, 5, 8, 9, 2]  from previous generation.
       1 : (Fitness: 25) [7, 4, 1, 0, 5, 2, 6, 3]
       2 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       3 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       4 : (Fitness: 25) [7, 4, 1, 0, 5, 2, 6, 3]
       5 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       6 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       7 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       8 : (Fitness: 25) [7, 4, 1, 0, 5, 2, 6, 3]
       9 : (Fitness: 25) [7, 4, 1, 0, 5, 2, 6, 3]
      10 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
Generation #4
        Crossover using [1, 2, 4, 5, 6]  from previous generation.
       1 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       2 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       3 : (Fitness: 22) [3, 4, 7, 5, 1, 0, 6, 2]
       4 : (Fitness: 24) [2, 4, 7, 1, 6, 5, 0, 3]
       5 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       6 : (Fitness: 25) [3, 4, 7, 5, 0, 1, 6, 2]
       7 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       8 : (Fitness: 23) [1, 4, 6, 0, 2, 3, 7, 5]
       9 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
      10 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
Generation #5
        Crossover using [0, 1, 4, 6, 8]  from previous generation.
       1 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       2 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       3 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       4 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       5 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       6 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       7 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       8 : (Fitness: 18) [0, 5, 2, 7, 4, 3, 6, 1]
       9 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
      10 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
Generation #6
        Crossover using [0, 1, 2, 3, 4]  from previous generation.
       1 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       2 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       3 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       4 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       5 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       6 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       7 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       8 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       9 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
      10 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
Generation #7
        Crossover using [0, 1, 2, 3, 4]  from previous generation.
       1 : (Fitness: 26) [2, 6, 7, 0, 4, 1, 5, 3]
       2 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       3 : (Fitness: 26) [6, 4, 0, 3, 5, 7, 2, 1]
       4 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       5 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       6 : (Fitness: 23) [2, 0, 7, 3, 4, 1, 6, 5]
       7 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       8 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       9 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
      10 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
Generation #8
        Crossover using [0, 1, 2, 3, 4]  from previous generation.
       1 : (Fitness: 26) [6, 4, 0, 3, 5, 7, 2, 1]
       2 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       3 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       4 : (Fitness: 25) [4, 0, 6, 1, 5, 2, 7, 3]
       5 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       6 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       7 : (Fitness: 26) [6, 4, 0, 3, 5, 7, 2, 1]
       8 : (Fitness: 26) [6, 4, 0, 3, 5, 7, 2, 1]
       9 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
      10 : (Fitness: 26) [6, 4, 0, 3, 5, 7, 2, 1]
Generation #9
        Crossover using [0, 1, 2, 4, 5]  from previous generation.
       1 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       2 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       3 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       4 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       5 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       6 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       7 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       8 : (Fitness: 26) [2, 4, 7, 0, 5, 1, 6, 3]
       9 : (Fitness: 25) [0, 5, 7, 4, 2, 6, 1, 3]
      10 : (Fitness: 28) [2, 4, 6, 0, 3, 1, 7, 5]


==================================================================
Goal Reached
Correct Answer found in Generation 9
Configuration:  [2, 4, 6, 0, 3, 1, 7, 5]
Fitness:  28


x       x       Q       x       x       x       x       x

x       x       x       x       Q       x       x       x

x       x       x       x       x       x       Q       x

Q       x       x       x       x       x       x       x

x       x       x       Q       x       x       x       x

x       Q       x       x       x       x       x       x

x       x       x       x       x       x       x       Q

x       x       x       x       x       Q       x       x


==================================================================
'''