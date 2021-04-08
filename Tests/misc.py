import os
import pickle
os.chdir(r"C:\Users\Mathi\Desktop\cards7\Simulator_main\model\nodes")
pref = 0
for node_pack in os.listdir():
    node_list = pickle.load(open(node_pack, "rb"))

    for node in node_list:
        if node.identifier.flop == []:
            pref += 1

print(pref)




