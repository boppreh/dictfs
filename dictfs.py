from os import path, listdir, remove
from shutil import rmtree

class DictFs(object):
    def __init__(self, start_dir='.'):
        """
        Creates a new DictFs object starting at the given directory.
        """
        self.path = path.abspath(path.expanduser(start_dir))
        if not path.isdir(self.path):
            raise IOError('start_dir must be a directory, got {}'.format(self.path))

    def _subpath(self, index):
        """
        Returns a subpath from a string or integer index.
        """
        if isinstance(index, str):
            return path.join(self.path, path.expanduser(index))
        elif isinstance(index, int):
            return self.keys()[index]
        else:
            raise KeyError('Invalid index {} ({}).'.format(type(index), index))

    def keys(self, show_hidden=True):
        """
        Returns the name of all elements in this directory.
        If show_hidden is False, names starting with a dot are ommited.
        """
        keys = listdir(self.path)
        if not show_hidden:
            keys = [path for path in keys if not path.startswith('.')]
        return sorted(keys)

    def items(self, show_hidden=True):
        """
        Returns pairs (key, value) for all elements in this directory.
        The value of file elements are their content, so this reads all
        files in the current directory.
        """
        for key in self.keys(show_hidden):
            yield key, self[key]

    def files(self, show_hidden=True):
        """
        Returns the name of all files in this directory.
        """
        return filter(path.isfile, self.keys(show_hidden))

    def dirs(self, show_hidden=True):
        """
        Returns the name of all directories inside this directory.
        """
        return filter(path.isdir, self.keys(show_hidden))

    def index(self, key):
        """
        Return the numeric index of the given element name.
        """
        return self.keys().index(key)

    def __len__(self):
        """
        Return the number of elements in this directory.
        """
        return len(self.keys())

    def __getitem__(self, index):
        """
        Returns all elements matching the given index.
        Index may be an element name, an integer, a list of
        element names or integers, or a slice object.

        Files are returned as their content and directories as
        further instances of DictFs.
        """
        if hasattr(index, '__iter__'):
            return [self[i] for i in index]
        elif isinstance(index, slice):
            if isinstance(index.start, str):
                index.start = self.index(start)
            if isinstance(index.stop, str):
                index.stop = self.index(stop)
            return [self[i] for i in self.keys().__getitem__(index)]

        new_path = self._subpath(index)

        if path.isdir(new_path):
            return DictFs(new_path)
        elif path.isfile(new_path):
            with open(new_path, 'r') as f:
                return f.read()
        else:
            raise KeyError('Path not found: {}'.format(new_path))

    def __setitem__(self, index, value):
        """
        Writes the value to a file given by index.
        If the file doesn't exist it is created.
        """
        new_path = self._subpath(index)
        if isinstance(value, bytes):
            bytes_value = value
        else:
            bytes_value = str(value).encode('utf-8')

        with open(new_path, 'wb') as f:
            f.write(bytes_value)

    def __delitem__(self, index):
        """
        Deletes a file or directory.
        """
        new_path = self._subpath(index)
        if path.isfile(new_path):
            remove(new_path)
        elif path.isdir(new_path):
            rmtree(new_path)
        else:
            raise KeyError('Path not found: {}'.format(new_path))

    def __add__(self, other):
        """
        Performs a simple concatenation of the current path and the given
        value.
        """
        return self.path + other

    def __truediv__(self, other):
        """
        Returns the subpath of the given element, which may not exist.
        """
        return self.path + path.sep + other

    __div__ = __truediv__

    def __iter__(self):
        """
        Iterates through all elements in this directory.
        """
        return iter(self.keys())

    def __contains__(self, index):
        """
        Returns True if index is the name of an element in this directory,
        or if it's a valid integer index.
        """
        return path.exists(self._subpath(index))

    def __repr__(self):
        return 'DictFs' + repr(self.path)

    def __str__(self):
        return str(self.path)

    def __eq__(self, other):
        if isinstance(other, DictFs):
            return self.path == other.path
        return self.path == path.abspath(other.path)

curdir = DictFs('.')

if __name__ == '__main__':
    curdir
    # DictFs'/home/boppreh/git/dictfs'

    for i in curdir:
        print(i)
        # .git
        # .gitignore
        # LICENSE
        # README.md
        # dictfs.py

    curdir.files()
    # ['.gitignore', 'LICENSE', 'README.md', 'dictfs.py']

    curdir['.git']
    # DictFs'/home/boppreh/git/dictfs/.git'

    'LICENSE' in curdir
    # True

    curdir[0]
    # DictFs'/home/boppreh/git/dictfs/.git'

    curdir[0:2]
    # [DictFs'/home/boppreh/git/dictfs/.git',
    #  '# Byte-compiled / optim ...']

    curdir['LICENSE']
    # 'The MIT License (MIT)\n\nCopyright (c) 2014 BoppreH...'

    curdir['LICENSE', 'README.md']
    # ['The MIT License...', 'dictfs\n======\n\nWraps the ...'])

    curdir['test.txt'] = 'Hello!'
    del curdir['test.txt']

    curdir[curdir.files()]
    # ['# Byte-compiled / optimized ...',
    #  'The MIT License (MIT) ...',
    #  'dictfs\n======\n\nWraps ...',
    #  'from os import path, listdir, ...']

    curdir / '.git'
    # '/home/boppreh/git/dictfs/.git'

    curdir['~/']
    # DictFs'/home/boppreh'