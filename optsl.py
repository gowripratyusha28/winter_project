from random import seed, randint, random
import matplotlib.pyplot as plt


def my_range(start, end, B, h):
    while start < end:
        yield start
        start = B[h][start][end]


# function to construct levels using pivot matrix B
def compute_level(h, i, j, level, B):
    for a in my_range(i, j, B, h):
        b = B[h][a][j]
        level[b - 1] = h - 1
        if b > a + 1:
            compute_level(h - 1, a, b - 1, level, B)


def compute_optimal(p, n, level, cost_list, h_list):
    # weight matrix initialization
    (rows, cols) = (n + 1, n + 1)
    w = [[0.0 for i in range(cols)] for j in range(rows)]
    for i in range(0, n + 1):
        w[i][i] = p[i]
    for i in range(0, n + 1):
        for j in range(i + 1, n + 1):
            w[i][j] = w[i][j - 1] + p[j]
    # initialize base cases of D1, D2
    D1 = [[0.0 for i in range(cols)] for j in range(rows)]
    D2 = [[0.0 for i in range(cols)] for j in range(rows)]
    for i in range(0, n):
        D1[i][i] = D2[i][i] = 0
        D1[i][i + 1] = D2[i][i + 1] = p[i + 1]
    D1[n][n] = D2[n][n] = 0
    delta = D1
    delta_prev = D2
    # initialize the cost matrix delta_prev
    for i in range(0, n):
        for j in range(i + 2, n + 1):
            delta_prev[i][j] = delta_prev[i][j - 1] + p[j] * (j - i)
    # initializing min to the cost of the 1 - optimal skip list
    min = delta_prev[0][n] + 1
    cost_list.append(min)
    h_list.append(1)
    max = 1000  # max number of elements in the list
    logmax = 10  # maximum height
    # pivot matrix initialization #
    B = [[[0 for i in range(rows)] for j in range(cols)] for k in range(logmax)]
    for h in range(1, logmax):
        for i in range(0, n):
            B[h][i][i + 1] = i + 1
    # initialize the pivots matrix B[1] #
    for i in range(0, n):
        for j in range(i + 1, n + 1):
            B[1][i][j] = i + 1
    h = 2
    h1 = 2
    while True:
        # compute an optimal skip list of height h and its cost matrix delta #
        for i in range(0, n + 1):
            k = n - i
            for j in range(k + 2, n + 1):
                dmin = n * n
                for u in range(B[h][k][j - 1], B[h][k + 1][j] + 1):
                    val = delta_prev[k][u - 1] + delta[u][j] + w[u][j]
                    if (val <= dmin):
                        dmin = val
                        umin = u
                delta[k][j] = dmin
                B[h][k][j] = umin
        val = delta[0][n] + h
        cost_list.append(val)
        h_list.append(h)
        if val < min:
            tmp = delta
            delta = delta_prev
            delta_prev = tmp
            min = val
            h1 = h + 1
        if h == n:
            break
        h = h + 1
    # reconstructing the levels using B
    compute_level(h1, 0, n, level, B)


# Class to implement node
class Node(object):
    def __init__(self, key, level):
        self.key = key
        self.forward = [None] * (level + 1)


# Class for skip list
class SkipList(object):
    def __init__(self, max_lvl):
        self.MAXLVL = max_lvl
        self.header = self.createNode(self.MAXLVL, -1)
        self.level = 0

    def createNode(self, lvl, key):
        n = Node(key, lvl)
        return n

    def insertElement(self, key, levelarr, elem):
        update = [None] * (self.MAXLVL + 1)
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current is None or current.key != key:
            r = elem.index(key)
            rlevel = levelarr[r]

            if rlevel > self.level:
                for i in range(self.level + 1, rlevel + 1):
                    update[i] = self.header
                self.level = rlevel

            n = self.createNode(rlevel, key)

            for i in range(rlevel + 1):
                n.forward[i] = update[i].forward[i]
                update[i].forward[i] = n

    def displayList(self, elem):
        print("\n****Skip List****")
        head = self.header
        for lvl in range(self.level + 1):
            i = 0
            levl = self.level - lvl
            print("Level {}: ".format(levl), end=" ")
            node = head.forward[levl]
            while node is not None:
                if node.key == elem[i]:
                    print(format(node.key, "<3"), end=" ")
                    node = node.forward[levl]
                    i = i + 1
                else:
                    print("x  ", end=" ")
                    i = i + 1
            while i < len(elem):
                print("x  ", end=" ")
                i = i + 1
            print(" ")


if __name__ == "__main__":
    print("Enter # of elements in skip list:")
    n = int(input())  # number of elements in list
    elem = []  # elements in the list
    for i in range(0, n):  # to generate random integers
        elem.append(randint(0, 100))
    print("Random elements generated for skip list: ")
    elem.sort()
    print(elem)
    p = []  # access probabilities
    for i in range(0, n + 1):
        p.append(random())
    s = sum(p)
    p = [i / s for i in p]
    print("Access probabilities generated: ")
    print(p)
    print(sum(p))
    level = [0 for i in range(0, n + 1)]  # list to store the levels of the elements
    cost_list = []  # list to store all the costs
    h_list = []  # list to store all the heights
    compute_optimal(p, n, level, cost_list, h_list)
    for i in range(0, n):
        print("level of {} is {}".format(elem[i], level[i]))
    lst = SkipList(10)
    for i in elem:
        lst.insertElement(i, level, elem)
    lst.displayList(elem)
    plt.plot(h_list, cost_list)
    plt.xlabel('height')
    plt.ylabel('cost')
    plt.show()
