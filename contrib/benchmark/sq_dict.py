
import os
import cPickle
import sqlite3

__version__ = '0.5'

MTN = 'DICTIONARY_TABLE' #MTN -> Magic Table Name
sentinel = object()
isfile = os.path.isfile

def sq_dict_open(filename, flag='w', mtn=MTN):
    if flag == 'c':
        flag = 'w'
    return SqLiteDictionary(filename, flag, mtn)

def btopen(filename, flag='w', mtn=MTN):
    if flag == 'c':
        flag = 'w'
    return OrderedSqLiteDictionary(filename, flag, mtn)

def shelve(filename, flag='w', mtn=MTN):
    if flag == 'c':
        flag = 'w'
    return ShelveSqLiteDictionary(filename, flag, mtn)

def ashelve(filename, flag='w', mtn=MTN):
    if flag == 'c':
        flag = 'w'
    return ArbitrarySqLiteDictionary(filename, flag, mtn)

def _explain(db, q, args):
    _row = ['addr', 'opcode', 'p1', 'p2', 'p3', 'p4', 'p5', 'comment']
    rows = list(map(str, i) for i in db.execute("EXPLAIN "+q, args))
    rows.insert(0, row)
    for i, row in enumerate(rows):
        while len(row) != len(_row):
            row.append('')
    cw = [max(map(len, i)) for i in zip(*rows)]
    rows.insert(1, [i*'-' for i in cw])
    fstring = '  '.join('%%%is'%i for i in cw)
    return '\n'.join(fstring%tuple(i) for i in rows)

'''
flag	meaning
----	-------
r		read-only
w		read-write
'''

class SqLiteDictionary(object):
    __slots__ = '_flag', '_db', '_cursor', '_mtn', 'autosync', '_orderby'
    def __init__(self, filename, flag, mtn, autosync=0):
        # check flag
        if flag not in ('r', 'w'):
            raise ValueError(
                "flag argument must be 'r' or 'w'; not %r"%(flag,))
        self._flag = flag

        self._mtn = mtn

        # check whether the file exists
        if filename != ':memory:':
            if self._flag == 'r':
                os.stat(filename)
        elif self._flag == 'r':
            # in-memory database that is to be read-only?
            raise IOError("File not found")

        # open the db and check for the table
        self._db = sqlite3.connect(filename)
        for name, in self._db.execute("SELECT name FROM sqlite_master"):
            if name == self._mtn:
                continue
            break
        else:
            if self._flag == 'w':
                self._create_table()
            else:
                raise ValueError(
                    "Dictionary table %s does not exist within sqlite database"%
                    self._mtn)
        self._cursor = None
        self.autosync = autosync
        self._orderby = ' ORDER BY ROWID '

#------------------------------- internal bits -------------------------------
    def _create_table(self):
        self._db.execute('''
            CREATE TABLE %s (
                ROWKEY BLOB PRIMARY KEY,
                ROWVAL BLOB);'''%self._mtn)

    @staticmethod
    def _check_key(key):
        if type(key) not in (str, buffer):
            raise ValueError(
                "Can only use str instances as keys, not %r"%(type(key),))
        return buffer(key)

    @staticmethod
    def _check_value(value):
        if type(value) not in (str, buffer):
            raise ValueError(
                "Can only use str instances as values, not %r"%(type(value),))
        return buffer(value)

    @staticmethod
    def _ke(key):
        return KeyError("Key %r not found"%(key,))

    @classmethod
    def _ro(cls):
        return TypeError(
            "Read-only instance of %s does not support item assignment"%
            (cls.__name__,))

#----------------------- standard sequence operations ------------------------
    def __len__(self):
        for length, in self._db.execute("SELECT count(1) FROM %s"%self._mtn):
            return length
        # should never get here

    def __iter__(self):
        QUERY = "SELECT ROWKEY FROM %s %s"%(self._mtn, self._orderby)
        for rowkey, in self._db.execute(QUERY):
            yield str(rowkey)

    def __contains__(self, key):
        key = self._check_key(key)
        try:
            self[key]
        except KeyError:
            return 0
        return 1

    def __getitem__(self, key):
        key = self._check_key(key)
        QUERY = "SELECT ROWVAL FROM %s WHERE ROWKEY = ?"%self._mtn
        for rowval, in self._db.execute(QUERY, (key,)):
            return str(rowval)
        raise self._ke(key)

    def __setitem__(self, key, value):
        if self._flag == 'r':
            raise self._ro()
        key = self._check_key(key)
        value = self._check_value(value)
        QUERY = "REPLACE INTO %s (ROWKEY, ROWVAL) VALUES (?, ?)"%self._mtn
        self._db.execute(QUERY, (key, value))
        if self.autosync:
            self.sync()

    def __delitem__(self, key):
        if self._flag == 'r':
            raise self._ro()
        key = self._check_key(key)
        QUERY = "DELETE FROM %s WHERE ROWKEY = ?"%self._mtn
        if self._db.execute(QUERY, (key,)) < 1:
            raise self._ke(key)
        if self.aytosync:
            self.sync()

