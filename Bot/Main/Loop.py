# own_queue = queue for tree and odds service
import time
from random import random
import logging
logging.basicConfig(level=logging.DEBUG)

from Bot.Main.Helpers.botGameController import game_controller
from Bot.Misc.wait_loop import waitLoops
from Bot.Readers.ReaderController import readerController
from Bot.Readers.ReaderStack import StackReader
from Poker.Deck import Deck


# TODO: Do local sim when N[Split] < threshold


def loop(clicker, ID, master_queue, odds_q, own_queue):
    stop = False
    clicker.start_game()


    while not stop:
        # dummy while loop we can break out of
        try:
            while True:
                # Init objects
                reader = readerController(ID)
                waitLoop = waitLoops(ID, clicker)
                GC = game_controller(own_queue, ID)
                deck = Deck()

                # Wait for first action
                waitLoop.beforePreFlop()

                # Start game
                reader.game_start_read(waitLoop)
                hero = GC.start_game(deck, reader.position, reader.hand)

                # Process actions in tree
                cur_node = GC.processActions(reader.folded, reader.bets)
                # Hero does action
                hero.determine_odds(GC.players, GC, odds_q, ID, own_queue)
                print("odds are: " + str(hero.win_odds))
                cur_node = GC.do_action_bot(cur_node, hero)
                GC.click_action(cur_node, clicker)

                situation = waitLoop.beforeFlop()
                print(situation)
                while situation == "preflop":
                    reader.intermediate_reads()
                    cur_node = GC.processActions(reader.folded, reader.bets, current_player=hero, current_node=cur_node)

                    hero.determine_odds(GC.players, GC, odds_q, ID, own_queue)
                    print("odds are: " + str(hero.win_odds))
                    cur_node = GC.do_action_bot(cur_node, hero)
                    GC.click_action(cur_node, clicker)

                    situation = waitLoop.beforeFlop()

                if situation == "folded":
                    break

                ############# FLOP ############

                reader.read_community("flop")
                reader.intermediate_reads()

                # Figure out what the other players did first (can either be fold, call or check)
                cur_node = GC.process_unseen_actions_flop(cur_node, reader.folded)

                current_player, cur_node = GC.update_street(deck, GC.players, cur_node, reader.flop)

                if current_player.name != hero.name:
                    cur_node = GC.processActions(reader.folded, reader.bets, current_player=current_player,
                                                 current_node=cur_node)

                hero.determine_odds(GC.players, GC, odds_q, ID, own_queue)
                print("odds are: " + str(hero.win_odds))
                cur_node = GC.do_action_bot(cur_node, hero)
                GC.click_action(cur_node, clicker)

                situation = waitLoop.beforeTurn()

                while situation == "flop":
                    reader.intermediate_reads()
                    cur_node = GC.processActions(reader.folded, reader.bets, current_player=hero, current_node=cur_node)
                    hero.determine_odds(GC.players, GC, odds_q, ID, own_queue)
                    print("odds are: " + str(hero.win_odds))
                    cur_node = GC.do_action_bot(cur_node, hero)
                    GC.click_action(cur_node, clicker)

                    situation = waitLoop.beforeTurn()
                if situation == "folded":
                    break

                ############# TURN ############
                reader.read_community("turn")
                reader.intermediate_reads()

                cur_node = GC.process_unseen_actions_turn(cur_node, reader.folded)
                current_player, cur_node = GC.update_street(deck, GC.players, cur_node, reader.turn)

                if current_player.name != hero.name:
                    cur_node = GC.processActions(reader.folded, reader.bets, current_player=current_player,
                                                 current_node=cur_node)

                hero.determine_odds(GC.players, GC, odds_q, ID, own_queue)
                print("odds are: " + str(hero.win_odds))
                cur_node = GC.do_action_bot(cur_node, hero)
                GC.click_action(cur_node, clicker)

                situation = waitLoop.beforeRiver()
                while situation == "turn":
                    reader.intermediate_reads()
                    cur_node = GC.processActions(reader.folded, reader.bets, current_player=hero, current_node=cur_node)
                    hero.determine_odds(GC.players, GC, odds_q, ID, own_queue)
                    print("odds are: " + str(hero.win_odds))
                    cur_node = GC.do_action_bot(cur_node, hero)
                    GC.click_action(cur_node, clicker)

                    situation = waitLoop.beforeRiver()
                if situation == "folded":
                    break


                ############# RIVER ############
                reader.read_community("river")
                reader.intermediate_reads()

                cur_node = GC.process_unseen_actions_river(cur_node, reader.folded)
                current_player, cur_node = GC.update_street(deck, GC.players, cur_node, reader.river)


                if current_player.name != hero.name:
                    cur_node = GC.processActions(reader.folded, reader.bets, current_player=current_player,
                                                 current_node=cur_node)

                hero.determine_odds(GC.players, GC, odds_q, ID, own_queue)
                print("odds are: " + str(hero.win_odds))
                cur_node = GC.do_action_bot(cur_node, hero)
                GC.click_action(cur_node, clicker)

                situation = waitLoop.afterRiver()

                while situation == "river":
                    reader.intermediate_reads()
                    cur_node = GC.processActions(reader.folded, reader.bets, current_player=hero, current_node=cur_node)
                    hero.determine_odds(GC.players, GC, odds_q, ID, own_queue)
                    print("odds are: " + str(hero.win_odds))
                    cur_node = GC.do_action_bot(cur_node, hero)
                    GC.click_action(cur_node, clicker)

                    situation = waitLoop.afterRiver()
                if situation == "folded":
                    break

                break

        except Exception as e:
            logging.exception(e)
            time.sleep(30)
            print("Exception happened")
            print(e)


        try:
            msg = master_queue.get(block=False)
            if msg == "stop":
                stop = True

            elif msg == "pause":
                clicker.pause()
                time.sleep(random.randint(100, 250))
                clicker.start_game()


        except:
            stackReader = StackReader(ID)
            stackReader.Read()
            print("Stack size: " + str(stackReader.stack))

            if stackReader.stack > 2.5:
                clicker.pause()
                clicker.start_game()
            stop = False
