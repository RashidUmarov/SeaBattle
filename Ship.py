import math
import random as rnd


def getRandomPalyer():
    return rnd.randint(0, 1)


# класс позиции Строка-Столбец
class Pos:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def getRow(self):
        return self.row

    def getCol(self):
        return self.col

    def getX(self):
        return self.getCol()

    def getY(self):
        return self.getRow()

    def addPos(self, pos):
        r = self.row + pos.getRow()
        c = self.col + pos.getCol()
        return Pos(r, c)

    # получить случайную позицию в диапазоне от (0,0) до (rows-1,cols-1)
    @staticmethod
    def getRandomPos(rows, cols):
        row = rnd.randint(0, rows)
        col = rnd.randint(0, cols)
        pos = Pos(row, col)
        return pos

    def __repr__(self):
        return f'({self.row},{self.col})'

    def __str__(self):
        return f'({self.row},{self.col})'

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    # расстояние между 2-мя позициями
    def distance(self, other_pos):
        return math.sqrt((self.row - other_pos.row) ** 2 + (self.col - other_pos.col) ** 2)


# палуба корабля
class Unit:
    def __init__(self, pos, alive):
        self.pos = pos  # позиция палубы
        self.alive = alive  # True живой, False убит

    def getPos(self):
        return self.pos

    def setPos(self, pos):
        self.pos = pos

    # живой - True
    def isAlive(self):
        return self.alive

    # убит - False
    def isDead(self):
        return not self.alive

    # позиция палубы на игровом поле
    def posOnBoard(self):
        return f'({self.pos.row + 1},{self.pos.col + 1}  {self.alive})'

    def __str__(self):
        return f'({self.pos.row},{self.pos.col}  {self.alive})'

    def __repr__(self):
        return f'({self.pos.row},{self.pos.col}  {self.alive})'


# корабль
class Ship:
    def __init__(self, units):
        # список палуб
        self.units = []
        self.units.append(Unit(Pos(0, 0), True))
        while len(self.units) < units:
            row = rnd.randint(-1, 1)
            col = rnd.randint(-1, 1)
            unit = Unit(Pos(row, col), True)
            OK = False
            Clash = False
            for u in self.units:
                d = u.getPos().distance(unit.getPos())
                # print(f' {str(u.getPos())} - {str(unit.getPos())} ={d}')
                if d == 1:
                    OK = True
                elif d == 0:
                    Clash = True
            if OK and not Clash:
                self.units.append(unit)

    # создать список кораблей с указанным количеством палуб
    @staticmethod
    def getShipList(*args):
        ships = []
        for units in args:
            ship = Ship(units)
            ships.append(ship)
        return ships

    def changePos(self, pos):
        for u in self.units:
            new_pos = u.getPos().addPos(pos)
            u.setPos(new_pos)

    # строковое описание корабля на игровом поле
    def posOnBoard(self):
        description = ''
        for i, u in enumerate(self.units):
            description += f'u{i + 1}: {u.posOnBoard()} \n'
        return description

    def __str__(self):
        out = ''
        for i, u in enumerate(self.units):
            out += f'u{i + 1}: {str(u)} \n'
        return out

    def __repr__(self):
        out = ''
        for i, u in enumerate(self.units):
            out += f'u{i + 1}{str(u)}  '
        return out

    def isAlive(self):
        return any(list(map(Unit.isAlive, self.units)))

    def isDamaged(self):
        return any(list(map(Unit.isDead, self.units)))

    def isDead(self):
        return all(list(map(Unit.isDead, self.units)))

    def Status(self):
        return f'  Alive:{self.isAlive()}\n  Damaged:{self.isDamaged()}\n  Dead:{self.isDead()}'


