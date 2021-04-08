import sqlite3
import os
import pickle
import time
from pathlib import Path


class DB:

    def __init__(self, new_model=False, path="model_db"):

        os.chdir(r"C:\Users\Mathi\Desktop\cards7\Simulator_main")

        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()

        if new_model:
            self.cursor.execute("DROP TABLE IF EXISTS nodes")
            self.cursor.execute("DROP TABLE IF EXISTS child_map")

            self.cursor.execute("CREATE TABLE nodes (key blob, data blob)")
            self.cursor.execute("CREATE TABLE child_map (key blob, data blob)")

            self.cursor.execute("CREATE INDEX IF NOT EXISTS key_idx_node on nodes (key);")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS key_idx_child on child_map (key);")

    def get_node(self, key):
        out = self.cursor.execute("SELECT * FROM nodes WHERE key = '{0}'".format(key)).fetchone()
        try:
            return pickle.loads(out[1])
        except TypeError as E:
            print("Could not find node: " + str(key) + " " + str(E))
            raise TypeError

    def update_node(self, node, commit=True):
        serialized = pickle.dumps(node, protocol=4)
        self.cursor.execute("UPDATE nodes SET data = ? WHERE key = ?", (memoryview(serialized), node.identifier.name))

        if commit:
            self.commit()

    def add_node(self, node, commit=True):
        serialized = pickle.dumps(node, protocol=4)
        self.cursor.execute("INSERT INTO nodes (key, data) VALUES (?,?)",
                            (node.identifier.name, memoryview(serialized)))
        if commit:
            self.commit()

    def add_children(self, parent_ID, child_ID, commit=True):
        out = self.cursor.execute("SELECT * FROM child_map WHERE key = '{0}'".format(parent_ID)).fetchone()

        if out is None:
            child_list = [child_ID]
            serialized = pickle.dumps(child_list, protocol=4)
            self.cursor.execute("INSERT INTO child_map (key, data) VALUES (?,?)", (parent_ID, memoryview(serialized)))

        else:
            child_list = pickle.loads(out[1])
            child_list.append(child_ID)
            serialized = pickle.dumps(child_list, protocol=4)
            self.cursor.execute("UPDATE child_map SET data = ? WHERE key = ?", (memoryview(serialized),
                                                                                parent_ID))

        if commit:
            self.commit()

    def get_children(self, parent_ID):
        out = self.cursor.execute("SELECT * FROM child_map WHERE key = '{0}'".format(parent_ID)).fetchone()
        if out is None:
            return None
        return pickle.loads(out[1])

    def tree_to_db(self, tree):
        idx = 0
        length = len(tree.nodes.values())
        for node in tree.nodes.values():
            node.children = None
            self.add_node(node, commit=False)

            if (idx + 1) % 10000 == 0:
                print(str(idx / length) + " % done")
                self.commit()
            idx += 1
        self.commit()

    def CM_to_db(self, CM):
        idx = 0
        length = len(CM.values())
        for parent_ID in CM.keys():

            serialized = pickle.dumps(CM[parent_ID], protocol=4)
            self.cursor.execute("INSERT INTO child_map (key, data) VALUES (?,?)", (parent_ID, memoryview(serialized)))

            if (idx + 1) % 10000 == 0:
                print(str(idx / length) + " % done")
                self.commit()
            idx += 1
        self.commit()

    def commit(self):
        self.conn.commit()


if __name__ == "__main__":
    from Tree.Tree import Tree

    db = DB(new_model=False)
    db.get_node("root")
