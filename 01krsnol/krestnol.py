board_m = '123456789'
def draw_board():
    print("-------------")
    for i in range(3):
        print("|", board_m[0+i*3], "|", board_m[1+i*3], "|", board_m[2+i*3], "|")
        print("-------------")

def take_input(player_token):
    global board_m
    while True:
        player_answer = input("Куда поставим " + player_token+"? ")
        if player_answer in "123456789" and len(player_answer) == 1:
             if board_m[int(player_answer)-1] not in "OX":
                board_m = board_m[:int(player_answer)-1] + player_token + board_m[int(player_answer):]
                break
             else:
                print(f"Клетка №{player_answer} занята!")
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
    win = False
    while not win:
        draw_board()
        if counter % 2 == 0:
            take_input("X")
        else:
            take_input("O")
        counter += 1
        if counter > 4:
            tmp = check_win()
            if tmp:
                print(tmp, "выиграл!")
                win = True
                break
        if counter == 9:
            print("Ничья!")
            break
main()