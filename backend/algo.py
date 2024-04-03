import numpy as np

def update(grid,i,j,v):
    ChildGrid = np.copy(grid)
    n = ChildGrid[0].size
    ChildGrid[i, j] = v
    gain = 0

    #check in +ve i dirn
    for k in range(i+1, n):
        if ChildGrid[k, j] == v:
            count = 0
            ChildGrid_1 = np.copy(ChildGrid)
            for l in range(i+1, k):
                if ChildGrid_1[l,j] == v*-1:
                    ChildGrid_1[l,j] = v
                    count +=1
                else:
                    count = 0
                    break
            if count > 0:
                gain += count
                ChildGrid = ChildGrid_1
            break
    
    #check in -ve i dirn
    for k in range(i-1, -1, -1):
        if ChildGrid[k, j] == v:
            count = 0
            ChildGrid_1 = np.copy(ChildGrid)
            for l in range(i-1, k, -1):
                if ChildGrid_1[l,j] == v*-1:
                    ChildGrid_1[l,j] = v
                    count +=1
                else:
                    count = 0
                    break
            if count > 0:
                gain += count
                ChildGrid = ChildGrid_1
            break

    #check in +ve j dirn
    for k in range(j+1, n):
        if ChildGrid[i, k] == v:
            count = 0
            ChildGrid_1 = np.copy(ChildGrid)
            for l in range(j+1, k):
                if ChildGrid_1[i,l] == v*-1:
                    ChildGrid_1[i,l] = v
                    count +=1
                else:
                    count = 0
                    break
            if count > 0:
                gain += count
                ChildGrid = ChildGrid_1
            break
    
    #check in -ve j dirn
    for k in range(j-1, -1, -1):
        if ChildGrid[i, k] == v:
            count = 0
            ChildGrid_1 = np.copy(ChildGrid)
            for l in range(j-1, k, -1):
                if ChildGrid_1[i,l] == v*-1:
                    ChildGrid_1[i,l] = v
                    count +=1
                else:
                    count = 0
                    break
            if count > 0:
                gain += count
                ChildGrid = ChildGrid_1
            break

    #check +i +j diagonal
    k = 1
    while i+k <n and j+k <n:
        if ChildGrid[i+k, j+k] == v:
            count = 0
            ChildGrid_1 = np.copy(ChildGrid)
            for l in range(1, k):
                if ChildGrid_1[i+l, j+l] == v*-1:
                    ChildGrid_1[i+l, j+l] = v
                    count +=1
                else:
                    count = 0
                    break
            if count > 0:
                gain += count
                ChildGrid = ChildGrid_1
            break
        k+=1
    
    #check +i -j diagonal
    k = 1
    while i+k <n and j-k >-1:
        if ChildGrid[i+k, j-k] == v:
            count = 0
            ChildGrid_1 = np.copy(ChildGrid)
            for l in range(1, k):
                if ChildGrid_1[i+l, j-l] == v*-1:
                    ChildGrid_1[i+l, j-l] = v
                    count +=1
                else:
                    count = 0
                    break
            if count > 0:
                gain += count
                ChildGrid = ChildGrid_1
            break
        k+=1

    #check -i +j diagonal
    k = 1
    while i-k >-1 and j+k <n:
        if ChildGrid[i-k, j+k] == v:
            count = 0
            ChildGrid_1 = np.copy(ChildGrid)
            for l in range(1, k):
                if ChildGrid_1[i-l, j+l] == v*-1:
                    ChildGrid_1[i-l, j+l] = v
                    count +=1
                else:
                    count = 0
                    break
            if count > 0:
                gain += count
                ChildGrid = ChildGrid_1
            break
        k+=1

    #check -i -j diagonal
    k = 1
    while i-k > -1 and j-k > -1:
        if ChildGrid[i-k, j-k] == v:
            count = 0
            ChildGrid_1 = np.copy(ChildGrid)
            for l in range(1, k):
                if ChildGrid_1[i-l, j-l] == v*-1:
                    ChildGrid_1[i-l, j-l] = v
                    count +=1
                else:
                    count = 0
                    break
            if count > 0:
                gain += count
                ChildGrid = ChildGrid_1
            break
        k+=1
    

    return ChildGrid, gain


class Node:
    def __init__(self,n, chance, grid, depth, prev = None):
        self.grid = grid
        self.chance = chance
        self.max_child = None
        self.n = n
        self.depth = depth
        self.score = 0
        self.children = []
        self.prev = prev
        self.can_move = self.find_children()

    def find_children(self):
        if self.depth == 0:
            self.score = np.sum(self.grid)
            self.max_child = np.sum(self.grid)
            return
        if np.all(self.grid):
            score = np.sum(self.grid)
            if score>0:
                self.score = 1
                self.max_child = 1
            elif score == 0:
                self.score =self.max_child= 0
            else:
                self.score = self.max_child = -1
            return
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i, j]==0:
                    arr, updates = update(self.grid, i, j, self.chance)
                    if updates == 0:
                        continue
                    node=Node(self.n, self.chance*-1, arr, self.depth-1, self)
                    self.children.append(node)
        if self.children == []:
            self.score = np.sum(self.grid)
            self.max_child = np.sum(self.grid)
            return "can't move"
        children_score = [i.score for i in self.children]
        self.score = sum(children_score)
        children_max_score = [i.max_child for i in self.children]
        self.max_child = max(children_max_score)
        return "can move"
    
    def find_next_move(self):
        if self.children == []:
            if len(Node(self.n, self.chance*-1, self.grid, self.depth).children) == 0:
                return "game over" , None
            else:
                return "opponent chance", None
        ans_arr = [i for i in self.children if i.max_child == self.max_child]
        ans = ans_arr[0]
        for i in ans_arr[1:]:
            if i.score > ans.score:
                ans = i
        return ans.grid.tolist(), [i.grid.tolist() for i in ans.children]
