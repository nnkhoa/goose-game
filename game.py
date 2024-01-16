from random import randint

START = 0
END = 63
BRIDGE = 6
BRIDGE_DESTINATION = 12
GOOSE = [5, 9, 14, 18, 23, 27]


def auto_roll():
    return [randint(1, 6), randint(1, 6)]


def parse_roll_input(roll_input):
    # auto roll if nothing is entered
    if roll_input.strip() == '':
        return auto_roll()

    roll_int = []
    roll_str = roll_input.split(',')
    for roll in roll_str:
        if not roll.isdigit():
            print('Invalid dice value! Please re-enter the roll')
            break
        else:
            if int(roll) == 0 or int(roll) > 6:
                print('Invalid dice value! Please re-enter the roll')
                break
            roll_int.append(int(roll))
    return roll_int


def prank(last_pos, current_pos, player_list, player_pos):
    while current_pos in player_pos:
        idx = player_pos.index(current_pos)
        player_pos[idx] = last_pos
        print('On {} there is {}, who returns to {}.'.format(current_pos, player_list[idx], player_pos[idx]))

    return player_pos


def goose(player_name, player_pos, roll_value):
    last_pos = player_pos
    while last_pos in GOOSE:
        new_pos = last_pos + roll_value
        print('The goose. {} moves again from {} to {}'.format(player_name, last_pos, new_pos))
        last_pos = new_pos
    # while this might be a warning "referenced before assignment", the loop will always run at least once
    # hence the variable will always be available
    return new_pos


def add_player():
    players = []
    add_new = 'Y'
    while add_new.upper() == 'Y':
        player_name = input('Add a player: ')

        if player_name.strip() in players:
            print('Player {} has already existed'.format(player_name))
            continue
        else:
            players.append(player_name.strip())
        add_new = input('Add another players? (Y/N): ')

        while add_new.strip().upper() != 'N' and add_new.strip().upper() != 'Y':
            print('Invalid answer! Please only use \'Y\' or \'N\'')
            add_new = input('Add another players? (Y/N): ')

    return players

# game loop
def game(player_list):
    player_pos = [0] * len(player_list)
    winner = ''
    # game loop
    while True:
        for player_idx in range(len(player_list)):
            roll_value = []
            while not roll_value:
                roll_input = input('{} rolls: '.format(player_list[player_idx]))
                roll_value = parse_roll_input(roll_input)
            print('{} rolled {},{}'.format(player_list[player_idx], roll_value[0], roll_value[1]))

            last_pos = player_pos[player_idx]
            # get the new position of the dice roll
            new_pos = player_pos[player_idx] + sum(roll_value)

            # Check Bridge
            if new_pos == BRIDGE:
                new_pos = BRIDGE_DESTINATION
                print('{} moves from {} to the Bridge. {} jumps to {}'.format(player_list[player_idx], last_pos,
                                                                              player_list[player_idx], new_pos))
                # check if prank condition is met and update the position of all player aside the current one
                player_pos = prank(last_pos, new_pos, player_list, player_pos)

                # update current player position
                player_pos[player_idx] = BRIDGE_DESTINATION
                continue

            # Check Goose
            if new_pos in GOOSE:
                print('{} moves from {} to {}.'.format(player_list[player_idx], last_pos, new_pos))
                new_pos = goose(player_list[player_idx], new_pos,
                                sum(roll_value))  # handles single/multiple goose jumps
                # check if prank condition is met and update the position of all player aside the current one
                player_pos = prank(last_pos, new_pos, player_list, player_pos)

                # update current player position
                player_pos[player_idx] = new_pos
                continue

            # Check end game condition
            if new_pos == END:
                print('{} moves from {} to {}'.format(player_list[player_idx], last_pos, new_pos))
                winner = player_list[player_idx]
                break
            elif new_pos > END:
                # bounce if roll value exceeds what is needed to read the end tile
                bounce = new_pos - END
                new_pos = END - bounce
                print('{} moves from {} to {}, but bounces back to {}'.format(player_list[player_idx], last_pos, END,
                                                                              new_pos))
                # prank check
                if new_pos != last_pos:  # avoid infinite loop on a specific case that there are 2 players at the same spot and one is bounced back to the exact spot
                    # check if prank condition is met and update the position of all player aside the current one
                    player_pos = prank(last_pos, new_pos, player_list, player_pos)
                # update current player position
                player_pos[player_idx] = new_pos
            else:
                print('{} moves from {} to {}'.format(player_list[player_idx], last_pos, new_pos))
                # check if prank condition is met and update the position of all player aside the current one
                player_pos = prank(last_pos, new_pos, player_list, player_pos)
                # update current player position
                player_pos[player_idx] = new_pos

        if winner in player_list:
            break

    print('Winner: ', winner)


if __name__ == '__main__':
    player_list = add_player()

    print('Here are the current players: ')
    for player in player_list:
        print(player)

    print('Game Start!')
    game(player_list)
