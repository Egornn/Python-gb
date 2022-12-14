import random as r
from PIL import Image, ImageDraw
import os as os


# 1/Напишите программу, удаляющую из текста все слова, содержащие ""абв"".
def remove_str(input_file, output_file, removed_str):
    file = open(input_file, encoding='utf-8', mode='r')
    output = ' '.join([x for x in file.read().split() if not removed_str in x])
    file.close()
    file = open(output_file, encoding='utf-8', mode='w')
    file.write(output)
    file.close()


input_id = '1_in.txt'
output_id = '1_out.txt'
remove_strng = 'абв'
remove_str(input_id, output_id, remove_strng)

# 2. Создайте программу для игры с конфетами человек против человека.

# Условие задачи: На столе лежит 2021 конфета. Играют два игрока делая ход друг после друга. Первый ход определяется жеребьёвкой.
# За один ход можно забрать не более чем 28 конфет. Все конфеты оппонента достаются сделавшему последний ход.
# Сколько конфет нужно взять первому игроку, чтобы забрать все конфеты у своего конкурента?

candy = 51
max_candies = 28
print(f'To win the first one takes {candy % (max_candies + 1)} candies. ')


def pvp_candies(start, max_step):
    player_turn = r.randint(1, 3)
    turn = -1
    while start > 0:
        player_turn = player_turn % 2 + 1
        while not 0 < turn < max_step + 1:
            turn = int(input(
                f'{start} candies left. Player {player_turn}, how many candies do ' \
                f'you want to take? You cannot take more than {min(max_candies, start)} '))
        start -= turn
        turn = -1
    print(f"Congratulation to player {player_turn}! You've won!")


# a) Добавьте игру против бота

# b) Подумайте как наделить бота ""интеллектом""

def pve_candies(start, max_step):
    player_turn = r.randint(1, 3)
    turn = -1
    while start > 0:
        player_turn = player_turn % 2 + 1
        if player_turn == 1:
            while not 0 < turn < max_step + 1:
                turn = int(input(
                    f'{start} candies left. Human player, how many candies do ' \
                    f'you want to take? You cannot take more than {min(max_candies, start)} '))
        else:
            if start % (max_step + 1) == 0:
                turn = r.randint(1, max_step + 1)
            else:
                turn = start % (max_step + 1)
            print(f'There was {start} candies and the computer took {turn}.There is {start - turn} left.')
        start -= turn
        turn = -1
    if player_turn == 1:
        print("Congratulation to human player! You've won!")
    else:
        print("My condolences to human player! You've lost!")


def choose_mode(mode, candies, max_at_once):
    if mode == "pvp":
        pvp_candies(candies, max_at_once)
    elif mode == 'pve':
        pve_candies(candies, max_at_once)
    else:
        print('There is no such mode.')


# choose_mode(input('Use "pvp" or "pve" for 2 players and against computer mode respectively '), candy, max_candies)

# 3.Создайте программу для игры в ""Крестики-нолики"".
board_path = 'tic-tac-toe.jpg'
size = 1500


