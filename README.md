dictfs
======

Wraps the file system in a dictionary-like access structure.

```python
from dictfs import curdir

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
```
