import random
import json
from enum import IntEnum


class GameAction(IntEnum):

    Rock = 0
    Paper = 1
    Scissors = 2


class GameResult(IntEnum):
    Victory = 0
    Defeat = 1
    Tie = 2


Victories = {
    GameAction.Rock: GameAction.Paper,
    GameAction.Paper: GameAction.Scissors,
    GameAction.Scissors: GameAction.Rock
}


# Porcentaje de probabilidad de elección para las tres primeras partidas
game_probability = [
    {0: 26, 1: 51, 2: 23},  # Partida 1
    {0: 36, 1: 36, 2: 28},  # Partida 2
    {0: 32, 1: 37, 2: 30},  # Partida 3
]

def assess_game(user_action, computer_action):

    game_result = None

    if user_action == computer_action:
        print(f"User and computer picked {user_action.name}. Draw game!")
        game_result = GameResult.Tie

    # You picked Rock
    elif user_action == GameAction.Rock:
        if computer_action == GameAction.Scissors:
            print("Rock smashes scissors. You won!")
            game_result = GameResult.Victory
        else:
            print("Paper covers rock. You lost!")
            game_result = GameResult.Defeat

    # You picked Paper
    elif user_action == GameAction.Paper:
        if computer_action == GameAction.Rock:
            print("Paper covers rock. You won!")
            game_result = GameResult.Victory
        else:
            print("Scissors cuts paper. You lost!")
            game_result = GameResult.Defeat

    # You picked Scissors
    elif user_action == GameAction.Scissors:
        if computer_action == GameAction.Rock:
            print("Rock smashes scissors. You lost!")
            game_result = GameResult.Defeat
        else:
            print("Scissors cuts paper. You won!")
            game_result = GameResult.Victory

    return game_result


def get_random_number(game_probability):
    #Random number between 1 and 100
    random_number = random.randint(1, 100)
    lower_limit = 0

    for num, probability in game_probability.items():
        upper_limit = lower_limit + probability
        # Check if the generated random number is within the current range
        if lower_limit < random_number <= upper_limit:
            return num
        # Update the lower bound for the next iteration
        lower_limit = upper_limit


def get_computer_action(game):
    
    if game == 0 or game == 1 or game == 2:

        computer_selection = get_random_number(game_probability[game])
        computer_action = GameAction(computer_selection)
        print(f"Computer picked 1 {computer_action.name}.")
        
    else:

        # Path to your JSON file
        json_file_path = 'history.json'

        # Read the JSON data 
        with open(json_file_path, 'r') as file: 
            data = json.load(file)
        
        game_history = data['history']
        for game in game_history:
            player = game['player']
            #computer = game['computer']
            result = game['result']
        if result == 0:
            computer_action = GameAction(random.randint(0, 1))
            print(f"Computer picked {computer_action.name}.")
        else:
            if player == 0:
                computer_action = GameAction(1)
            elif player == 1:
                computer_action = GameAction(2)
            elif player == 2:
                computer_action = GameAction(0)
            print(f"Computer picked {computer_action.name}.")

    return computer_action


def get_user_action():
    # Scalable to more options (beyond rock, paper and scissors...)
    game_choices = [f"{game_action.name}[{game_action.value}]" for game_action in GameAction]
    game_choices_str = ", ".join(game_choices)
    user_selection = int(input(f"\nPick a choice ({game_choices_str}): "))
    user_action = GameAction(user_selection)

    return user_action


def play_another_round():
    another_round = input("\nAnother round? (y/n) : ")
    while (another_round != "y") and (another_round != "n"):
        another_round = input("\nInvalid selection. Please insert yes (y) or no (n) or press CTRL+C to exit : ")
    return another_round.lower() == 'y'

def update_history(game, player, computer, result):
    result_json = 'history.json'
    
    try:
        with open(result_json, 'r') as f:
            game_history = json.load(f)
    except FileNotFoundError:
        game_history = {"history": []}
        
    match_info = {"game_number":game, "player": player, "computer": computer, "result": result}
    
    game_history["history"].append(match_info)

    # Save the results to a file
    with open(result_json, 'w') as f:
        json.dump(game_history, f, indent=4)


def main():
    
    game = 0

    while True:
        try:
            player = get_user_action()
        except ValueError:
            range_str = f"[0, {len(GameAction) - 1}]"
            print(f"Invalid selection. Pick a choice in range {range_str}!")
            continue

        computer = get_computer_action(game)
        result = assess_game(player, computer)

        update_history(game, player, computer, result)
            
        game +=1

        if not play_another_round():
            break


if __name__ == "__main__":
    main()