def initial_setup(size):
    try:
        os.remove(board_path)
    except:
        pass
    im = Image.new('RGB', (size, size), (256, 256, 256))
    draw = ImageDraw.Draw(im)
    for i in range(size // 3, size, size // 3):
        draw.line((i, 0, i, size), fill=(0, 0, 0), width=10)
        draw.line((0, i, size, i), fill=(0, 0, 0), width=10)
    im.save(board_path, quality=100)
    return [[' ' for x in range(3)] for y in range(3)]


def get_input_coordinates(board, symbol):
    is_done = False
    coord = [-1, -1]
    while (not (0 <= coord[0] <= 2)) or (not (0 <= coord[1] <= 2)) or not is_done:
        coordinates = input(f'Enter the (row,column) to draw a {symbol} from 1 to 3) ')
        try:
            coord_given = list(map(int, coordinates.split(',')))
            coord = [coord_given[i] - 1 for i in range(len(coord_given))]
        except:
            pass
        if not len(coord) == 2:
            print('Write coordinates in a form "x,y"')
            coord = [-1, -1]

        # coord[0] = int(input(f'Enter the row to draw a {symbol} from 1 to 3): ')) - 1
        # coord[1] = int(input(f'Enter the column to draw a {symbol} from 1 to 3): ')) - 1
        try:
            correct = board[coord[0]][coord[1]] == " "
            if correct:
                is_done = True
            else:
                print('This space is already taken')
        except:
            pass
        print('')
    return coord


def coordinates_of_x(horizontal, vertical, left_or_right):
    center_x = vertical * size // 3 + size // 6
    center_y = horizontal * size // 3 + size // 6
    offset = size // 10
    if left_or_right == 'L':
        return (center_x - offset, center_y - offset, center_x + offset, center_y + offset)
    elif left_or_right == "R":
        return (center_x + offset, center_y - offset, center_x - offset, center_y + offset)


def coordinates_of_o(horizontal, vertical):
    center_x = vertical * size // 3 + size // 6
    center_y = horizontal * size // 3 + size // 6
    offset = size // 8
    return (center_x - offset, center_y - offset, center_x + offset, center_y + offset)


def draw_x_o(horizontal, vertical, x_or_o):
    im = Image.open(board_path)
    draw = ImageDraw.Draw(im)
    if x_or_o == 'X':
        draw.line(coordinates_of_x(horizontal, vertical, "L"), fill=(255, 0, 0), width=size // 30)
        draw.line(coordinates_of_x(horizontal, vertical, "R"), fill=(255, 0, 0), width=size // 30)
    elif x_or_o == 'O':
        draw.ellipse(coordinates_of_o(horizontal, vertical), fill=(255, 255, 255), outline=(0, 256, 0),
                     width=size // 30)
    im.save(board_path, quality=100)


def check_if_win(b, symbol):
    win = [symbol for x in range(3)]
    lines = [b[0], b[1], b[2], [b[i][0] for i in range(3)], [b[i][1] for i in range(3)], [b[i][2] for i in range(3)],
             [b[i][i] for i in range(3)], [b[i][-i - 1] for i in range(3)]]
    return win in lines


def play_cycle(board):
    turn = 0
    current_player = 1
    corresponding_symbols = {1: 'X', 2: 'O'}
    while not check_if_win(board, corresponding_symbols[current_player % 2 + 1]):
        if turn == 9:
            current_player = -1
            break
        coordinate = get_input_coordinates(board, corresponding_symbols[current_player])
        board[coordinate[0]][coordinate[1]] = corresponding_symbols[current_player]
        draw_x_o(coordinate[0], coordinate[1], corresponding_symbols[current_player])
        current_player = current_player % 2 + 1
        turn += 1
    if current_player == 1:
        print('Congratulations to O player')
    elif current_player == 2:
        print('Congratulations to the X player')
    elif current_player == -1:
        print("That's a tie")


current_board = initial_setup(size)


# play_cycle(current_board)


# 4.Реализуйте RLE алгоритм: реализуйте модуль сжатия и восстановления данных.

def encode(string):
    if string == '': return ''
    encoded = ''
    i = 0
    while i < len(string) - 1:
        counter = 1
        symbol = string[i]
        j = i
        while j < len(string) - 1:
            if string[j] == string[j + 1]:
                counter += 1
                j += 1
            else:
                break
        encoded += str(counter) + symbol
        i = j + 1
    return encoded


def decode(enc_string):
    if enc_string == '': return ''
    decoded = ''
    i = 0
    while i < len(enc_string) - 1:
        number = ""
        j = i
        while j < len(enc_string):
            if enc_string[j].isdigit():
                number += enc_string[j]
            else:
                symbol = enc_string[j]
                decoded += symbol * int(number)
                break
            j += 1
        i = j + 1
    return decoded


cryptic = encode('jjeerff')
print(cryptic)
print(decode(cryptic))
