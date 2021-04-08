import mysql.connector as mySql
import os
import pickle
import time


class DB:

    def __init__(self, new_model=False, path="cards"):


        if new_model:
            self.conn = mySql.connect(host="localhost", user="root", password="Wohdf92160")
            self.cursor = self.conn.cursor(buffered=True)
            self.cursor.execute("DROP DATABASE IF EXISTS cards")

            self.cursor.execute("CREATE DATABASE cards")
            self.commit()

            self.cursor.execute("USE cards")

            self.cursor.execute("DROP TABLE IF EXISTS nodes")
            self.cursor.execute("DROP TABLE IF EXISTS child_map")


            self.cursor.execute("CREATE TABLE nodes (nKey MEDIUMTEXT, nData LONGBLOB)")

            self.cursor.execute("CREATE TABLE child_map (cKey MEDIUMTEXT, cData LONGBLOB)")

            self.cursor.execute("CREATE UNIQUE INDEX key_idx_node ON nodes (nKey(350))")
            self.cursor.execute("CREATE UNIQUE INDEX key_idx_child ON child_map (cKey(350))")
            self.commit()
        else:
            self.conn = mySql.connect(host="localhost", user="root", password="Wohdf92160", database = "cards")
            self.cursor = self.conn.cursor(buffered=True)

    def get_node(self, key):
        self.cursor.execute("SELECT * FROM nodes FORCE INDEX (key_idx_node) WHERE nKey = %s", (key,))
        out = self.cursor.fetchone()
        return pickle.loads(out[1])

    def update_node(self, node, commit=True):
        serialized = pickle.dumps(node, protocol=4)
        self.cursor.execute("UPDATE nodes SET nData = %s WHERE nKey = %s", (serialized, node.identifier.name,))

        if commit:
            self.commit()

    def add_node(self, node, commit=True):
        serialized = pickle.dumps(node, protocol=4)
        self.cursor.execute("INSERT INTO nodes (nKey, nData) VALUES (%s,%s)", (node.identifier.name, serialized))

        if commit:
            self.commit()

    def add_children(self, parent_ID, child_ID, commit=True):
        out = self.get_children(parent_ID)


        if out is None:
            child_list = [child_ID]
            serialized = pickle.dumps(child_list, protocol=4)
            self.cursor.execute("INSERT INTO child_map (cKey, cData) VALUES (%s,%s)", (parent_ID, serialized,))

        else:
            child_list = out
            child_list.append(child_ID)
            serialized = pickle.dumps(child_list, protocol=4)
            self.cursor.execute("UPDATE child_map SET cData = %s WHERE cKey = %s", (serialized, parent_ID,))

        if commit:
            self.commit()

    def get_children(self, parent_ID):
        self.cursor.execute("SELECT * FROM child_map WHERE cKey = %s", (parent_ID,))
        out = self.cursor.fetchone()

        if out is None:
            return None
        return pickle.loads(out[1])

    def tree_to_db(self, nodes, root_done):
        idx = 0
        length = len(nodes)
        for node in nodes:
            if node.identifier.name == "root" and not root_done or node.identifier.name != "root":
                node.children = None
                self.add_node(node, commit=False)

                if (idx + 1) % 10000 == 0:
                    print(str(idx / length) + " % done")
                    self.commit()
                idx += 1
            if node.identifier.name == "root":
                root_done = True

        self.commit()
        return root_done

    def CM_to_db(self, CM):
        idx = 0
        length = len(CM.values())
        for parent_ID in CM.keys():

            serialized = pickle.dumps(CM[parent_ID], protocol=4)
            self.cursor.execute("INSERT INTO child_map (cKey, cData) VALUES (%s,%s)", (parent_ID, serialized,))

            if (idx + 1) % 10000 == 0:
                print(str(idx / length) + " % done")
                self.commit()
            idx += 1
        self.commit()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    os.chdir(r"C:\Users\Mathi\Desktop\cards7\Simulator_main\model\nodes")
    db = DB(new_model=True)
    rd = False
    for node_pack in os.listdir():
        node_list = pickle.load(open(node_pack, "rb"))

        rd = db.tree_to_db(node_list, rd)


    CMM = pickle.load(open(r"C:\Users\Mathi\Desktop\cards7\Simulator_main\model\etc\child_map", "rb"))
    db.CM_to_db(CMM)
