import sys, string, time

class Constant_Pool_Class:
    def __init__(self):
        self.pool_list = { }

    def ReadConstantPool(self):
        cfile = "const_pool.byc"
        _cfile = open(cfile, 'r')
        if _cfile.readline() == "CONSTANT POOL\n":
            entries = _cfile.readlines()
            for x in range(len(entries)):
                entry = entries[x].rstrip('\n')
                cword = string.split(entry)
                self.pool_list[x] = cword
            return self.pool_list
        else:
            print 'Improper COnstant Pool File'