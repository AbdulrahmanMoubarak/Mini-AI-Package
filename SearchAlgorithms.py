import collections

class MazeProblem:
    init_state = []
    Goal_id = 0
    start_id = 0
    RowCount = 0
    ColCount = 0

    def __init__(self, Maze_str):
        self.init_state = CreateMaze(Maze_str)
        self.ColCount = count_cols(Maze_str)
        self.RowCount = count_rows(Maze_str)
        self.init_state = get_Neighbours(self.init_state, self.RowCount)
        self.start_id = GetStartID(self.init_state)
        self.Goal_id = GetGoalID(self.init_state)


class Node:
    id = None  # Unique value for each node.
    up = None  # Represents value of neighbors (up, down, left, right).
    down = None
    left = None
    right = None
    previousNode = None  # Represents value of neighbors.
    edgeCost = None  # Represents the cost on the edge from any parent to this node.
    gOfN = None  # Represents the total edge cost
    hOfN = None  # Represents the heuristic value
    heuristicFn = None  # Represents the value of heuristic function

    def __init__(self, value):
        self.value = value


class SearchAlgorithms:
    ''' * DON'T change Class, Function or Parameters Names and Order
        * You can add ANY extra functions,
          classes you need as long as the main
          structure is left as is '''
    path = []  # Represents the correct path from start node to the goal node.
    fullPath = []  # Represents all visited nodes from the start node to the goal node.
    totalCost = -1  # Represents the total cost in case using UCS, AStar (Euclidean or Manhattan)

    def __init__(self, mazeStr, heristicValue=None):
        ''' mazeStr contains the full board
         The board is read row wise,
        the nodes are numbered 0-based starting
        the leftmost node'''
        self.path.clear()
        self.fullPath.clear()
        self.problem = MazeProblem(mazeStr)
        self.Not_visited = collections.deque()
        self.costList = heristicValue
        pass

    def DLS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        start_node = self.problem.start_id
        limit = GetLimit(self.problem.init_state)
        self.Not_visited.append(self.problem.start_id)
        self.rec_dls(start_node, self.problem.init_state, limit)
        return self.path, self.fullPath

    def rec_dls(self, node, problem, limit):
        if len(self.Not_visited) == 0:
            return False
        node = self.Not_visited.popleft()
        if node == self.problem.Goal_id:
            self.path = GetPath(self.problem.init_state[node])
            return self.path
        if limit == 0:
            return False
        if node not in self.fullPath:
            self.fullPath.append(node)
            childList = getChilds(node, self.problem.init_state)
            for child in childList:
                if child not in self.Not_visited and child not in self.fullPath:
                    self.problem.init_state[child].previousNode=self.problem.init_state[node]
                    self.Not_visited.appendleft(child)
            #current = self.Not_visited.popleft()
            return self.rec_dls(node, problem, limit-1)




    def BDS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        NotVisited1 = collections.deque() #Start
        NotVisited2 = collections.deque() #End

        fullpath1 = []
        fullpath2 = []


        NotVisited1.append(self.problem.start_id)
        NotVisited2.append(self.problem.Goal_id)



        while True:

            if len(NotVisited1) == 0 or len(NotVisited2) == 0:
                return False
            node1 = NotVisited1.popleft()
            node2 = NotVisited2.popleft()

            if node1 == node2:
                p1 = GetPath(self.problem.init_state[node1])
                p2 = GetPath(self.problem.init_state[node2].previousNode)
                p2.reverse()
                self.path = p1 + p2
                self.fullPath = fullpath1 + fullpath2
                return self.path, self.fullPath

            if node1 not in fullpath1:
                fullpath1.append(node1)
                childs1 = getChilds(node1, self.problem.init_state)
                for child in childs1:
                    if self.problem.init_state[child].previousNode != None and child not in fullpath1 and child not in NotVisited1:
                        p1 = GetPath(self.problem.init_state[node1])
                        p2 = GetPath(self.problem.init_state[child])
                        p2.reverse()
                        self.path = p1 + p2
                        self.fullPath = fullpath1 + fullpath2
                        return self.path, self.fullPath
                    else:
                        if child not in fullpath1 and child not in NotVisited1:
                            self.problem.init_state[child].previousNode = self.problem.init_state[node1]
                            NotVisited1.append(child)

            if node2 not in fullpath2:
                fullpath2.append(node2)
                childs2 = getChilds(node2, self.problem.init_state)
                for child2 in childs2:
                    if self.problem.init_state[child2].previousNode != None and child2 not in fullpath2 and child2 not in NotVisited2:
                        p1 = GetPath(self.problem.init_state[child2])
                        p2 = GetPath(self.problem.init_state[node2])
                        p2.reverse()
                        self.path = p1 + p2
                        self.fullPath = fullpath1 + fullpath2
                        return self.path, self.fullPath
                    else:
                        if child2 not in fullpath2 and child2 not in NotVisited2:
                            self.problem.init_state[child2].previousNode = self.problem.init_state[node2]
                            NotVisited2.append(child2)

        return False


    def BFS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        self.problem.init_state = Intit_cost(self.problem.init_state, self.costList)
        openlist = []
        openlist.append((self.problem.init_state[self.problem.start_id].heuristicFn,self.problem.start_id))
        self.fullPath.append(self.problem.start_id)
        self.totalCost = 0
        while len(self.fullPath) != 0 and len(openlist) != 0:
            if len(self.fullPath) == 0 or len(openlist) == 0:
                return False
            openlist.sort()
            bestH = openlist[0]
            #self.totalCost += bestH[0]
            best_id = bestH[1]
            if best_id == self.problem.Goal_id:
                self.totalCost = self.problem.init_state[self.problem.Goal_id].heuristicFn
                self.path = GetPath(self.problem.init_state[best_id])
                return self.path, self.fullPath, self.totalCost
            childList = getChilds(best_id, self.problem.init_state)
            for child in childList:
                if child not in self.fullPath and child not in self.path:
                    self.problem.init_state[child].previousNode = self.problem.init_state[best_id]
                    self.problem.init_state[child].heuristicFn = self.problem.init_state[child].hOfN + self.problem.init_state[best_id].heuristicFn
                    self.fullPath.append(child)
                    openlist.append((self.problem.init_state[child].heuristicFn,child))
            openlist.remove(openlist[0])



