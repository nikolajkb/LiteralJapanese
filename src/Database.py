import os
import pickledb
import Constants


class Database:
    db = None

    def __init__(self,name):
        self.db = _make_db(name)

    def write_to_disk(self):
        self.db.dump()

    def add_to_list(self,key,val):
        try:
            self.db.ladd(key,val)
        except KeyError:
            self.db.lcreate(key)
            self.db.ladd(key,val)

    def get(self,key, default=None):
        val = self.db.get(key)
        if not val:
            return default
        return val

    def is_empty(self):
        return len(self.db.getall()) == 0


def _make_db(name):
    file_dir = Constants.PROJECT_DIR
    file_path = os.path.join(file_dir, "..", "data","PickleDB",name)
    return pickledb.load(file_path,False)

