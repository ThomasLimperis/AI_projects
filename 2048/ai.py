from __future__ import absolute_import, division, print_function
import copy, random
from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1

# Tree node. To be used to construct a game tree.
class Node:
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        self.state = (state[0], state[1])

        # to store a list of (direction, node) tuples
        self.children = []
        self.terminal = True
        self.player_type = player_type
        self.move =None

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        #TODO: complete this
        if self.terminal and self.player_type == 1:
            #print(self.move) #This is leaf node
            return True
        elif self.terminal and self.children == 0:
            print("This is an error, MAX_PLAYER is a leaf node")
            return None
        else:
            #not leaf
            return False

# AI agent. Determine the next move.
class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3):
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    # (Hint) Useful functions:
    # self.simulator.current_state, self.simulator.set_state, self.simulator.move

    # TODO: build a game tree from the current node up to the given depth
    def build_tree(self, node=None, depth=0):
        if depth == 0:
            return

        if node.player_type == 0:
            #if (self.simulator.can_move()): not necessary
                for move in MOVES:
                    dcopy = (copy.deepcopy(node.state))
                    self.simulator.set_state(*dcopy)
                    if self.simulator.move(move):
                        c = self.simulator.current_state()
                        child = Node(c, 1)
                        child.move = move
                        node.terminal = False
                        node.children.append((move, child))
                        node.terminal = False
                        self.build_tree(child, depth - 1)
        else:
            space = self.simulator.get_open_tiles()
            #create copy, set state to the copy state, place the tile, get the current state and repeat
            for chance in space:
                dcopy = (copy.deepcopy(node.state))
                self.simulator.set_state(*dcopy)
                self.simulator.tile_matrix[chance[0]][chance[1]] = 2
                c = self.simulator.current_state()
                child = Node(c, 0)
                child.move = -1
                node.terminal = False
                node.children.append((-1, child))
                self.build_tree(child, depth - 1)

    # TODO: expectimax calculation.
    # Return a (best direction, expectimax value) tuple if node is a MAX_PLAYER
    # Return a (None, expectimax value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):
        # TODO: delete this random choice but make sure the return type of the function is the same
          #print("exp:",node.state)
          if (self.simulator.game_over()):
              print("You ended the game and screwed up")
              return None
          if node.is_terminal():
              if (node.player_type == 0):
                  print("ERROR, player is leaf node")
                  return None
              else:
                  return (node.move, node.state[1])

          if node.player_type ==0:
              maxscore = -1
              score = 0
              void = None
              best_d = -1 #non move
              for child in node.children:
                  move = child[0]
                 # print(child)
                  void ,score = self.expectimax(child[1]) #just giving node because i already have .move
                  if (score >= maxscore):
                      maxscore = score
                      best_d= move
              if (best_d != -1):
                  return (best_d,maxscore)
              else:
                  print("Error, best direction invalid")
                  return None
          elif node.player_type == 1: #chance put random 2 tile, get open tiles and chance is 1/tiles available
              v2 = 0
              chance = 1
              if len(node.children) != 0:
                 chance = 1.0 / len(node.children)
              else:
                  chance = 1.0
              #z = 0
              #  return (None, node.state[1])
              for child in node.children:
                  void,v1 = self.expectimax(child[1])
                  v2 = v2 + v1 * chance
              return (void,v2)
          else:
              print(node.state)
              print(node.move)
              print("Error, Node is null")
              return random.randint(0, 3), 0

    # Return decision at the root
    def compute_decision(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax(self.root)
        return direction

    # TODO (optional): implement method for extra credits
    def compute_decision_ec(self):
        return random.randint(0, 3)
