import math
from random import seed, randint, random
import matplotlib.pyplot as plt

#Class to implement node
class Node(object):
	def __init__(self, key, level, wi):
		self.key = key
		self.forward = [None]*(level+1)
		self.height = level
		self.weight = wi

#Class for skip list
class SkipList(object):
	def __init__(self, max_lvl):
		self.MAXLVL = max_lvl
		self.header = self.createNode(self.MAXLVL, -1, -1)
		self.level = 0

	def createNode(self, lvl, key, w):
		n = Node(key, lvl, w)
		return n

	# function to calculate rank of a node
	def rank(self, wi, a):
		if wi == 0:
			return 0
		return math.floor(math.log(wi,a))

	def insertElement(self, key, w, a, b, elem):
		update = [None]*(self.MAXLVL+1)
		current = self.header

		for i in range(self.level, -1, -1):
			while current.forward[i] and current.forward[i].key < key:
				current = current.forward[i]
			update[i] = current

		current = current.forward[0]

		if current == None or current.key != key:
			rlevel = self.rank(w,a) 

			if rlevel > self.level:
				for i in range(self.level+1, rlevel+1):
					update[i]=self.header
				self.level = rlevel

			n = self.createNode(rlevel,key,w)
			
			for i in range(rlevel+1):
				n.forward[i] = update[i].forward[i]
				update[i].forward[i] = n

		lst.I2(key,elem,a)
		#lst.displayList(elem)
		lst.I1(elem,b)

		#print("Inserted ",key)

	# function to get height of i-
	def height_prev_elem(self, key, elem):
		# get the index of key in the elem array
		i = elem.index(key)
		if i != 0:
			key1 = elem[i-1] # index of i-
			head = self.header
			node = head.forward[0]
			while node != None:
				if node.key == key1:
					return node.height # height of i-
					break
				node = node.forward[0]
		else: # if the key is the first element then there is no i-
			return -1

	# function to get height of i+
	def height_next_elem(self, key, elem):
		i = elem.index(key)
		if i != len(elem) - 1:
			key1 = elem[i+1] # index of i+
			head = self.header
			node = head.forward[0]
			while node != None:
				if node.key == key1:
					return node.height # height of i+
					break
				node = node.forward[0]
		else: # if the key is the last element then there is no i+
			return -1

	# function to get level-j predecessor of given element
	def level_j_predecessor(self, j, key):
		head = self.header
		node = head.forward[j]
		pred = -1
		while node != None:
			if node.key < key:
				pred = node.key
			elif node.key == key:
				break
			node = node.forward[j]
		return pred

	# function to get level-j successor of given element
	def level_j_successor(self, j, key):
		head = self.header
		node = head.forward[j]
		succ = -1
		while node != None:
			if node.key > key:
				succ = node.key
				break
			node = node.forward[j]
		return succ

	def left_profile(self, key, elem, Lij, PL):
		h_prev = self.height_prev_elem(key, elem)
		for j in range(h_prev, self.level+1):
			l = self.level_j_predecessor(j, key)
			k1 = j
			flag = 1
			for k in Lij:
				if k == l:
					flag = 0
					break
			if flag == 1 and l != -1:
				Lij.append(l)
				PL.append(k1)
		#for k in range(0,len(Lij)):
			#print(Lij[k]," - ",PL[k])

	def right_profile(self, key, elem, Rij, RL):
		h_next = self.height_next_elem(key, elem)
		for j in range(h_next, self.level+1):
			r = self.level_j_successor(j, key)
			k1 = j
			flag = 1
			for k in Rij:
				if k == r:
					flag = 0
					break
			if flag == 1 and r != -1:
				Rij.append(r)
				RL.append(k1)
		#for k in range(0,len(Rij)):
			#print(Rij[k], " - ",RL[k])

	def demote_node(self, key, new_height):
		update = [None]*(self.MAXLVL+1)
		current = self.header
		for i in range(self.level, -1, -1):
			while (current.forward[i] and current.forward[i].key < key):
				current = current.forward[i]
			update[i] = current
		current = current.forward[0]
		if current != None and current.key == key:
			for i in range(new_height+1,self.level+1):
				if update[i].forward[i] != current:
					break
				update[i].forward[i] = current.forward[i]
			while (self.level > 0 and self.header.forward[self.level] == None):
				self.level -= 1
		current.height = new_height

	def promote_node(self, key, new_height):
		#delete part
		update = [None]*(self.MAXLVL+1)				
		current = self.header
		for i in range(self.level,-1,-1):
			while(current.forward[i] and current.forward[i].key < key):
				current = current.forward[i]
			update[i] = current
		current = current.forward[0]
		w = current.weight
		if current != None and current.key == key:
			for i in range(self.level+1):
				if update[i].forward[i] != current:
					break
				update[i].forward[i] = current.forward[i]
			while(self.level>0 and self.header.forward[self.level] == None):
				self.level -= 1
		#insert part
		update = [None]*(self.MAXLVL+1)
		current = self.header
		for i in range(self.level,-1,-1):
			while(current.forward[i] and current.forward[i].key < key):
				current = current.forward[i]
			update[i] = current
		current = current.forward[0]
		if current == None or current.key != key:
			if new_height > self.level:
				for i in range(self.level+1,new_height+1):
					update[i] = self.header
				self.level = new_height
			n = self.createNode(new_height,key,w)
			for i in range(new_height+1):
				n.forward[i] = update[i].forward[i]
				update[i].forward[i] = n

	def search(self, key):
		current = self.header
		for i in range(self.level,-1,-1):
			while(current.forward[i] and current.forward[i].key < key):
				current = current.forward[i]
		current = current.forward[0]
		return current

	# check if the node violates I2 and demote node
	def I2(self, key, elem, a):
		h_prev = self.height_prev_elem(key,elem)		
		current = self.search(key)
		wi = current.weight
		ri = self.rank(wi, a)
		Lij = []
		PL = []
		self.left_profile(key,elem,Lij,PL)
		for j in range(h_prev,ri+1):
			flag = 0
			for check in PL:
				if check == j:
					flag = 1
					break
			if flag == 1:       # if j ∈ PL(i)
				#print("j = ",j)
				index_j = PL.index(j)
				u = Lij[index_j] # u = L ij
				#print("u = ",u)
				node_u = self.search(u)
				wu = node_u.weight
				ru = self.rank(wu,a)
				#print("ru = ",ru)
				#print("height = ",node_u.height)
				for i in range(ru+1,node_u.height+1): # rx < i <= hx
					#print("entered for j = ",j)
					#print("i = ",i)
					consec_key = self.level_j_successor(i,node_u.key)
					consec_node = self.search(consec_key)
					node_check = node_u
					# check if there are atleast a nodes of height i-1
					count = 0
					node_check = node_check.forward[0]
					while node_check != consec_node:
						if node_check.height > i-2:
							count = count+1
						node_check = node_check.forward[0]
					if count < a: # I2 violated
						# check if u is i-
						#print("entered again")
						index_i = elem.index(key)
						prev_key = elem[index_i-1]
						if u == prev_key: # if u is i- then demote u to height ru
							self.demote_node(node_u.key,ru)
						else: # if u is not i- then demote to max(j',ru)
							#print("yes")
							j1 = 0
							if index_j != 0:
								j1 = PL[index_j-1]
							hu1 = max(j1,ru)
							self.demote_node(node_u.key,hu1) 

	# check if node violates I1
	def I1(self, elem, b):
		node = self.header
		for j in range(0,self.level+1):
			#print("j = ",j)
			count = 0
			current = node.forward[j]
			start = node.forward[j]
			prev = -1
			while current != None:
				if current.height == j and prev != -1:
					count = count + 1
					#print("1 = ",current.key)
					current = current.forward[j]
					if count > b:
						start = start.forward[j]
						start = start.forward[j]
						current = start.forward[j]
						self.promote_node(start.key,j+1)
						prev = -1
				elif current.height == j and prev == -1:
					#print("2 = ",current.key)
					count = 1
					prev = 1
					start = current
					current = current.forward[j]
				elif current.height != j:
					#print("3 = ",current.key)
					prev = -1
					count = 0
					current = current.forward[j]

	def fingerSearch(self, key1, key2):
		head = self.header
		node1 = self.search(key1)		

	def displayList(self, elem):
		print("\n****Skip List****")
		head = self.header
		for lvl in range(self.level+1):
			i = 0
			levl = self.level-lvl
			print("Level {}: ".format(levl), end=" ")
			node = head.forward[levl]
			while node != None:
				if node.key == elem[i]:
					print(format(node.key, "<3"), end=" ")
					node = node.forward[levl]
					i = i+1
				else:
					print("x  ",end = " ")
					i = i+1
			while(i < len(elem)):
				print("x  ",end = " ")
				i = i+1
			print(" ")

	def displayHeight(self):
		print("\nheights")
		current = self.header
		node = current.forward[0]
		while(node != None):
			print(node.key, "-", node.height)
			node = node.forward[0]
		print(" ")

	def cost(self, elem, p):
		h = [] # to store horizontal costs of all the elements
		for key in elem:
			c = 0
			current = self.header
			for i in range(self.level,-1,-1):
				while(current.forward[i] and current.forward[i].key < key):
					current = current.forward[i]
					c = c + 1
			current = current.forward[0]
			c = c + 1
			h.append(c)
		#print(h)
		total_cost = 0
		for i in range(len(h)):
			total_cost = total_cost + (h[i]*p[i])
		total_cost = total_cost + self.level
		return total_cost


if __name__ == "__main__":
	print("Enter n:") 
	n = int(input()) #number of elements in list
	print("Enter elems: ")
	elem = []
	elem = list(map(int,input().strip().split()))[:n]
	print(elem)
	elem.sort()
	print(elem)
	print("Enter access weights:")
	w = [] #list of weights
	w = list(map(float,input().strip().split()))[:n]
	# print(w)
	p = []
	for i in w:
		p.append(i/sum(w))
	#print(p)
	a = 2
	b = 4	
	lst = SkipList(10)
	for i in range(n):
		lst.insertElement(elem[i],w[i],a,b,elem)
		lst.displayList(elem)
		lst.displayHeight()
	lst.cost(elem,p)
