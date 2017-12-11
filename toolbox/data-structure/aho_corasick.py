# -*- coding:utf-8 -*-
# ------ Import ------ #

import os
import sys
from collections import deque

# ------ Global Parameters ------ #


# ------ Class & Function ------ #

class Node(object):
	def __init__(self):
		self.next = dict()
		self.fail = None
		self.leaf = []
		return


class AC(object):
	def __init__(self):
		self.root = Node()
		return

	def __add__(self, word):
		p = self.root
		for c in word:
			p.next.setdefault(c, Node())
			p = p.next[c]
		p.leaf.append(word)

	def build(self, words):
		# build trie first
		for w in words:
			self.__add__(w)

		# add fail jump
		q = deque()

		# handle root
		for k, v in self.root.next.iteritems():
			self.root.next[k].fail = self.root
			q.append(self.root.next[k])

		# bfs for else node
		while q:
			tmp = q.pop()
			p = tmp.fail
			for k, v in tmp.next.iteritems():
				while p:
					if k in p.next:
						tmp.next[k].fail = p.next[k]
						tmp.next[k].leaf += p.next[k].leaf
						break
					p = p.fail
				if not p:
					tmp.next[k].fail = self.root
				q.append(tmp.next[k])
		return True

	def search_all(self, text):
		p = self.root
		result = []
		pos = 0

		while pos < len(text):
			c = text[pos]
			if p == self.root and c not in p.next:
				pos += 1
				continue

			if c in p.next:
				p = p.next[c]
				if p.leaf:
					result += p.leaf
				pos += 1
			else:
				p = p.fail
		return result

# ------ Main Process ------ #

if __name__ == "__main__":

	words = ['ab', 'abc', 'bc']
	ac = AC()
	ac.build(words)

	print ac.search_all('abcdef')