# игровое поле
class Board:

    def __init__(self, size):
        self.empty = ' '  # пустая клетка
        self.miss = '-'  # промах
        self.zero = '·'  # пустая клетка рядом с убитым кораблем
        self.size = size  # размер поля в ячейках [size x size]
        self.cells = []  # ячейки поля
        self.hits = []  # храним выстрелы по игровому полю
        self.ships = []  # список кораблей на игровом поле
        # список позиций для обхода вокруг клетки
        self.neighbours = [Pos(-1, 0),
                           Pos(0, 1),
                           Pos(1, 0),
                           Pos(0, -1)
                           ]
        # заполняем ячейки начального пустого поля
        for i in range(size):
            row = []
            for k in range(size):
                row.append(self.empty)
            self.cells.append(row)
        return None

    # конструктор со списком кораблей
    def __init__(self, size, attempts, shiplist):
        # self.__init__(size)  не прокатило
        self.empty = ' '  # пустая клетка
        self.miss = '-'  # промах
        self.zero = '·'  # пустая клетка рядом с убитым кораблем
        self.size = size  # размер поля в ячейках [size x size]
        self.cells = []  # ячейки поля
        self.hits = []  # храним выстрелы по игровому полю
        self.ships = []  # список кораблей на игровом поле
        # список позиций для обхода вокруг клетки
        self.neighbours = [Pos(-1, 0),
                           Pos(0, 1),
                           Pos(1, 0),
                           Pos(0, -1)
                           ]
        # заполняем ячейки начального пустого поля
        for i in range(size):
            row = []
            for k in range(size):
                row.append(self.empty)
            self.cells.append(row)
        for ship in shiplist:
            if not self.tryToAddShipd(ship, attempts):
                break

    def getCells(self):
        return self.cells

    def boardPrint(self):
        print(f'  | 1 | 2 | 3 | 4 | 5 | 6 |')
        print(f'  – – – – – – – – – – – – – ')
        for i, r in enumerate(self.cells):
            print(f'{i + 1} | ' + ' | '.join(r) + ' |')

    # hide = True означает отображение поля для противника
    def getBoardAsStringList(self, hide=False):
        info = []
        info.append(f'  | 1 | 2 | 3 | 4 | 5 | 6 |')
        info.append(f'  – – – – – – – – – – – – – ')
        # показываем поле для себя
        if not hide:
            for i, r in enumerate(self.cells):
                info.append(f'{i + 1} | ' + ' | '.join(r) + ' |')
        # показываем поле для противника
        else:
            hidecells = self.getHideCelss()
            for i, r in enumerate(hidecells):
                info.append(f'{i + 1} | ' + ' | '.join(r) + ' |')

        return info

    # возвращает клетки, на которых скрыты живые корабли
    def getHideCelss(self):
        hidecells = []
        # сначала скопируем клетки как есть
        for r, row in enumerate(self.cells):
            hide_row = []
            for c, col in enumerate(row):
                hide_row.append(self.cells[r][c])
            hidecells.append(hide_row)
        # теперь замажем клетки с живыми палубами
        for ship in self.ships:
            if ship.isAlive():
                for unit in ship.units:
                    if unit.isAlive():
                        try:
                            hidecells[unit.getPos().getRow()][unit.getPos().getCol()] = self.empty
                        except Exception as e:
                            pass
        # теперь пометим клетки вокруг убитых кораблей
        for ship in self.ships:
            if ship.isDead():
                # проверим окрестности каждой палубы
                for unit in ship.units:
                    unit_pos = unit.getPos()
                    # обойдем клетки вокруг палубы
                    for shift in self.neighbours:
                        # если клетка внутри игрового поля,
                        check_pos = unit_pos.addPos(shift)
                        if self.isIn(check_pos):
                            row = check_pos.getRow()
                            col = check_pos.getCol()
                            # если клетка подбита или стоит знак промаха
                            if hidecells[row][col] == 'X' or hidecells[row][col] == self.miss:
                                pass  # ничего не меняем
                            else:
                                hidecells[row][col] = self.zero  # пометим как пустое

        return hidecells

    # проверяет позицию на попадание в игровое поле
    def isIn(self, pos):
        if not isinstance(pos, Pos):
            return False
        if pos.getRow() < 0 or pos.getRow() >= self.size:
            return False
        if pos.getCol() < 0 or pos.getCol() >= self.size:
            return False
        return True

    # проверяет, что все палубы корабля попадают в игровое поле
    def shipIsIn(self, ship, pos):
        for u in ship.units:
            unit_pos = Pos(u.getPos().getRow() + pos.getRow(),
                           u.getPos().getCol() + pos.getCol())
            if not self.isIn(unit_pos):
                return False
        return True

    # проверяет, что новый корабль не попадает в границы другого корабля
    def noClashWithOtherShips(self, ship, pos):
        for r in range(0, self.size):
            for c in range(0, self.size):
                if self.cells[r][c] == '■':
                    p = Pos(r, c)
                    if p == pos:
                        return False
                    for unit in ship.units:
                        test_pos = unit.getPos().addPos(pos)
                        if p.distance(test_pos) < 2:
                            return False
        return True

    # помещает корабль на игровое поле
    def putShip(self, ship, pos):
        for u in ship.units:
            r = u.getPos().getRow() + pos.getRow()
            c = u.getPos().getCol() + pos.getCol()
            self.cells[r][c] = '■'

    # отмечает знаком X подбитые палубы
    def checkShips(self):
        for ship in self.ships:
            for unit in ship.units:
                if unit.isDead():
                    r = unit.getPos().getRow()
                    c = unit.getPos().getCol()
                    self.cells[r][c] = 'X'

    # возвращает количество живых кораблей на доске
    def liveShips(self):
        live=len(list(filter(Ship.isAlive,self.ships)))
        return live

    # помещает корабль на доску, ставит ему локальную позицию и добавляет в список кораблей
    def addShip(self, ship, pos):
        self.putShip(ship, pos)
        ship.changePos(pos)
        self.ships.append(ship)

    # попытка добавить корабль на доску
    def tryToAddShipd(self, ship, attempts):
        res = False
        for attempt in range(attempts):
            pos = Pos.getRandomPos(5, 5)
            if self.shipIsIn(ship, pos) and self.noClashWithOtherShips(ship, pos):
                self.putShip(ship, pos)
                self.addShip(ship, pos)
                if __name__ == '__main__':
                    print(f'ship added on attempt #{attempt + 1} ')
                res = True
                break
        return res

    # добавляет позицию выстрела в список,
    def hit(self, pos):
        if pos is None:
            return -1
        # если уже стреляли по этой клетке, то взведем исключение
        if pos in self.hits:
            # if False:
            #raise ValueError('Сюда уже стреляли ')
            print('   Сюда уже стреляли, повтор хода ')
            return -1
        else:
            self.hits.append(pos)
            # проверим корабли на попадание
            for ship in self.ships:
                for unit in ship.units:
                    if pos == unit.getPos():
                        #self.cells[pos.getRow()][pos.getCol()] == 'X'
                        unit.alive = False
                        if __name__=='__main__':
                            print('Попадание! \n' + ship.posOnBoard())
                        if ship.isDead():
                            print('   Убит')
                            return 2
                        else:
                            print('   Ранен')
                            return 1
                    else:
                        self.cells[pos.getRow()][pos.getCol()] = self.miss
            print('   Мимо')
            return 0


