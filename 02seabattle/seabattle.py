from random import randint

# создаём классы исключений
class BoardExeption(Exception):
    pass

class BoardOutExeption(BoardExeption):
    def __str__(self):
        return "Вы пытались выстрелить за игровое поле!"

class BoartUsedExeption(BoardExeption):
    def __str__(self):
        return "Вы уже стреляли в эту клетку!"

class BoardWrongShipExeption(BoardExeption):
    def __str__(self):
        return "Не правильно распологаете корабль!"

# класс точка
class Dot:
    def __init__(self, x, y):  # метод
        self.x = x
        self.y = y
    def __eq__(self, other):  # метод отвечающий за сравнеие двух объектов
       return self.x == other.x and self.y == other.y
    def __repr__(self):
        return f"Dot({self.x},{self.y})"

class Ship:

    def __init__(self, bow, l, o):  # конструктор, он задает параметр карабля:
        # координаты, количество жизни(длина), ориентацию
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l
    @property  # Описывает свойства карабля
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y
            if self.o == 0:  # если ноль, то вертикаль
                cur_x += i
            elif self.o == 1:  # если 1, то горизанталь
                cur_y += i
            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots
    def shooten(self, shot): #показывает попали ли мы в карабль или нет
        return shot in self.dots

class Board:

    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid
        self.count = 0 #количество пораженных караблей
        self.field = [["0"] * size for _ in range(size)]
        self.busy = []
        self.ship = []

    def __str__(self):
        res = " " * 4
        for j in range(self.size):
            res += f"{j + 1} | "
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"
        if self.hid:
            res = res.replace("■", "0")  # замена символов в игровом поле
        return res

    def out(self, d): # проверка выходит ли точка за пределы поля или нет
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):
        near = [(-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 0), (0, 1),
                (1, -1), (1, 0), (1, 1) ] # отмечены все тоочки вокруг точки в которой мы находимся

        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipExeption()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)
        self.ship.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out(d):
            raise BoardOutExeption()  # укласс исключения, если стреляли за пределы поля

        if d in self.busy:
            raise BoartUsedExeption()  # класс исключения, если стреляли ужев занятую клетку на игровом поле

        self.busy.append(d)  # если не занято, занять

        for ship in self.ship:
            if ship.shooten(d):
                ship.lives -= 1
                self.field[d.x][d.y] = "x"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Карабль уничтожен!")
                    return False  # большенельзясделать ход
                else:
                    print("Карабль ранен!")
                    return True  # повторите выстрел

        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False
    def begin(self):
        self.busy = []  # обнульть, что бы хранить точки выстрелла

    def defeat(self):
        return self.count == len(self.ship)

class Player:

    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy
    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardExeption as e:
                print(e)

class AI(Player):

    def ask(self):
        d = Dot(randint(0, self.board.size), randint(0, self.board.size))
        print(f"Cледующий ход делает компьтер:{d.x + 1} {d.y + 1}")
        return d

class User(Player):
    def ask(self):
        while True:
            cords = input("Ход пользователя. Введите координаты: ").split()
            if len(cords) != 2:
                print("Введите 2 координаты!")
                continue
            x, y = cords
            if not (x.isdigit()) or not (y.isdigit()):
                print("Введите числа!")
                continue
            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)

class Game:
    def __init__(self, size=6, ship_list=[3, 2, 2, 2, 1, 1, 1, 1], hide_ship=True):
        self.size = size
        self.ship_list = ship_list
        self.hide_ship = hide_ship
        # создаем доски игроков
        pl = self.random_board()
        co = self.random_board()
        co.hid = self.hide_ship #скрывать или нет корабли противника
        # создаем игроков
        self.ai = AI(co, pl)
        self.us = User(pl, co)
    def try_board(self):

        board = Board(size=self.size)  # определяем доску
        attempts = 0
        for l in self.ship_list:
            while True:
                attempts += 1  # попытки расставить корабли
                if attempts > 2000:
                    return None  # нет больше возможности поставить карабль, возврат пустой доски
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipExeption:
                    pass

        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print("--------------------------------------------------------")
        print("          Приветсвуем вас в игре морской бой")
        print("---------------------------------------------------------")
        print(" формат ввода: x y | x - номер строки | y - номер столбца")
        print("---------------------------------------------------------")

    @staticmethod
    def hstack(first, second):
        first_sp = first.split("\n")
        second_sp = second.split("\n")
        max_width = max(map(len, first_sp))
        max_len = max(len(first_sp),len(second_sp))
        first_sp += [""] * (max_len - len(first_sp))
        second_sp += [""] * (max_len - len(second_sp))
        text = []
        for f, s in zip(first_sp, second_sp):
            text.append(f"{f: <{max_width}}   :   {s: <{max_width}}")
        return "\n".join(text)

# цикл самой игры

    def loop(self):
        num = 0
        while True:
            #print("-" * 20)
            user_board = "Доска пользователя:\n\n" + str(self.us.board)
            ai_board = "Доска компьютера:\n\n" + str(self.ai.board)
            print(self.hstack(user_board, ai_board))
            if num % 2 == 0:
                print("-" * 20)
                #print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                #print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1
            if self.ai.board.defeat():
                print("-" * 20)
                print("Пользователь выиграл!")
                break
            if self.us.board.defeat():
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()
#Начальные условия для старта игры
g = Game(9, [4, 3, 3, 2, 2, 2, 1, 1, 1, 1], False)
#g = Game()
g.start()
