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


def obtener_numero_aleatorio(escenario):
    #Número aleatorrio entre 1 y 100
    num_aleatorio = random.randint(1, 100)
    limite_inferior = 0

    
    for numero, probabilidad in escenario.items():
        limite_superior = limite_inferior + probabilidad
        # Comprueba si el número aleatorio generado está dentro del rango actual
        if limite_inferior < num_aleatorio <= limite_superior:
            return numero
        # Actualiza el límite inferior para la próxima iteración
        limite_inferior = limite_superior

# Escenarios con sus porcentajes, tomando como referencia la imagen adjuntada en el README
partidas_probabilidades = [
    {0: 26, 1: 51, 2: 23},  # Partida 1
    {0: 36, 1: 36, 2: 28},  # Partida 2
    {0: 32, 1: 37, 2: 30},  # Partida 3
]
    
def get_computer_action1():
    computer_selection = random.randint(0, len(GameAction) - 1)
    computer_action = GameAction(computer_selection)
    print(f"Computer picked {computer_action.name}.")

    return computer_action

def get_computer_action(partida):
    
    if partida == 0 or partida == 1 or partida == 2:

        computer_selection = obtener_numero_aleatorio(partidas_probabilidades[partida])
        computer_action = GameAction(computer_selection)
        print(f"Computer picked {computer_action.name}.")
        
    else:
        
        #Modificar condición a partir de la 3 partida
        computer_selection = random.randint(0, len(GameAction) - 1)
        computer_action = GameAction(computer_selection)
        print(f"Computer picked {computer_action.name}.")

        return computer_action

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


def main():
    
    partida = 0

    while True:
        try:
            player1 = get_user_action()
        except ValueError:
            range_str = f"[0, {len(GameAction) - 1}]"
            print(f"Invalid selection. Pick a choice in range {range_str}!")
            continue

        result_json = 'result.json'
        
        try:
            with open(result_json, 'r') as f:
                game_record = json.load(f)
        except FileNotFoundError:
            game_record = {"record": []}

        player2 = get_computer_action(partida)
        result = assess_game(player1, player2)

        match_info = {"player1": player1, "player2": player2, "result": result}
        
        game_record["record"].append(match_info)

        # Save the results to a file
        with open(result_json, 'w') as f:
            json.dump(game_record, f, indent=4)
            
        partida +=1

        if not play_another_round():
            break


if __name__ == "__main__":
    main()
