from collections import defaultdict


class Graph:
    def __init__(self, vertices):
        self.V = vertices  # V = cnt of vertexes
        self.graph = defaultdict(list)
        self.path = []

    # function to add an edge to graph
    def addOneEdge(self, u, v):
        self.graph[u].append(v)  # for c: for r: eddEdge

    def addTwoEdges(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    # remove edge u-v and v-u
    def rmvEdge(self, u, v):
        for index, value in enumerate(self.graph[u]):
            if value == v:
                self.graph[u].pop(index)
        for index, value in enumerate(self.graph[v]):
            if value == u:
                self.graph[v].pop(index)

    # DFS to count reachable vertices from v
    def DFSCount(self, v, visited):
        count = 1
        visited[v] = True
        for i in self.graph[v]:
            if not visited[i]:  # visited[i] == False
                count = count + self.DFSCount(i, visited)
        return count

    # The function to check if edge u-v can be next edge in Euler Path
    def isValidNextEdge(self, u, v):
        # The edge u-v is valid in one of the following two cases:

        # If v is the only adjacent vertex of u
        if len(self.graph[u]) == 1:
            return True
        else:
            '''vertices reachable from u'''
            visited = [False] * self.V
            count1 = self.DFSCount(u, visited)
            '''Remove edge (u, v) and after removing the edge, count vertices reachable from u'''
            self.rmvEdge(u, v)
            visited = [False] * self.V
            count2 = self.DFSCount(u, visited)
            '''Add the edge back to the graph'''
            self.addTwoEdges(u, v)
            '''If count1 is greater, then edge (u, v) is a bridge'''
            return False if count1 > count2 else True

    # Print Euler  starting from vertex u
    def printEulerUtil(self, u):
        # Recur for all the vertices adjacent to this vertex
        for v in self.graph[u]:

            # If edge u-v is not removed and it's a a valid next edge
            if self.isValidNextEdge(u, v):
                # print("%d - %d " % (u + 1, v + 1))
                # create path
                if self.path:  # if path not empty
                    self.path.pop()
                    self.path.append(u + 1)
                    self.path.append(v + 1)
                else:
                    self.path.append(u + 1)
                    self.path.append(v + 1)
                self.rmvEdge(u, v)
                self.printEulerUtil(v)

    def printEulerTour(self):
        # Find a vertex with odd degree
        u = -1
        for i in range(self.V):
            if len(self.graph[i]) % 2 != 0:
                u = i
                break
        if u == -1:
            print("There are no Euler Path")
        else:
            # Print tour starting from odd vertex
            self.printEulerUtil(u)


g1 = Graph(4)
g1.addTwoEdges(0, 1)
g1.addTwoEdges(0, 2)
g1.addTwoEdges(1, 2)
g1.addTwoEdges(2, 3)
g1.printEulerTour()
# print(g1.path)
