
from Services.database_SQLite import DB
from Tree.node import Node
from Tree.Identifier import Identifier
from Tree.data2 import Data




class Tree:
    def __init__(self, new_tree=False, path="model_db", root=None):

        self.db = DB(new_tree, path)

        if new_tree:
            if root is None:
                ID = Identifier()
                ID.create_name(is_root=True)
                self.add_node(ID, data=Data(), is_root=True)
                self.root = root

    def add_node(self, ID, data=None, is_root=False, parent=None):
        new_node = Node(ID, data)


        if is_root:
            ID.create_name()
        else:
            self.db.add_children(parent.identifier.name, new_node.identifier.name, commit=False)

            if parent.children is None:
                parent.children = []
            parent.children.append(new_node)

        self.db.add_node(new_node, commit=False)
        self.db.commit()


    """ Expand tree with new nodes if possible """
    def expand_tree(self, current_player, all_players, current_node, controller):

        if current_node.is_leaf() and current_player.chips > 0:

            all_players.update_remaining()
            pot = all_players.pot_size()
            bet1 = True
            bet2 = True
            call = False
            check = False
            allIn = True
            current_bet = all_players.find_max_bet_player().bet

            # A % pot size bet is:
            # a: Find opponenets bet size.
            # b: Calculate the pot now (pot + opponenets bet x 2)

            # Raise: a + (% * b)
            # So basically, calculate pot after figuring out biggest raise.
            # Multiply pot with %, and add biggest raise.
            if ((pot + current_bet) * 0.4 + current_bet) - current_player.bet > current_player.chips:
                bet1 = False
            if ((pot + current_bet) * 0.8 + current_bet) - current_player.bet > current_player.chips:
                bet2 = False


            # Calls must also be available preflop, since blinds have been posted...
            if current_node.identifier.call_available(controller.new_street, controller.preflop,
                                                      name=current_player.name):
                call = True
                fold = True
            else:
                fold = False
                check = True

            if current_player.chips == 0:
                allIn = False
                call = False
                fold = False
                check = False

            elif current_node.identifier.allIn_occured():
                allIn = False

            actions = [(fold, "f"), (call, "ca"), (check, "ch"),
                       (bet1, "b1"), (bet2, "b2"), (allIn, "AL")]

            for action, string in actions:
                if action:
                    # Copies parent identifier
                    iden = Identifier(current_node.identifier)
                    # Checks if new street has arrived
                    iden.update_new_street(controller.new_street)
                    # Update with new action
                    iden.update_street_list((current_player.name, string))
                    iden.create_name()
                    if string == "f":
                        self.add_node(iden, data=Data(pre_flop=controller.preflop, fold_node=True), parent=current_node)
                    else:
                        self.add_node(iden, data=Data(pre_flop=controller.preflop), parent=current_node)

        controller.new_street = [False, ""]


    def get_node(self, node_ID):
        node = self.db.get_node(node_ID)
        children_ID = self.db.get_children(node_ID)
        node.children = []
        if children_ID is not None:
            for child_ID in children_ID:
                child = self.db.get_node(child_ID)
                node.children.append(child)

        return node







