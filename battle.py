# Collin Brooks
# 5/18/23
# Fighter & Enemy Fight Simulation

from dataclasses import dataclass, field
from typing import List
import pygame, random

class BattleWonException(Exception):
    """
    An exception to signify the battle has ended in a victory.
    """
    pass

class BattleLossException(Exception):
    """
    An exception to signify the battle has ended in a loss.
    """
    pass

class UnknownMoveException(Exception):
    """
    An exception to signify the move is not in move list.
    """
    pass

class InvalidMoveException(Exception):
    """
    Exception for invalid moves (e.g. using the same attack twice in a row)
    """
    pass

@dataclass
class Fighter:
    name: str
    hp: int
    move_list: dict
    last_move: str = ""

@dataclass
class Enemy:
    name: str
    hp: int
    move_list: dict
    move_list_items: list = field(init=False)
    last_move: int = -1 # Ensures that the enemy will start with the first move at '0' due to index adding 1

    def __post_init__(self):
        self.move_list_items = list(self.move_list)

@dataclass
class Move:
    name: str
    value: int # Negative indicates a healing move (not yet implemented)

@dataclass
class PassiveEffect:
    pass

def delay_print(text):
        print(text)
        pygame.time.delay(delay)

class FighterBattleSimulator:
    def __init__(self, fighter: Fighter, enemy: Enemy, move: Move = ("",0), upgrade: int = 0):
        self.fighter = fighter
        self.fighter.last_move = ""
        self.enemy = enemy
        self.move = move
        self.upgrade = upgrade
        self.round = 0

    def verify_move(self, attack: str) -> None: # Verifies the move is known and not repeated
        if attack not in self.fighter.move_list.keys():
            raise UnknownMoveException
        elif attack == self.fighter.last_move:
            raise InvalidMoveException

    def advance_round(self, attack: str) -> None: # Will only advance the round after verifying the move
        try:
            self.verify_move(attack)
            self.advance(attack)
            self.battle_info()
        except InvalidMoveException:
            print(f'Invalid move: {attack.title()}. You cannot use the same move twice in a row.\n')
        except UnknownMoveException:
            print(f'Invalid move: {attack.title()}. This attack is not in the move list.\n')
        except BattleWonException:
            self.battle_info()
            if self.upgrade > 0:
                print("Congratulations! All your abilities have been upgraded by 2!")
                for move in self.fighter.move_list.keys():
                    if self.fighter.move_list[move] >= 0:
                        self.fighter.move_list[move] += 2
                    else:
                        self.fighter.move_list[move] -= 2
            elif self.move.value > 0:
                self.fighter.move_list[self.move.name] = self.move.value
                print(f'Congratulations! You have gained a new ability as a reward: {self.move.name.title()} ({self.move.value} damage)')
            elif self.move.value < 0:
                self.fighter.move_list[self.move.name] = self.move.value
                print(f'Congratulations! You have gained a new ability as a reward: {self.move.name.title()} ({self.move.value*-1} heal)')
        except BattleLossException:
            self.battle_info()
            pygame.time.delay(delay*3)
            print("Sorry adventurer, but you have perished. You're journey ends here....")
            pygame.time.delay(delay*2)
            print("...")
            pygame.time.delay(delay*3)
            print("...")
            pygame.time.delay(delay*4)
            print("...")
            pygame.time.delay(delay*5)
            quit()

    def advance(self, attack: str) -> None: # This method calculates the damage and completes the round
        self.round+=1 # Advance the round counter each round
        damage = self.fighter.move_list[attack]
        self.fighter.last_move = attack
        if damage >= 0:
            self.enemy.hp -= damage # Damage is applied to the enemy first
        else:
            self.fighter.hp -= damage
        if self.enemy.hp <= 0:
            self.enemy.hp = 0
            raise BattleWonException
        
        # Initiate the enemy's next move based on the last one and calulate its damage
        index = random.randrange(0,len(self.enemy.move_list)) # This will go back to the beginning when it reaches the final one
        enemy_attack = list(self.enemy.move_list)[index]
        damage = self.enemy.move_list[enemy_attack]
        self.enemy.last_move = index
        self.fighter.hp -= damage # Damage is applied to the fighter after knowing the enemy is not dead
        if self.fighter.hp <= 0:
            self.fighter.hp = 0
            raise BattleLossException

    def battle_info(self) -> None:
        print(f'Round {self.round}')
        pygame.time.delay(delay*2)
        if self.fighter.move_list[self.fighter.last_move] >= 0:
            print(f'Last Fighter Attack: {self.fighter.last_move.title()} ({self.fighter.move_list[self.fighter.last_move]} damage)')
        else:
            print(f'Last Fighter Attack: {self.fighter.last_move.title()} ({self.fighter.move_list[self.fighter.last_move]*-1} heal)')
        pygame.time.delay(delay*2)
        if self.enemy.hp > 0:
            print(f'Last Enemy Attack: {list(self.enemy.move_list)[self.enemy.last_move]} ({self.enemy.move_list[list(self.enemy.move_list)[self.enemy.last_move]]} damage)')
        else:
            print(f'Last Enemy Attack: N/A')
        pygame.time.delay(delay*2)
        print(f'HP: Fighter {self.fighter.hp} Enemy {self.enemy.hp}')
    
    def run_battle(self) -> None:
        sim = self
        pygame.time.delay(delay)
        print("")
        delay_print(f'The battle is {sim.fighter.name} against {sim.enemy.name}.')
        delay_print(f'The Fighter has {sim.fighter.hp} health.')
        delay_print(f'The Enemy has {sim.enemy.hp} health.')
        delay_print("Type \"help\" for a list of all available commands.\n")
        user_input = input("  :").lower()
        print("")
        while user_input != "quit" and sim.enemy.hp > 0:
            if user_input == "moves" or user_input == "move":
                for move in sim.fighter.move_list.keys():
                    if sim.fighter.move_list[move] >= 0:
                        delay_print(f'{move.title()} ({sim.fighter.move_list[move]} damage)')
                    else:
                        delay_print(f'{move.title()} ({sim.fighter.move_list[move]*-1} heal)')
            elif user_input == "enemymoves" or user_input == "enemymove":
                for move in sim.enemy.move_list.keys():
                    delay_print(f'{move.title()} ({sim.enemy.move_list[move]} damage)')
            elif user_input == "help":
                print("help -> Shows this menu")
                print("moves -> Shows your available moves to use in battle")
                print("quit -> Quits the game (progress not saved)")
                print("enemymoves -> Shows the enemy's available moves to use in battle")
            else:
                sim.advance_round(user_input)
            if sim.enemy.hp > 0:
                print("")
                user_input = input("  :").lower()
                print("")
        if user_input == "quit":
            exit()
        

delay = 500
collin = Fighter(name = "Collin", hp = 30, move_list = {"punch":2, "kick":4}) # All moves should be written in lowercase
harry = Enemy(name = "Harry", hp = 10, move_list = {"Punch":1, "Kick":2, "Knife Stab":4})
steven = Enemy(name = "Steven", hp = 5, move_list = {"Punch":1, "Kick":2})
john = Enemy(name = "John", hp = 20, move_list = {"Slap":2, "Knife Stab":7})
boss = Enemy(name = "John", hp = 50, move_list = {"Slap":10, "Throw":15})

fight1 = FighterBattleSimulator(collin, harry, Move("rest", -4)) # Pass in your fighter and enemy here
fight1.run_battle()

fight2 = FighterBattleSimulator(collin, steven, Move("wrestle", 7))
fight2.run_battle()

fight3 = FighterBattleSimulator(collin, john, upgrade = True)
fight3.run_battle()

fight4 = FighterBattleSimulator(collin, boss)
fight4.run_battle()

