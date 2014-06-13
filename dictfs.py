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

	def files(self, show_hidden=True):
		return filter(path.isfile, self.keys(show_hidden))

	def dirs(self, show_hidden=True):
		return filter(path.isdir, self.keys(show_hidden))

	def __getitem__(self, index):
		if hasattr(index, '__iter__'):
			return [self[i] for i in index]

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
		return repr(self.dir)

	def __str__(self):
		return str(self.dir)

curdir = DictFs('.')

if __name__ == '__main__':
	print(DictFs('~'))