import random
import json
from enum import IntEnum
import os


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
    
    '''
    Devuelve el historial de partidas del player con su elección
    
    Returns
    -------
    list[str]
    '''
    
    player_history = []
    
    json_file_path = os.path.abspath('data/history.json')

    try:
        with open(json_file_path, 'r') as file: 
            data = json.load(file)
            
            game_history = data['history']
    
        for game in game_history:
            player_history.append(game['player'])
            
    except FileNotFoundError:
        pass
    
        
    return player_history
    

def calculate_frequencies():
    
    '''
    Calcula la frecuencia con la que aparecen en el historial de partidas cada elección
    
    Returns
    -------
    dict{str:int}
    '''
    
    #Diccionario con la frecuencia con la que aparece cada elección (en un princio 0)
    frequencies = {GameAction.Rock.name: 0, GameAction.Paper.name: 0, GameAction.Scissors.name: 0}
    
    player_history = get_player_history()
        
    total_elections = len(player_history)
        
    for player_action in frequencies:
        #Contar las veces en las que aparecen cada elección en el historial de resultados del player
        elections_count = player_history.count(player_action)
        #Calcular la frecuencia de cada elección
        frequencies[player_action] = elections_count / total_elections
    
    return frequencies


def get_computer_action():
    
    '''
    Devuelve la elección de computer
        
    Returns
    -------
    Objeto
    '''
    
    #Devolver elección aleatoria, en el caso de que el json tenga menos de 3 partidas guardadas
    if len(get_player_history()) <= 2:
        
        computer_selection = random.randint(0, len(GameAction) - 1)
        computer_action = GameAction(computer_selection)
        
    else:

        frequencies = calculate_frequencies()
        
        #Recuperar la elección que aparece con mayor frecuencia en el historial de partidas
        player_action_frequency = max(frequencies, key=frequencies.get)
        
        #Obtener la opción que gana a la elección con más frecuencia
        computer_action = Victories.get(GameAction[player_action_frequency].value)
        
        #Introducir cierta aleatoriedad para evitar patrones demasiado predecibles
        if random.random() < 0.1:
            computer_selection = random.randint(0, len(GameAction) - 1)
            computer_action = GameAction(computer_selection)
    
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

def update_history(player, computer, result):
    
    """
    Actualiza el historial de partidas

    Parameters
    ----------
    param1 : str
        Elección del player
    param2 : str
        Elección de computer
    param3 : str
        Resultado de la partida
    """
    
    result_json = os.path.abspath('data/history.json')
    
    try:
        with open(result_json, 'r') as f:
            game_history = json.load(f)
    except FileNotFoundError:
        game_history = {"history": []}
        
    match_info = {"player": player, "computer": computer, "result": result}
    
    game_history["history"].append(match_info)

    with open(result_json, 'w') as f:
        json.dump(game_history, f, indent=4)


def main():

    while True:
        try:
            player = get_user_action()
        except ValueError:
            range_str = f"[0, {len(GameAction) - 1}]"
            print(f"Invalid selection. Pick a choice in range {range_str}!")
            continue
        
        computer = get_computer_action()
        result = assess_game(player, computer)

        update_history(player.name, computer.name, result.name)

        if not play_another_round():
            break


if __name__ == "__main__":
    main()
