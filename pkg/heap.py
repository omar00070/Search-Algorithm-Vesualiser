


class MinHeap(object):
	def __init__(self, items):
		self.items = items

	def get_left_child_index(self, parent_index):
		return 2 * parent_index + 1

	def get_right_child_index(self, parent_index):
		return 2 * parent_index + 2

	def get_parent_index(self, child_index):
		return (child_index - 1)//2

	def has_left_child(self, index):
		return self.get_left_child_index(index) < len(self.items)

	def has_right_child(self, index):
		return self.get_right_child_index(index) < len(self.items)

	def has_parent(self, index):
		return self.get_parent_index(index) >= 0

	def left_child(self, index):
		return self.items[self.get_left_child_index(index)][1]

	def right_child(self, index):
		return self.items[self.get_right_child_index(index)][1]

	def parent(self, index):
		return self.items[self.get_parent_index(index)][1]

	def peek(self):
		if len(self.items) == 0:
			print('no items in the list')
			return
		return self.items[0]

	def poll(self):
		if len(self.items) == 0:
			print('no items in the list')
			return
		item = self.items[0]
		self.items[0] = self.items[len(self.items) - 1]
		self.items.pop(len(self.items) - 1)
		self.heapify_down()
		return item

	def add(self, item):
		self.items.append(item)
		self.heapify_up()

	def heapify_up(self):
		index = len(self.items) - 1
		while self.has_parent(index) and self.items[index][1] < self.parent(index):
			self.swap(self.get_parent_index(index), index)
			index = self.get_parent_index(index)

	def heapify_down(self):
		index = 0
		while self.has_left_child(index):
			min_child_index = self.get_left_child_index(index)
			if self.has_right_child(index) and self.right_child(index) < self.left_child(index):
				min_child_index = self.get_right_child_index(index)
			if self.items[index][1] < self.items[min_child_index][1]:
				break
			else:
				self.swap(index, min_child_index)
			index = min_child_index

	def swap(self, index, another_index):
		swapper = self.items[index]
		self.items[index] = self.items[another_index]
		self.items[another_index] = swapper

	def display(self):
		return self.items