def CreateMaze(MazeStr):
    MyMaze = []
    row = []
    count = 0;
    for character in MazeStr:
        count += 1;
        if character == ' ' or count == (len(MazeStr)):
            if count == len(MazeStr):
                row.append(character)
            RowToStr = str(row)
            MyMaze.append(RowToStr)
            row.clear()
        elif character != ',':
            row.append(character)
    ID_count = 0
    Node_List = []
    for OneRow in MyMaze:
        for node in OneRow:
            if node == 'S' or node == '.' or node == '#' or node == 'E':
                MyNode = Node(node)
                MyNode.id = ID_count
                Node_List.append(MyNode)
                ID_count += 1
    return Node_List

def count_rows(MazeStr):
    count = 0;
    for char in MazeStr:
        if char == ' ':
            return count
        if char != ',':
            count += 1
    return count

def count_cols(MazeStr):
    count = 0;
    for char in MazeStr:
        if char == ' ':
            count += 1
    return (count+1)

def get_Neighbours(Node_List, row):
    node_count = 0
    for node in Node_List:

        if (node_count - 1) >= 0 and (node_count)% row != 0:
            if (Node_List[node_count - 1].value) != '#':
                node.left = Node_List[node_count - 1]
        if (node_count + 1) <= len(Node_List)-1 and (node_count + 1)% row != 0:
            if (Node_List[node_count+1].value) != '#':
                node.right = Node_List[node_count+1]
        if (node_count - row) >= 0:
            if (Node_List[node_count - row].value) != '#':
                node.up = Node_List[node_count - row]
        if (node_count + row) <= len(Node_List)-1:
            if (Node_List[node_count + row ].value) != '#':
                node.down = Node_List[node_count + row]
        node_count += 1
    return Node_List

def getChilds(nodeID, problem):
    node = problem[nodeID]
    mylist = []
    if node.left != None:
        mylist.append(node.left.id)
    if node.right != None:
        mylist.append(node.right.id)
    if node.up != None:
        mylist.append(node.up.id)
    if node.down != None:
        mylist.append(node.down.id)
    return mylist


def GetStartID(Node_List):
    for item in Node_List:
        if item.value == 'S':
            return item.id
    return 0

def GetGoalID(Node_list):
    for item in Node_list:
        if item.value == 'E':
            return item.id
    return 0

def GetLimit(Node_lis):
    count = 0
    for item in Node_lis:
        if item.value != '#':
            count += 1
    return count

def GetPath(node):
    parents = []
    x=[]
    while True:
        parents.append(node)
        x.append(node.id)
        node = node.previousNode
        if node == None:
            break
    x.reverse()
    parents.reverse()
    return x

def  Intit_cost(Maze, cost_list):
    for node in Maze:
        node.hOfN = cost_list[node.id]
        node.heuristicFn = cost_list[node.id]
    return Maze

def main():
    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath = searchAlgo.DLS()
    print('**DFS**\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')

                #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath = searchAlgo.BDS()
    print('**BFS**\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')
                #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.', [0, 15, 2, 100, 60, 35, 30, 3
                                                                                                             , 100, 2, 15, 60, 100, 30, 2
                                                                                                             , 100, 2, 2, 2, 40, 30, 2, 2
                                                                                                             , 100, 100, 3, 15, 30, 100, 2
                                                                                                             , 100, 0, 2, 100, 30])
    path, fullPath, TotalCost = searchAlgo.BFS()
    print('** UCS **\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\nTotal Cost: ' + str(
        TotalCost) + '\n\n')
               #######################################################################################

main()