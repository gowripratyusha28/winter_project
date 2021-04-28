from random import seed, randint, random
import matplotlib.pyplot as plt
import csv


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


def compute_optimal(p, n, level, cost_min):
    # weight matrix initialization
    (rows, cols) = (n + 1, n + 1)
    w = [[0.0 for i in range(cols)] for j in range(rows)]
    #print(type(w))
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
    max = 1000  # max number of elements in the list
    logmax = 100 # maximum height
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
    while True:
        # compute an optimal skip list of height h and its cost matrix delta #
        for i in range(0, n + 1):
            k = n - i
            for j in range(k + 2, n + 1):
                dmin = n * n * n
                #umin = j
                for u in range(B[h][k][j - 1], B[h][k + 1][j] + 1):
                    val = delta_prev[k][u - 1] + delta[u][j] + w[u][j]
                    if (val <= dmin):
                        dmin = val
                        umin = u
                delta[k][j] = dmin
                B[h][k][j] = umin
        val = delta[0][n] + h
        if val < min:
            tmp = delta
            delta = delta_prev
            delta_prev = tmp
            min = val
        else:
            break
        h = h + 1
    cost_min.append(min)
    # reconstructing the levels using B
    compute_level(h, 0, n, level, B)


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
                    print(format(node.key, "<4"), end=" ")
                    node = node.forward[levl]
                    i = i + 1
                else:
                    print("x   ", end=" ")
                    i = i + 1
            while i < len(elem):
                print("x   ", end=" ")
                i = i + 1
            print(" ")


