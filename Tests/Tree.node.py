from Services.database_SQLite import DB
from Tree.node import Node
from Tree.Tree import Tree

T = Tree()
a = T.get_node("root")
print(a.find_distribution(0.5))
