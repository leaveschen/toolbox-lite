# -*- coding:utf-8 -*-
# ------ Import ------ #

import os
import sys
from itertools import chain, izip, groupby
import collections

# ------ Global Parameters ------ #


# ------ Class & Function ------ #

class Darts(object):
	def __init__(self):
		return

	def __build_token__(self, words):
		wl = list(chain(*words))
		id2token = {i+1:v for i,v in enumerate(sorted(set(wl), key=wl.index))}
		token2id = dict(izip(id2token.itervalues(), id2token.iterkeys()))
		return id2token, token2id

	def __resize__(self):
		sz = len(self.base)
		self.base += [0] * sz
		self.check += [0] * sz
		return True

	def __handle__(self, encoded, handle_queue):
		# pop current node
		parent, left, right, depth = handle_queue.popleft()
		print '[current handle queue]: ', parent, left, right, depth

		# find siblings, which element is [char, length]
		group = groupby(encoded[left:right], key=lambda x:x[depth])
		siblings = [ [c, sum(1 for item in items)] for c, items in group ]
		print '[siblings]: ', siblings

		# find valid bias
		bias = self.base[parent]
		while True:
			flag = True
			for c, _ in siblings:
				# check & resize
				if bias+c >= len(self.base):
					self.__resize__()

				if self.check[bias+c] != 0:
					bias += 1
					flag = False
					break
			if flag:
				break
		# modify conflict
		print '[current bias]: ', bias
		self.base[parent] = bias

		# set base, check and children node
		left_t = left
		result_queue = list()
		for c, length in siblings:
			# check & resize
			if bias+c >= len(self.base):
				self.__resize__()

			if c != self.END:
				self.base[bias+c] = bias
				self.check[bias+c] = parent
				result_queue.append([bias+c, left_t, left_t+length, depth+1])
				left_t += length
			else:
				self.base[bias+c] = -1
				self.check[bias+c] = parent
				left_t += length
		for q in result_queue[::-1]:
			handle_queue.appendleft(q)
		print '[next handle queue]: ', handle_queue
		return True

	def build(self, words):
		# initial token map
		self.id2token, self.token2id = self.__build_token__(words)
		self.END = len(self.token2id)+1

		# initial base & check array
		self.base = [0] * 4
		self.check = [0] * 4

		# encode words
		encoded = [ [ self.token2id[c] for c in w ] + [self.END] for w in words ]
		print '[encoded]: ', encoded

		# initial root, which start at position 1
		self.base[1] = 2

		# handle queue, which element is [node_index, left, right, depth]
		handle_queue = collections.deque()
		handle_queue.append([1, 0, len(encoded), 0])

		# handle queue
		while handle_queue:
			print
			print '[base]: ', self.base
			print '[check]: ', self.check
			self.__handle__(encoded, handle_queue)
		print '[base]: ', self.base
		print '[check]: ', self.check

		self.size = len(self.base)
		return True

	def has(self, word):
		# encode
		encoded = list()
		for c in word:
			if c not in self.token2id:
				return 'encode error'
			encoded.append(self.token2id[c])
		encoded.append(self.END)

		# traversal
		curr = 1
		for c in encoded:
			bias = self.base[curr]
			print '[check current]: ', curr, bias, c, self.base[bias+c], self.check[bias+c]
			if bias+c >= self.size:
				return 'has not'

			if self.base[bias+c] != 0 and self.check[bias+c] == curr:
				curr = bias + c
			elif c != self.END:
				return 'has not'

		# final
		if self.base[curr] != -1:
			return 'prefix'
		return 'has'

# ------ Main Process ------ #

if __name__ == "__main__":

	words = ['c', 'ca', 'ba']
	words = ['c', 'ca', 'cat', 'car', 'bag', 'bot']
	d = Darts()
	d.build(words)
	print d.has('bot')





