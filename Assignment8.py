import time
import random
import argparse

class Die:
    def __init__(self):
        random.seed(0)

    def roll(self):
        return random.randint(1, 6)

class Player:
    def __init__(self, name):
        self.name = name
        self.total_score = 0

    def add_score(self, score):
        self.total_score += score

    def reset_score(self):
        self.total_score = 0

    def roll_or_hold(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

class HumanPlayer(Player):
    def roll_or_hold(self):
        choice = input(f"{self.name}, do you want to roll (r) or hold (h)? ")
        return choice.lower() == 'r'

class ComputerPlayer(Player):
    def roll_or_hold(self):
        return self.total_score + 25 <= 100

class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == "human":
            return HumanPlayer(name)
        elif player_type == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError("Invalid player type")

class PigGame:
    def __init__(self, player1, player2):
        self.die = Die()
        self.players = [player1, player2]
        self.current_player = 0

    def switch_turn(self):
        self.current_player = 1 - self.current_player

    def play_turn(self):
        player = self.players[self.current_player]
        turn_total = 0

        print(f"{player.name}'s turn")
        while True:
            roll = self.die.roll()
            print(f"Rolled: {roll}")

            if roll == 1:
                print(f"{player.name} rolled a 1! No points added.")
                turn_total = 0
                break
            else:
                turn_total += roll
                print(f"Turn total: {turn_total}, Overall score: {player.total_score}")
                if not player.roll_or_hold():
                    break

        player.add_score(turn_total)
        print(f"{player.name} ends turn with {player.total_score} points.\n")
        self.switch_turn()

    def play_game(self):
        while all(player.total_score < 100 for player in self.players):
            self.play_turn()

        winner = max(self.players, key=lambda p: p.total_score)
        print(f"{winner.name} wins with {winner.total_score} points!")

class TimedGameProxy:
    def __init__(self, game):
        self.game = game
        self.start_time = time.time()

    def play_game(self):
        while all(player.total_score < 100 for player in self.game.players):
            if time.time() - self.start_time > 60:
                break
            self.game.play_turn()
        winner = max(self.game.players, key=lambda p: p.total_score)
        print(f"{winner.name} wins with {winner.total_score} points!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--player1", choices=["human", "computer"], default="human")
    parser.add_argument("--player2", choices=["human", "computer"], default="human")
    parser.add_argument("--timed", action="store_true")
    args = parser.parse_args()

    player1 = PlayerFactory.create_player(args.player1, "Player 1")
    player2 = PlayerFactory.create_player(args.player2, "Player 2")
    game = PigGame(player1, player2)

    if args.timed:
        game = TimedGameProxy(game)

    game.play_game()
