from subtree_trainer.misc import parse_actions


def sim(tree, current_node_ID, community, players, street, denote):


    print("one round in local sim")
    if denote in ["F:", "T:", "R:"]:
        current_node = tree.get_node(current_node_ID[:-2])
    else:
        current_node = tree.get_node(current_node_ID)
    current_player = players.find_hero()
    GC, deck, players = parse_actions(current_node, community, players, street, denote)
    print("current player is: " + str(current_player))
    GC.selected_nodes.append((current_node, current_player.win_odds, current_player))


    while not GC.game_ended:
        tree.expand_tree(current_player, players, current_node, GC)
        current_player.determine_odds(players, GC)
        current_node = GC.do_action(current_node, current_player, players, is_local_sim=True)
        current_node = tree.get_node(current_node.identifier.name)
        current_player = GC.find_next_player(current_player, players)
        GC.check_if_game_ended(players)
        if GC.check_if_street_ended(players) and not GC.game_ended:
            current_player = GC.update_street(deck, players)
            # Do another check, to avoid "end" error:
            GC.check_if_game_ended(players)

    pot = players.pot_size()
    winner = GC.find_winner(players, deck)
    GC.back_prop(pot, winner, tree)












