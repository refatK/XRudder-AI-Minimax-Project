from xruddergame import XRudderGame
from players.humanPlayer import HumanPlayer

def main():
    game_types = ['0', '1', '2', '3']

    # choose game type
    while True:
        game_type = input('''\
Choose Game Type:
1 : Player vs Player
2 : Player vs AI (Player is first)
3 : Player vs AI (AI is first)
>''')
        if game_type in game_types:
            break
        else:
            print('Invalid input, type [1], [2], or [3]')
            continue
    
    while True:
        symbol_p1 = input('Choose Player 1 symbol (must be 1 char or empty for default)\n>')
        if len(symbol_p1) > 1:
            print('Invalid input, must be ONE char')
            continue
        if not symbol_p1:
            symbol_p1 = '■'
        break
    while True:
        symbol_p2 = input('Choose Player 2 symbol (must be 1 char or empty for default)\n>')
        if len(symbol_p2) > 1:
            print('Invalid input, must be ONE char')
            continue
        if not symbol_p2:
            symbol_p2 = '□' if symbol_p1 != '□' else '■'
        break

    if game_type == '1':
        ps = (HumanPlayer(1, symbol_p1), HumanPlayer(2, symbol_p2))
    elif game_type == '2':
        ps = (HumanPlayer(1, symbol_p1), symbol_p2)
    elif game_type == '3':
        ps = (symbol_p1, HumanPlayer(2, symbol_p2))
    else:
        ps = None

    game = XRudderGame(players=ps)
    game.play()


if __name__ == '__main__':
    main()