#---------------------------- dictionary iterface ----------------------------
    has_key = __contains__

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key, default=sentinel):
        try:
            default = self[key]
            del self[key]
        except KeyError:
            if default is sentinel:
                raise
        return default

    def popitem(self, key, default=sentinel):
        value = self.pop(key, default)
        return key, value

    def setdefault(self, key, default):
        value = self.get(key, sentinel)
        if value is sentinel:
            self[key] = value = default
        return default

    # keys
    def keys(self):
        return Keys(self)

    iterkeys = keys

    # values
    def values(self):
        return Values(self)

    itervalues = values

    def _itervalues(self):
        for i,j in self._iteritems():
            yield j

    # items
    def items(self):
        return Items(self)

    iteritems = items

    def _iteritems(self):
        QUERY = "SELECT ROWKEY, ROWVAL FROM %s %s"%(self._mtn, self._orderby)
        for i,j in self._db.execute(QUERY):
            yield str(i), str(j)

    # update
    def update(self, other):
        if hasattr(other, 'iteritems'):
            other = other.iteritems()
        elif hasattr(other, 'items'):
            other = other.items()
        for i,j in other:
            self[i] = j

    # clear
    def clear(self):
        self._db.execute("DELETE FROM %s"%self._mtn)

    def _slowclear(self):
        self._db.execute("DELETE FROM %s WHERE 1"%self._mtn)

#---------------------------- dbm-like interface -----------------------------
    def sync(self):
        self._db.commit()

    def close(self):
        if self._db is not None:
            self.sync()
            self._cursor = None
            self._db.close()
            self._db = None

class OrderedSqLiteDictionary(SqLiteDictionary):
    def __init__(self, filename, flag, mtn, autosync=0):
        SqLiteDictionary.__init__(self, filename, flag, mtn, autosync)
        self._orderby = " ORDER BY ROWKEY "

#---------------------- bsddb.btree-compatilble additions ----------------------
    def _sc(self, c, x):
        if c is None:
            raise KeyError("%s key not found"%x)
        c = tuple(str(i) for i in c)
        self._cursor = c
        return c

    def _step(self, key, cmp, dire):
        key = self._check_key(key)
        o = ''
        if '<' in cmp:
            o = 'DESC'
        c = None
        QUERY = ("SELECT ROWKEY, ROWVAL FROM %s WHERE ROWKEY %s ? %s %s LIMIT 1"
                 %(self._mtn, cmp, self._orderby, o))
        for c in self._db.execute(QUERY, (key,)):
            break
        return self._sc(c, dire)

    def set_location(self, key):
        return self._step(key, '>=', 'Usable')

    def first(self):
        return self._step('', '>=', 'First')

    def next(self):
        if self._cursor is None:
            return self.first()
        return self._step(self._cursor[0], '>', 'Next')

    def last(self):
        for c, in self._db.execute("SELECT MAX(ROWKEY) FROM %s"%self._mtn):
            return self._step(c, '<=', 'Last')
        return self._sc(None, 'Last')

    def previous(self):
        if self._cursor is None:
            return self.last()
        return self._step(self._cursor[0], '<', 'Previous')

class ShelveSqLiteDictionary(SqLiteDictionary):
    # put the heavy lifting for ArbitrarySqLiteDictionary here
    _allowed_keys = (str, buffer)
    @classmethod
    def _check_key(cls, key):
        if type(key) not in cls._allowed_keys:
            raise ValueError(
                "Can only use (%s) instances as keys, not %r"%
                (", ".join(i.__name__ for i in cls._allowed_keys), type(key)))
        if type(key) is str:
            return buffer(key)
        return key

    # dump arbitrary data
    @staticmethod
    def _check_value(value):
        return buffer(cPickle.dumps(value))

    # load the data
    def __getitem__(self, key):
        return cPickle.loads(
            super(ShelveSqLiteDictionary, self).__getitem__(key))

    # fix the iterable keys
    def __iter__(self):
        QUERY = "SELECT ROWKEY FROM %s %s"%(self._mtn, self._orderby)
        for rowkey, in self._db.execute(QUERY):
            if type(rowkey) is buffer:
                yield str(rowkey)
            else:
                yield rowkey

    # fix the iterable values
    def iteritems(self):
        QUERY = "SELECT ROWKEY, ROWVAL FROM %s %s"%(self._mtn, self._orderby)
        for i,j in self._db.execute(QUERY):
            if type(i) is buffer:
                i = str(i)
            yield i, cPickle.loads(str(j))

class ArbitrarySqLiteDictionary(ShelveSqLiteDictionary):
    # only allow immutables as keys
    _allowed_keys = (str, buffer, unicode, int, float, type(None))

class Keys(object):
    # for Python 3.0's view object implementation
    __slots__ = '_parent',
    def __init__(self, parent):
        self._parent = parent

    def __len__(self):
        return len(self._parent)

    def __contains__(self, key):
        return key in self._parent

    def __iter__(self):
        return iter(self._parent)

    # view set operations
    def __and__(self, other):
        if type(other) not in (Keys, Items):
            return set(self) & set(other)
        if len(other) < len(self):
            self, other = other, self
        s = set()
        for i in self:
            if i in other:
                s.add(i)
        return s

    def __or__(self, other):
        s = set(self)
        s.update(other)
        return s

    def __sub__(self, other):
        if type(other) not in (Keys, Items):
            s = set(self)
            return s - set(other)
        s = set()
        for i in self:
            if i not in other:
                s.add(i)
        return s

    def __rsub__(self, other):
        if type(self) not in (Keys, Items):
            s = set(other)
            return s - set(self)
        s = set()
        for i in other:
            if i not in self:
                s.add(i)
        return s

    def __xor__(self, other):
        if (type(self) not in (Keys, Items)) or (type(other) not in (Keys, Items)):
            return set(self) ^ set(other)
        return (self-other) | (other-self)

class Values(Keys):
    def __contains__(self, value):
        return value in iter(self)
    def __iter__(self):
        return self._parent._itervalues()

class Items(Keys):
    def __contains__(self, kv_pair):
        if type(kv_pair) is not tuple or len(kv_pair) != 2:
            raise ValueError("Need 2-tuple to check item containment")
        return self._parent.get(kv_pair[0], sentinel) == kv_pair[1]
    def __iter__(self):
        return self._parent._iteritems()
