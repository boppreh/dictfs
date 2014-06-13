from os import path, listdir, remove
from shutil import rmtree

class DictFs(object):
	def __init__(self, start_dir):
		self.dir = path.abspath(path.expanduser(start_dir))

	def subpath(self, index):
		if isinstance(index, str):
			return path.join(self.dir, index)
		elif isinstance(index, int):
			return self.keys()[index]
		else:
			raise KeyError('Invalid index {} ({}).'.format(type(index), index))

	def keys(self, show_hidden=True):
		keys = listdir(self.dir)
		if not show_hidden:
			keys = [path for path in keys if not path.startswith('.')]
		return sorted(keys)

	def items(self, show_hidden=True):
		for key in self.keys(show_hidden):
			yield key, self[key]

	def files(self, show_hidden=True):
		return filter(path.isfile, self.keys(show_hidden))

	def dirs(self, show_hidden=True):
		return filter(path.isdir, self.keys(show_hidden))

	def index(self, key):
		return self.keys().index(key)

	def __len__(self):
		return len(self.keys())

	def __getitem__(self, index):
		if hasattr(index, '__iter__'):
			return [self[i] for i in index]
		elif isinstance(index, slice):
			start = index.start or 0
			stop = index.stop or len(self)
			if isinstance(start, str):
				start = self.index(start)
			elif start < 0:
				start += len(self)
			if isinstance(stop, str):
				stop = self.index(stop)
			elif stop < 0:
				stop += len(self)
			step = index.step or 1
			return [self[i] for i in range(start, stop, step)]

		new_path = self.subpath(index)

		if path.isdir(new_path):
			return DictFs(new_path)
		elif path.isfile(new_path):
			with open(new_path, 'r') as f:
				return f.read()
		else:
			raise KeyError('Path not found: {}'.format(new_path))

	def __setitem__(self, index, value):
		new_path = self.subpath(index)
		if isinstance(value, bytes):
			bytes_value = value
		else:
			bytes_value = str(value).encode('utf-8')

		with open(new_path, 'wb') as f:
			f.write(bytes_value)

	def __delitem__(self, index):
		new_path = self.subpath(index)
		if path.isfile(new_path):
			remove(new_path)
		elif path.isdir(new_path):
			rmtree(new_path)
		else:
			raise KeyError('Path not found: {}'.format(new_path))

	def __add__(self, other):
		return self.dir + path.sep + other

	def __iter__(self):
		return iter(self.keys())

	def __repr__(self):
		return 'DictFs' + repr(self.dir)

	def __str__(self):
		return str(self.dir)

curdir = DictFs('.')

if __name__ == '__main__':
	print(curdir.keys())
	print(curdir[:-1])
