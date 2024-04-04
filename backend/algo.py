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
        self.n = n
        self.first_child_created = False
        self.depth = depth
        self.score = 0
        self.sum_score = 0
        self.children = []
        self.prev = prev
        self.can_move = self.find_children()

    def find_children(self):

        #If on leaf due to depth = 0
        if self.depth == 0:
            self.score = np.sum(self.grid)
            return "can't move"

        #If on leaf due to grid filled
        if np.all(self.grid):
            self.score = np.sum(self.grid)
            return "can't move"

        for i in range(self.n):
            break_loop = False
            for j in range(self.n):
                if self.grid[i, j]==0:
                    arr, updates = update(self.grid, i, j, self.chance)
                    if updates == 0:
                        continue
                    if self.first_child_created == False:
                        self.first_child_created = True
                        node=Node(self.n, self.chance*-1, arr, self.depth-1,self)
                        self.children.append(node)
                        #need to set score for this node after creation of first node
                        self.score = node.score
                    else:
                        #check if this node's further children even matter for parent
                        if self.prev != None:
                            if (self.chance == 1 and self.prev.score <= self.score) or (self.chance == -1 and self.prev.score >= self.score):
                                break_loop = True
                                break
                            else:
                                node=Node(self.n, self.chance*-1, arr, self.depth-1 ,self)
                                self.children.append(node)
                                #need to check if I need to update this node's score after each node creation
                                if self.chance == 1:
                                    if self.score < node.score:
                                        self.score = node.score
                                else:
                                    if self.score > node.score:
                                        self.score = node.score
                        else:
                            #below is same code as previous else
                            node=Node(self.n, self.chance*-1, arr, self.depth-1 ,self)
                            self.children.append(node)
                            #need to check if I need to update this node's score after each node creation
                            if self.chance == 1:
                                if self.score < node.score:
                                    self.score = node.score
                            else:
                                if self.score > node.score:
                                    self.score = node.score
            if break_loop:
                break
        
        if len(self.children) == 0:
            return "can't move"
        return "can move"
    
    def find_next_move(self):
        if self.children == []:
            if len(Node(self.n, self.chance*-1, self.grid, self.depth).children) == 0:
                return "game over", None 
            else:
                return "opponent chance", None
        ans_arr = [i for i in self.children if i.score == self.score]
        ans = ans_arr[0]
        for i in ans_arr[1:]:
            if i.score > ans.score:
                ans = i
        return ans.grid.tolist(), [i.grid.tolist() for i in self.children]
