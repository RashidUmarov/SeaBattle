from Ship import Board, Ship, Pos, getRandomPalyer


# класс внутриигрового сообщения
class GameEvent:
    # нужно ввести координаты выстрела
    Event_Input = 0
    # событие "Смена игрока"
    Event_ChangePlayer = 1
    # событие Выстрел
    Event_Hit = 2
    # событие отрисовки
    Event_Draw = 3
    # событие выхода из игры
    Event_Quit = 100
    # событие победы
    Event_Win = 200

    def __init__(self, type, data=None, player=None) -> None:
        self.type = type
        self.data = data
        self.player = player

    def getType(self):
        return self.type

    def getData(self):
        return self.data

    def getPlayer(self):
        return self.player

    def __str__(self):
        stype = 'Event_Input'
        if type == 1:
            stype = 'Event_ChangePlayer'
        elif type == 2:
            stype = 'Event_Hit'
        elif type == 3:
            stype = 'Event_Draw'
        elif type == 100:
            stype = 'Event_Quit'
        elif type == 200:
            stype = 'Event_Win'
        return f'{stype}, pos({str(self.data)}), player {self.player}'


# -------------------------------------------------
# сюда будем помещать события
class EventList:
    # очередь событий
    events = []

    # забрать событие из очереди
    def getEvent(self):
        return self.events.pop(0)

    # добавить событие в очередь
    def addEvent(self, event):
        self.events.append(event)


# --------------------------------------------------
# класс игровой логики
class GameLogic:
    def __init__(self, shipsList1, shipList2) -> None:
        self.player = getRandomPalyer()
        # self.player = 1  Computer
        # print(f'GameLogic __init__: player={self.player}')
        # игровое поле человека
        ships_on_board=0
        while ships_on_board!=len(shipsList1):
            self.human_board = Board(6, 100, shipsList1)
            ships_on_board=len(self.human_board.ships)
        print(f'Human has {ships_on_board} ships')
        # игровое поле компьютера
        ships_on_board=0
        while ships_on_board!=len(shipsList1):
            self.PC_board = Board(6, 100, shipList2)
            ships_on_board = len(self.PC_board.ships)
        print(f'Computer has {ships_on_board} ships')
        # список выстрелов человека
        self.humanHitList = []
        # список выстрелов компьютера
        self.pcHitList = []
        #  очередь событий
        self.events = None

    def setEventsList(self, events):
        self.events = events

    # метод обработки сообщений, которые приходят к игровой логике
    def processEvent(self, event):
        win=False
        # событие ожидания координат выстрела
        if event.type == GameEvent.Event_Input:
            pos = self.getInput(player=self.player);
            self.events.addEvent(GameEvent(type=GameEvent.Event_Hit, data=pos, player=self.player))

        # событие смены игрока
        if event.type == GameEvent.Event_ChangePlayer:
            self.player = 0 if self.player == 1 else 1
            self.events.addEvent(GameEvent(type=GameEvent.Event_Input, player=self.player))

        # событие выстрела - нужно проверить результат
        if event.type == GameEvent.Event_Hit:
            # проверим выстрел человека на повтор
            if event.player == 0 and event.data in self.humanHitList:
                print("Повторный ввод, ошибка! ")
                # заново отправляем делать ввод
                self.events.addEvent(GameEvent(type=GameEvent.Event_Input, player=self.player))
            else:  # отработаем выстрел
                pos = event.data
                result = None
                # получим результат выстрела
                if event.player == 0:
                    result = self.PC_board.hit(pos)
                    self.PC_board.checkShips()
                    print(f'Computer: left {self.PC_board.liveShips()} ships')
                    # убит и нет больше живых кораблей
                    if result == 2 and not self.PC_board.liveShips():
                        self.events.addEvent(GameEvent(type=GameEvent.Event_Draw))
                        self.events.addEvent(GameEvent(type=GameEvent.Event_Win, player=event.player))
                        win=True # самому не нравится костыль
                else:
                    result = self.human_board.hit(pos)
                    self.human_board.checkShips()
                    print(f'Human: left {self.human_board.liveShips()} ships')
                    # убит и нет больше живых кораблей
                    if result == 2 and not self.human_board.liveShips():
                        self.events.addEvent(GameEvent(type=GameEvent.Event_Draw))
                        self.events.addEvent(GameEvent(type=GameEvent.Event_Win, player=event.player))
                        win = True  # самому не нравится костыль
                # если мимо, то меняемм игрока
                if not result:
                    self.events.addEvent(GameEvent(type=GameEvent.Event_Draw))
                    self.events.addEvent(GameEvent(type=GameEvent.Event_ChangePlayer))
                else:
                    if not win:
                        self.events.addEvent(GameEvent(type=GameEvent.Event_Draw))
                        self.events.addEvent(GameEvent(type=GameEvent.Event_Input))

        # событие отрисовки - нужно показать доску
        if event.type == GameEvent.Event_Draw:
            self.draw()

    # получить координаты выстрела
    def getInput(self, player):
        # если стреляет компьютер
        if player == 1:
            # берем случайную позицию, которой еще нет в списке выстрелов
            while True:
                # pos not in self.pcHitList:
                # соблюдаем размеры поля
                pos = Pos.getRandomPos(self.human_board.size - 1, self.human_board.size - 1)
                if pos not in self.pcHitList:
                    self.pcHitList.append(pos)
                    break
            print(f'Выстрел компьютера {str(pos.addPos(Pos(1, 1)))}')
            return pos
        else:  # стреляет человек
            return self.getHumanInput()

    # получить ввод от человека
    def getHumanInput(self):
        text = 'Введите строку и столбец без пробела (11-12-..-66):'
        choice = ""
        # цикл, пока не введут только цифры
        while not choice.isnumeric():
            choice = input(text)
            check = choice.replace(' ', '')
            if check.isnumeric():
                break
        # завершение игры
        if len(choice) == 1 and choice.find('0') != -1:
            return 0
        else:
            if len(choice.replace(' ', '')) == 2:  # строка и столбец
                row = int(choice[0]) - 1
                col = int(choice[1]) - 1
                return Pos(row, col)
            else:  # число содержит более 2-х знаков
                print("   Неверный ввод")
                return None

    def getHumanBoardString(self):
        # представление нашей доски
        return self.human_board.getBoardAsStringList()

    def getPcBoardString(self,show=True):
        # представление нашей доски
        return self.PC_board.getBoardAsStringList(hide=not show)


