board_m = '123456789'
def draw_board(itog):
    for i in range(3):
        a = board_m[0 + i * 3] if board_m[0 + i * 3] in "+o" or not itog else " "
        b = board_m[1 + i * 3] if board_m[1 + i * 3] in "+o" or not itog else " "
        c = board_m[2 + i * 3] if board_m[2 + i * 3] in "+o" or not itog else " "
        print("", a, b, c, "", sep="|")

def take_input(player_token):
    global board_m
    while True:
        player_answer = input("Куда поставим '" + player_token+"' ? ")
        if player_answer in "123456789" and len(player_answer) == 1:
             if board_m[int(player_answer)-1] not in "+o":
                board_m = board_m[:int(player_answer)-1] + player_token + board_m[int(player_answer):]
                break
             else:
                print(f"Клетка № {player_answer} занята!")
        else:
            print("Некорректный ввод. Введите число от 1 до 9.")

def check_win():
    win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    for each in win_coord:
        if board_m[each[0]] == board_m[each[1]] == board_m[each[2]]:
            return board_m[each[0]]
    return False

def main():
    counter = 0
    print("ИГРА НАЧАЛАСЬ!")
    print("Используйте цифры от 1 до 9 для установки крестика или нолика в соотвествующую клетку.")
    while True:
        draw_board(False)
        if counter % 2 == 0:
            take_input("+")
        else:
            take_input("o")
        counter += 1
        if counter > 4:
            who_win = check_win()
            if who_win:
                print(who_win, "выиграл! Итоговое поле:")
                draw_board(True)
                print("ИГРА ОКОНЧЕНА.")
                break
        if counter == 9:
            print("Ничья! Итоговое поле:")
            draw_board(True)
            print("ИГРА ОКОНЧЕНА.")
            break
main()