if __name__ == '__main__':
    """
    units = rnd.randint(1, 3)
    ship = Ship(units)
    print(ship)

    board = Board(6)
    #for r in board.getCells():
    #    print(r)
    # print('\nBoard')
    # board.boardPrint()
    ship = Ship(3)
    count = 0
    while True:
        count += 1
        row = rnd.randint(0, 5)
        col = rnd.randint(0, 5)
        pos = Pos(row, col)
        if board.shipIsIn(ship, pos):
            board.putShip(ship, pos)
            break
    
    """
    # теперь проверим добавление всех кораблей
    board = Board(6,100,[])
    ships = []
    ship = Ship(3)
    while True:
        pos = Pos.getRandomPos(5, 5)
        if board.shipIsIn(ship, pos):
            board.putShip(ship, pos)
            board.addShip(ship, pos)
            ships.append(ship)
            break

    print('\nBoard with ship')
    print('big ship\n' + str(ship))
    board.boardPrint()

    # еще 2 корабля
    ship2 = Ship(2)
    ship3 = Ship(2)

    print('ship2 status:\n' + ship2.Status() + "\n")
    """
    print('ship2 is Alive:', ship2.isAlive())
    print('ship2 is Damaged:', ship2.isDamaged())
    print('ship2 is Dead:', ship2.isDead())
    """

    print('ship2:\n' + str(ship2))
    while True:
        pos = Pos.getRandomPos(5, 5)
        # print('pos=',pos)
        if board.shipIsIn(ship2, pos) and board.noClashWithOtherShips(ship2, pos):
            board.putShip(ship2, pos)
            board.addShip(ship2, pos)
            ships.append(ship2)
            break

    print('\nBoard with 2 ships')
    board.boardPrint()

    ship3.units[1].alive = False
    print('')
    print('ship3 status:\n' + ship3.Status() + "\n")
    print('ship3:\n' + str(ship3))

    while True:
        pos = Pos.getRandomPos(5, 5)
        # print('pos=',pos)
        if board.shipIsIn(ship3, pos) and board.noClashWithOtherShips(ship3, pos):
            board.putShip(ship3, pos)
            board.addShip(ship3, pos)
            ships.append(ship3)
            break

    print('\nBoard with 3 ships')
    board.boardPrint()

    ship4 = Ship(1)
    ship4.units[0].alive = False
    print('')
    print('ship4 status:\n' + ship4.Status() + "\n")

    while True:
        pos = Pos.getRandomPos(5, 5)
        # print('pos=',pos)
        if board.shipIsIn(ship4, pos) and board.noClashWithOtherShips(ship4, pos):
            board.putShip(ship4, pos)
            board.addShip(ship4, pos)
            ships.append(ship4)
            break

    board.checkShips()
    print('\nBoard with 4 ships')
    board.boardPrint()

    print('')
    print('тест board.info()')
    info = board.getBoardAsStringList()
    for s in info:
        print(s)
    print('')

    # сделаем 15 случайных выстрелов
    for hit in range(15):
        pos = Pos.getRandomPos(5, 5)
        print(f'{hit + 1}. Выстрел {str(pos.addPos(Pos(1, 1)))}')
        try:
            board.hit(pos)
        except ValueError as e:
            print('Повторный выстрел')
        else:
            board.checkShips()
        info = board.getBoardAsStringList()
        for s in info:
            print(s)
        print('')

    # print(ships)

    print('open view                       hide view')
    # представление нашей доски
    open = board.getBoardAsStringList()
    # представление доски противника
    hide = board.getBoardAsStringList(hide=True)
    # теперь соберем обе доски в единое табло и покажем
    for i in range(len(open)):
        s = open[i] + '      ' + hide[i]
        print(s)

    # теперь проверим массовое добавление
    board = Board(6,100,[])
    ship = Ship(3)
    print(f' ship added:' + str(board.tryToAddShipd(ship, 100)))
    board.boardPrint()

    ship = Ship(2)
    print(f' ship added:' + str(board.tryToAddShipd(ship, 100)))
    board.boardPrint()

    ship = Ship(2)
    print(f' ship added:' + str(board.tryToAddShipd(ship, 100)))
    board.boardPrint()

    ship = Ship(1)
    print(f' ship added:' + str(board.tryToAddShipd(ship, 100)))
    board.boardPrint()

    ship = Ship(1)
    print(f' ship added:' + str(board.tryToAddShipd(ship, 100)))
    board.boardPrint()

    ship = Ship(1)
    print(f' ship added:' + str(board.tryToAddShipd(ship, 100)))
    board.boardPrint()

    print('')
    ships = Ship.getShipList(3, 2, 2, 1, 1, 1)
    print(f'Добавим {len(ships)} кораблей за раз')
    print(ships)
    board.boardPrint()
