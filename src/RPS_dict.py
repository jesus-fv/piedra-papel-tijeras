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


def get_player_history():
    
    player_history = []
    
    # Path to your JSON file
    json_file_path = 'history.json'

    # Read the JSON data 
    try:
        with open(json_file_path, 'r') as file: 
            data = json.load(file)
            
            game_history = data['history']
    
        for game in game_history:
            player_history.append(game['player'])
            
    except FileNotFoundError:
        return []
    
        
    return player_history
    
    
def calculate_probabilities():
    
    probabilities = {0: 0, 1: 0, 2: 0}
    
    player_history = get_player_history()
        
    total_elections = len(player_history)
        
    for player_action in probabilities:
        frequency = player_history.count(player_action)
        probabilities[player_action] = frequency / total_elections
    
    return probabilities


def get_computer_action(game):
    
    if len(get_player_history()) <= 2:

        computer_selection = random.randint(0, len(GameAction) - 1)
        computer_action = GameAction(computer_selection)
        print(f"Computer picked 1 {computer_action.name}.")
        
    else:

        probabilities = calculate_probabilities()
        player_action_frequency = max(probabilities, key=probabilities.get)
        
        opciones = {0: 1, 1: 2, 2: 0}
        computer_action = GameAction(opciones[player_action_frequency])
        
        # Introducimos cierta aleatoriedad para evitar patrones demasiado predecibles
        if random.random() < 0.1:
            # 10% de probabilidad de elegir una acción aleatoria
            computer_action = random.randint(0, len(GameAction) - 1)
            
        print(f"Computer picked 1 {computer_action.name}.")

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

    # Guardar los resultados en el archivo
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
