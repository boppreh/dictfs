from os import path, listdir

class DictFs(object):
	def __init__(self, start_dir, type=''):
		self.dir = path.abspath(start_dir)
		self.type = type

	def subpath(self, index):
		if isinstance(index, str):
			return path.join(self.dir, index)
		elif isinstance(index, int):
			return self.keys()[index]
		else:
			raise KeyError('Invalid index type {} ({}).'.format(type(index), index))

	def keys(self, show_hidden=True):
		keys = listdir(self.dir)
		if not show_hidden:
			keys = [path for path in keys if not path.startswith('.')]
		return sorted(keys)

	def __getitem__(self, index):
		new_path = self.subpath(index)

		if path.isdir(new_path):
			return DictFs(new_path)
		elif path.isfile(new_path):
			with open(new_path, 'r' + self.type) as f:
				return f.read()

	def __iter__(self):
		return iter(self.keys())

	def __repr__(self):
		return self.dir

curdir = DictFs('.')

if __name__ == '__main__':
	for i in curdir:
		print(i)