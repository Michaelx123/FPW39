def draw_board(itog):
    for i in range(3):
        str_ = ''
        for j in range(3):
            if not itog or board_m[j + i * 3] in "+o":
                str_ = str_ + board_m[j + i * 3] + "|"
            else:
                str_ = str_ + " |"
        print("", str_, sep="|")

def take_input(player_token):
    while True:
        player_answer = input("Куда поставим '" + player_token+"' ? ")
        if player_answer not in "123456789" or len(player_answer) != 1:
            print("Некорректный ввод. Введите число от 1 до 9.")
            continue
        if board_m[int(player_answer)-1] in "+o":
            print(f"Клетка № {player_answer} занята!")
            continue
        return int(player_answer)
        break


def check_win():
    win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    for each in win_coord:
        if board_m[each[0]] == board_m[each[1]] == board_m[each[2]]:
            print(board_m[each[0]], "выиграл! ИГРА ОКОНЧЕНА. Итоговое поле:")
            return True
    return False

board_m = '123456789'
counter = 0
who_win = 0
print("ИГРА НАЧАЛАСЬ!")
print("Используйте цифры от 1 до 9 для установки крестика или нолика в соотвествующую клетку.")
while True:
    draw_board(False)
    if counter % 2 == 0:
        player_token="+"
        answer = take_input(player_token)
    else:
        player_token="o"
        answer = take_input(player_token)
    board_m = board_m[:answer - 1] + player_token + board_m[answer:]
    counter += 1
    if counter < 4:
        continue
    if check_win():
        draw_board(True)
        break
    if counter == 9:
        print("Ничья! ИГРА ОКОНЧЕНА. Итоговое поле:")
        draw_board(True)
        break

