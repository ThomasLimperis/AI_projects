from __future__ import print_function
from heapq import * #Hint: Use heappop and heappush

ACTIONS = [(0,1),(1,0),(0,-1),(-1,0)]

class AI:
    def __init__(self, grid, type):
        self.grid = grid
        self.set_type(type)
        self.set_search()

    def set_type(self, type):
        self.final_cost = 0
        self.type = type

    def set_search(self):
        self.final_cost = 0
        self.grid.reset()
        self.finished = False
        self.failed = False
        self.previous = {}

        # Initialization of algorithms goes here
        if self.type == "dfs":
            self.frontier = [self.grid.start]
            self.explored = []
        elif self.type == "bfs":
            self.frontier = [self.grid.start]
            self.explored = []
        elif self.type == "ucs":
            self.h = abs(self.grid.start[0]-self.grid.goal[0]) + abs(self.grid.start[1]-self.grid.goal[1])
            self.frontier = []
            heapify(self.frontier)
            heappush(self.frontier,(0,self.grid.start))
            self.explored = []
        elif self.type == "astar":
            self.h = abs(self.grid.start[0]-self.grid.goal[0]) + abs(self.grid.start[1]-self.grid.goal[1])
            self.frontier = [(self.h,self.grid.start)]
            self.explored = []
            heapify(self.frontier)



    def get_result(self):
        total_cost = 0
        current = self.grid.goal
        while not current == self.grid.start:
            total_cost += self.grid.nodes[current].cost()
            current = self.previous[current]
            self.grid.nodes[current].color_in_path = True #This turns the color of the node to red
        total_cost += self.grid.nodes[current].cost()
        self.final_cost = total_cost

    def make_step(self):
        if self.type == "dfs":
            self.dfs_step()
        elif self.type == "bfs":
            self.bfs_step()
        elif self.type == "ucs":
            self.ucs_step()
        elif self.type == "astar":
            self.astar_step()

    #DFS: BUGGY, fix it first
    def dfs_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        current = self.frontier.pop()

        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        if current == self.grid.goal:
            self.finished = True
            return

        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if not self.grid.nodes[n].puddle and n not in self.explored:
                        self.previous[n] = current
                        self.frontier.append(n)
                        self.grid.nodes[n].color_frontier = True
                        self.explored.append(n)
            if n == self.grid.goal:
                    self.finished = True
                    return
        self.grid.nodes[current].color_frontier= False
        self.grid.nodes[current].color_checked= True
        if n == self.grid.goal:
            self.finished = True
            return


    #Implement BFS here (Don't forget to implement initialization at line 23)
    def bfs_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        current = self.frontier.pop(0)
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        if current == self.grid.goal:
            self.finished = True
            return

        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if not self.grid.nodes[n].puddle and n not in self.explored:
                        self.previous[n] = current
                        self.frontier.append(n)
                        self.grid.nodes[n].color_frontier = True
                        self.explored.append(n)
            if n == self.grid.goal:
                self.finished = True
                return
        self.grid.nodes[current].color_frontier= False
        self.grid.nodes[current].color_checked= True
        if n == self.grid.goal:
            self.finished = True
            return

    #Implement UCS here (Don't forget to implement initialization at line 23)
    def ucs_step(self): #perfectly complete
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        gn, current = heappop(self.frontier) #cost is G(n')
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        if current == self.grid.goal:
            self.finished = True
            return
        self.explored.append(current)
        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if not self.grid.nodes[n].puddle:
                    nnp = self.grid.nodes[n].cost()  #n, n_p
                    if not any(n == x[1] for x in self.frontier ) and n  not in self.explored:
                        self.previous[n] = current
                        self.grid.nodes[n].color_frontier = True
                        heappush(self.frontier,(nnp +gn,n)) #G(n') = G(n) + (n,n')
                    elif any(x[1] == n for x in self.frontier):
                        for x in self.frontier:
                            if x[1] == n and(x[0] >  nnp +gn ): #G(n') = G(n) + (n,n')
                                self.previous[n] = current
                                self.frontier.remove(x)
                                self.grid.nodes[n].frontier = True
                                heappush(self.frontier,(nnp + gn,n)) #G(n') = G(n) + (n,n')
            if n == self.grid.goal:
                self.finished = True
                return
        self.grid.nodes[current].color_frontier= False
        self.grid.nodes[current].color_checked= True


    #Implement Astar here (Don't forget to implement initialization at line 23)
    def astar_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return

        gn, current = heappop(self.frontier) #cost is G(n')
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        if current == self.grid.goal:
            self.finished = True
            return
        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if not self.grid.nodes[n].puddle:
                    nnp = self.grid.nodes[n].cost() #n, n_p
                    h = abs(self.grid.nodes[n].pos[0] - self.grid.goal[0]) + abs(self.grid.nodes[n].pos[1] - self.grid.goal[1])
                    if not any(n == x[1] for x in self.explored) and not any(n == x[1] for x in self.frontier):
                        self.previous[n] = current
                        self.grid.nodes[n].color_frontier = True
                        heappush(self.frontier,(gn + nnp +h ,n)) #G(n') = G(n) + (n,n')
                        self.explored.append((gn + nnp +h,n))   #G(n') = G(n) + (n,n')
                    elif any(x[1] == n for x in self.frontier):
                        for x in self.frontier:
                            if (x[1] == n) and(x[0] > gn + nnp +h ): #G(n') = G(n) + (n,n')
                                self.previous[n] = current
                                self.frontier.remove(n)
                                self.grid.nodes[n].frontier = True
                                heappush(self.frontier,(gn + nnp +h,n)) #G(n') = G(n) + (n,n')
            if n == self.grid.goal:
                self.finished = True
                return
        self.grid.nodes[current].color_frontier= False
        self.grid.nodes[current].color_checked= True