# -----------------------------------------
class ConsoleGameGui:
    def __init__(self, logic) -> None:
        self.logic = logic
        self.events = EventList()
        self.logic.setEventsList(self.events)
        self.players=['Human','Computer']

    def initEvents(self):
        self.events.addEvent(GameEvent(type=GameEvent.Event_Input, data=None, player=self.logic.player))

    def start(self):
        print('Начинаем игру "Морской бой"\n')
        self.draw()
        running = True
        while running:
            self.initEvents()

            while self.events.events:
                event = self.events.getEvent()
                if event.type == GameEvent.Event_Quit:
                    print('Игра прекращена\n')
                    running = False
                elif event.type == GameEvent.Event_Win:
                    print(f'Ура,  победил {self.players[event.player]}!\n')
                    running = False
                elif event.type == GameEvent.Event_Draw:
                    self.draw()
                else:
                    self.processEvent(event)

    def processEvent(self, event):
        self.logic.processEvent(event)

    # показать доску
    def draw(self, finish=False):
        # Выведем доски
        humanBoard = self.logic.getHumanBoardString()
        pcBoard = self.logic.getPcBoardString(finish)
        print('Human                             Computer')
        # теперь соберем обе доски в единое табло и покажем
        for i in range(len(humanBoard)):
            s = humanBoard[i] + '      ' + pcBoard[i]
            print(s)
        print('')


# --------------------------------------------
if __name__ == "__main__":
    shipsHuman = Ship.getShipList(3, 2, 2, 1, 1, 1)
    shipsPC = Ship.getShipList(3, 2, 2, 1, 1, 1)
    game = ConsoleGameGui(GameLogic(shipsHuman, shipsPC))
    game.start()
    quit()
