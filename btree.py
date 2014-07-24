#!/usr/bin/python
from __future__ import print_function
import bisect 
import random
import cProfile

class Tree:

	def insert(self, key):
		return None

	def delete(self, key):
		return None

	def find(self, key):
		return None


class Node:

	def __init__(self):
		return None





class BTree(Tree):
	
	def __init__(self):
		self._root = BNode()

	def insert(self,key,node=None, parentNode=None):
		if node is None:
			node = self._root

		if node.isLeaf():
			if node.isFull():
				middle,left,right = node.split()
				if parentNode is None:
					parentNode = BNode([middle],[left,right])
					self._root = parentNode
				else:
					parentNode.splitInterval(middle,left,right)

				if key>middle:
					right.insertKey(key)
				else:
					left.insertKey(key)
				return True
			else:
				node.insertKey(key)
				return True
		else:
			if node.isFull():
				middle,left,right = node.split()
				if parentNode is None:
					parentNode = BNode([middle],[left,right])
					self._root = parentNode
				else:
					parentNode.splitInterval(middle,left,right)

				nextNode = left.findRightChild(key)
				if nextNode is not None:
					return self.insert(key,nextNode,left)

				nextNode = right.findRightChild(key)
				if nextNode is not None:
					return self.insert(key,nextNode,right)

				return False
			else:
				nextNode = node.findRightChild(key)
				if nextNode is not None:
					return self.insert(key,nextNode,node)

				return False


	def delete(self,key):
		return None
	
	def find(self,key,node=None):
		if node is None:
			node = self._root

		if node.hasKey(key):
			return key

		if node.isLeaf():
			return None
		
		nextNode = node.findRightChild(key)
		if nextNode is not None:
			return self.find(key,nextNode)
		else:
			return None

	def output(self,node = None, space = None):
		if node is None:
			node = self._root
		if space is None:
			space = ''
		print(space,end='')
		for x in node._keys:
			print(x,'',end='')
		print(' ')
		for x in node._children:	
			if x is not None:
				self.output(x,space+' ')





class BNode(Node):
	maxSize = 50


	def __init__(self, keys = None, children = None):
		if keys is None:
			self._keys = []
		else:
			self._keys = keys

		if children is None:
			self._children = [None for i in xrange(0,BNode.maxSize*2)]
			self._hasChildren = False
		else:
			self._hasChildren = False
			for x in children:
				if x is not None:
					self._hasChildren = True		
			self._children = children
			while len(self._children)<BNode.maxSize*2:
				self._children.append(None)
			
	def _findRightPos(self,key):
		pos = bisect.bisect_left(self._keys,key)          
		return pos

	def __getslice__(self,i,j):
		return BNode(self._keys[i:j],self._children[i:j])


	def isFull(self):
		return len(self._keys)==2*BNode.maxSize-1

	def isEmpty(self):
		return len(self._keys)==0

	def isLeaf(self):
		return not self._hasChildren

	def hasKey(self,key):
		pos = bisect.bisect_left(self._keys,key)          
		if pos!=len(self._keys) and self._keys[pos]==key:
			return True
		else:
			return False
		

	def findRightChild(self,key):
		ind = self._findRightPos(key)
		if len(self._children)>ind:
			return self._children[ind]
		else:
			return None

	def insertKey(self,key):
		ind = self._findRightPos(key)
		self._keys.insert(ind,key)

	def splitInterval(self,key,left,right):
		ind = self._findRightPos(key)
		self._keys.insert(ind,key)
		self._children.pop(ind)
		self._children.insert(ind,right)
		self._children.insert(ind,left)

		
	def split(self):
		if self.isFull():
			t = BNode.maxSize*2-1
			newParams = [self._keys[t//2]]
			newParams.append(self[:t//2])
			newParams.append(self[t//2+1:])
			return newParams
		else:
			return None


def main():
	

	tree = BTree()
	test = dict()
	pr = cProfile.Profile()
	pr.enable()
	for i in xrange(1,1000):
		rand = random.randint(0,10000)
		if rand in test:
			test[rand]+=1
		else:
			test[rand]=1
	 	tree.insert(rand)
	pr.disable()
	pr.print_stats()
	
	pr = cProfile.Profile()
	pr.enable()

	for i in xrange(1,100):
	 	rand = random.randint(0,10000)
	 	print(rand,' ',tree.find(rand),' ',rand in test)

	pr.disable()
	pr.print_stats()

	#for x in test:
	#	print(x,'',test[x])
	tree.output()
	


if __name__ == '__main__':
	main()