if __name__ == "__main__":

    ### facebook cluster A ###
    fb_A = "data/real_data/fb_clustA_10k_100hosts.csv"
    fields_fb_A = []
    rows_fb_A = []

    with open(fb_A,'r') as csvfile:
        csvreader_fb_A = csv.reader(csvfile)
        fields_fb_A = next(csvreader_fb_A)
        rows_fb_A = [[int(row[0]),int(row[1])] for row in csvreader_fb_A if row]

    m = csvreader_fb_A.line_num
    print(m)

    freq_fb_A = [0 for i in range(0, 100)]
    j = 0
    req_fb_A = []
    cost_list_fb_A = []
    for row in rows_fb_A:
        flag = 0
        for col in row:
            if col == -99:
                flag = 1
                if len(req_fb_A) != 0:
                    if req_fb_A[-1] != 2*j:
                        level = [0 for i in range(0,101)]
                        p = []
                        p.append(0.0)
                        k = 2*j
                        for i in freq_fb_A:
                            p.append(i/k)
                        compute_optimal(p,100,level,cost_list_fb_A)
                        req_fb_A.append(k)
                else:
                    level = [0 for i in range(0,101)]
                    p = []
                    p.append(0.0)
                    k = 2*j
                    for i in freq_fb_A:
                        p.append(i/k)
                    compute_optimal(p,100,level,cost_list_fb_A)
                    req_fb_A.append(k)
            else:
                freq_fb_A[col] = freq_fb_A[col] + 1
        if flag == 0:
            j = j + 1

    print("facebook cluster A")
    print(req_fb_A)
    print(cost_list_fb_A)

    ### facebook cluster B ###
    fb_B = "data/real_data/fb_clustB_10k_100hosts.csv"
    fields_fb_B = []
    rows_fb_B = []

    with open(fb_B,'r') as csvfile:
        csvreader_fb_B = csv.reader(csvfile)
        fields_fb_B = next(csvreader_fb_B)
        rows_fb_B = [[int(row[0]),int(row[1])] for row in csvreader_fb_B if row]

    m = csvreader_fb_B.line_num
    print(m)

    freq_fb_B = [0 for i in range(0, 100)]
    j = 0
    req_fb_B = []
    cost_list_fb_B = []
    for row in rows_fb_B:
        flag = 0
        for col in row:
            if col == -99:
                flag = 1
                if len(req_fb_B) != 0:
                    if req_fb_B[-1] != 2*j:
                        level = [0 for i in range(0,101)]
                        p = []
                        p.append(0.0)
                        k = 2*j
                        for i in freq_fb_B:
                            p.append(i/k)
                        compute_optimal(p,100,level,cost_list_fb_B)
                        req_fb_B.append(k)
                else:
                    level = [0 for i in range(0,101)]
                    p = []
                    p.append(0.0)
                    k = 2*j
                    for i in freq_fb_B:
                        p.append(i/k)
                    compute_optimal(p,100,level,cost_list_fb_B)
                    req_fb_B.append(k)
            else:
                freq_fb_B[col] = freq_fb_B[col] + 1
        if flag == 0:
            j = j + 1
    
    print("facebook cluster B")
    print(req_fb_B)
    print(cost_list_fb_B)

    ### hpc cesarNek ###
    hpc_cesar = "data/real_data/hpc_cesarNek_10k_100hosts.csv"
    fields_hpc_cesar = []
    rows_hpc_cesar = []

    with open(hpc_cesar,'r') as csvfile:
        csvreader_hpc_cesar = csv.reader(csvfile)
        fields_hpc_cesar = next(csvreader_hpc_cesar)
        rows_hpc_cesar = [[int(row[0]),int(row[1])] for row in csvreader_hpc_cesar if row]

    m = csvreader_hpc_cesar.line_num
    print(m)

    freq_hpc_cesar = [0 for i in range(0, 100)]
    j = 0
    req_hpc_cesar = []
    cost_list_hpc_cesar = []
    for row in rows_hpc_cesar:
        flag = 0
        for col in row:
            if col == -99:
                flag = 1
                if len(req_hpc_cesar) != 0:
                    if req_hpc_cesar[-1] != 2*j:
                        level = [0 for i in range(0,101)]
                        p = []
                        p.append(0.0)
                        k = 2*j
                        for i in freq_hpc_cesar:
                            p.append(i/k)
                        compute_optimal(p,100,level,cost_list_hpc_cesar)
                        req_hpc_cesar.append(k)
                else:
                    level = [0 for i in range(0,101)]
                    p = []
                    p.append(0.0)
                    k = 2*j
                    for i in freq_hpc_cesar:
                        p.append(i/k)
                    compute_optimal(p,100,level,cost_list_hpc_cesar)
                    req_hpc_cesar.append(k)
            else:
                freq_hpc_cesar[col] = freq_hpc_cesar[col] + 1
        if flag == 0:
            j = j + 1
    
    print("hpc cesarNek")
    print(req_hpc_cesar)
    print(cost_list_hpc_cesar)

    ### pfab_08 ###
    pfab_08 = "data/real_data/pfab_08_10k_100hosts.csv"
    fields_pfab_08 = []
    rows_pfab_08 = []

    with open(pfab_08,'r') as csvfile:
        csvreader_pfab_08 = csv.reader(csvfile)
        fields_pfab_08 = next(csvreader_pfab_08)
        rows_pfab_08 = [[int(row[0]),int(row[1])] for row in csvreader_pfab_08 if row]

    m = csvreader_pfab_08.line_num
    print(m)

    freq_pfab_08 = [0 for i in range(0, 100)]
    j = 0
    req_pfab_08 = []
    cost_list_pfab_08 = []
    for row in rows_pfab_08:
        flag = 0
        for col in row:
            if col == -99:
                flag = 1
                if len(req_pfab_08) != 0:
                    if req_pfab_08[-1] != 2*j:
                        level = [0 for i in range(0,101)]
                        p = []
                        p.append(0.0)
                        k = 2*j
                        for i in freq_pfab_08:
                            p.append(i/k)
                        compute_optimal(p,100,level,cost_list_pfab_08)
                        req_pfab_08.append(k)
                else:
                    level = [0 for i in range(0,101)]
                    p = []
                    p.append(0.0)
                    k = 2*j
                    for i in freq_pfab_08:
                        p.append(i/k)
                    compute_optimal(p,100,level,cost_list_pfab_08)
                    req_pfab_08.append(k)
            else:
                freq_pfab_08[col] = freq_pfab_08[col] + 1
        # if 2*j >= 30000:
        #     break
        if flag == 0:
            j = j + 1
    
    print("pfab_08")
    print(req_pfab_08)
    print(cost_list_pfab_08)

    ### microsoft ###
    hpc_microsoft = "data/real_data/microsoft_10k_100hosts.csv"
    fields_microsoft = []
    rows_microsoft = []

    with open(hpc_microsoft,'r') as csvfile:
        csvreader_microsoft = csv.reader(csvfile)
        fields_microsoft = next(csvreader_microsoft)
        rows_microsoft = [[int(row[0]),int(row[1])] for row in csvreader_microsoft if row]

    m = csvreader_microsoft.line_num
    print(m)

    freq_microsoft = [0 for i in range(0, 100)]
    j = 0
    req_microsoft = []
    cost_list_microsoft = []
    for row in rows_microsoft:
        flag = 0
        for col in row:
            if col == -99:
                flag = 1
                if len(req_microsoft) != 0:
                    if req_microsoft[-1] != 2*j:
                        level = [0 for i in range(0,101)]
                        p = []
                        p.append(0.0)
                        k = 2*j
                        for i in freq_microsoft:
                            p.append(i/k)
                        compute_optimal(p,100,level,cost_list_microsoft)
                        req_microsoft.append(k)
                else:
                    level = [0 for i in range(0,101)]
                    p = []
                    p.append(0.0)
                    k = 2*j
                    for i in freq_microsoft:
                        p.append(i/k)
                    compute_optimal(p,100,level,cost_list_microsoft)
                    req_microsoft.append(k)
            else:
                freq_microsoft[col] = freq_microsoft[col] + 1
        if flag == 0:
            j = j + 1
    
    print("microsoft")
    print(req_microsoft)
    print(cost_list_microsoft)

    ### plot ###
    plt.plot(req_fb_A, cost_list_fb_A, label = "fb_clusterA")
    plt.plot(req_fb_B, cost_list_fb_B, label = "fb_clusterB")
    plt.plot(req_hpc_cesar, cost_list_hpc_cesar, label = "hpc cesarNek")
    plt.plot(req_pfab_08, cost_list_pfab_08, label = "pfab_08")
    plt.plot(req_microsoft, cost_list_microsoft, label = "microsoft")
    plt.xlabel('# requests')
    plt.ylabel('cost')
    plt.legend()
    plt.show()



    # level = [0 for i in range(0,101)]
    # p = []
    # p.append(0.0)
    # for i in freq_fb_A:
    #     p.append(i/352)
    # print(sum(p))
    # compute_optimal(p,100,level,cost_min)

    # n = int(input("Enter # of elements in skip list: "))  # number of elements in list
    # req = int(input("Enter # of requests in skip list: ")) # number of requests in list
    # elem = []
    # for i in range(1,n+1):
    #     elem.append(i)
    # seed(2)
    # requests = []
    # for i in range(0,req):
    #     requests.append(randint(1,n))
    # #print(requests)
    # freq = []
    # for i in range(0,n):
    #     freq.append(0)
    # for i in requests:
    #     freq[i-1] = freq[i-1] + 1
    # #print(freq)
    # p = []
    # p.append(0.0)
    # for i in freq:
    #     p.append(i/req)
    # #print(p)
    # level = [0 for i in range(0, n + 1)]  # list to store the levels of the elements
    # compute_optimal(p, n, level)
    # for i in range(0, n):
    #     print("level of {} is {}".format(elem[i], level[i]))
    # lst = SkipList(10)
    # for i in elem:
    #     lst.insertElement(i, level, elem)
    # lst.displayList(elem)