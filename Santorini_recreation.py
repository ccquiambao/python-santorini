class Board(object):
    '''
    Game board class, able to check valid movements and build choices
    '''
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        '''
        Create 5x5 board
        '''
        board = []
        for row in range(5):
            new_row = []
            for col in range(5):
                new_row.append(Space(row,col))
            board.append(new_row)
        return board

    def check_levels(self, old_space, new_space):
        '''
        Can only move up 1 level, but can fall down any number of levels.
        Cannot move onto level 4 spaces.
        '''
        if new_space.level - old_space.level <= 1 and new_space.level != 4:
            return True
        else:
            return False

    def check_board(self,old_space, new_space):
        '''
        Checks if movement or build choice is legal. Row and col index must be in 0,1,2,3,4.
        New space, for building or moving,  can only be one space away, diagonally or orthognoally
        '''
        if new_space.col < 0 or new_space.row < 0:
            return False
        elif new_space.col > 5 or new_space.col > 5:
            return False
        elif abs(new_space.row - old_space.row) != 1 and (new_space.row - old_space.row) != 0:
            return False
        elif abs(new_space.col - old_space.col) != 1 and (new_space.col - old_space.col) != 0:
            return False
        else:
            return True

    def valid_movement(self, old_space, new_space):
        '''Checks if movement is legal and new space is empty'''
        if self.check_levels(old_space, new_space) and self.check_board(old_space, new_space) and new_space.occupant is None:
            return True
        else:
            print 'Invalid movement'
            raise Exception

    def valid_build(self,worker, build_space):
        '''
        Checks if build is legal. Build must be one space away, diagonally or orthognoally.
        Cannot build onto a level 4 space
        '''
        if self.check_board(worker.current_space, build_space) and build_space.level < 4 and build_space.occupant is None:
            return True
        else:
            return False

    def print_board(self):
        for row in self.board:
            for ele in row:
                print ele,
            print


class Space(object):
    '''
    Class for each space on the board. Stores coordinates, buildling level, and occupancy
    '''
    def __init__(self, row,col):
        self.row, self.col = row, col
        self.level = 0
        self.occupant = None

    def update_level(self):
        '''
        If built on, level will increase by 1, to a maximum of 4
        '''
        if self.level < 4:
            self.level += 1
        else:
            print 'cannot build further'

    def update_occupant(self, new_occupant=None):
        '''
        If Space is moved into, stores new occupant information.
        If Space is moved out of, empties occupant information.
        '''
        if new_occupant is None:
            self.occupant = None
        else:
            self.occupant = new_occupant

    def __str__(self):
        return '''{}, {} , {:15}, Lvl: {:<4}'''.format(self.row, self.col, self.occupant,self.level)


class Player(object):
    '''
    Class to hold player name and initialize two workers
    '''
    def __init__(self,name):
        self.name = name
        self.worker1 = Worker(self.name, 1)
        self.worker2 = Worker(self.name, 2)


class Worker(object):
    '''
    Workers are moved and used to build. Holds current Space object as an attribute.
    Also holds space from one movement back in case of mistaken action
    '''
    def __init__(self, player, number):
        self.owner = player
        self.number = number
        self.past_space = None
        self.current_space = None

    def __str__(self):
        return '{} Worker{}'.format(self.owner, self.number)

class PlayGame(object):
    '''
    Playing full game. Initializes Board, Players, and Workers
    '''
    def __init__(self, player1_name, player2_name):
        self.finished_game = False
        self.player1 = Player(player1_name)
        self.player2 = Player(player2_name)
        self.current_player = self.player1
        self.game_board = Board()
        self.game_board = self._initialize_workers()

    def _initialize_workers(self):
        '''
        Players take turns placing their workers on the Board before the first turn is taken.
        If an invalid placement happens (chosen space was occupied already, chosen space not on board),
        initialization starts over
        '''
        workers = [self.player1.worker1, self.player2.worker1, self.player1.worker2, self.player2.worker2]
        for worker in workers:
            print '\n'
            self.game_board.print_board()
            print '{}, please place {}'.format(self.current_player.name, worker)
            new_row = int(raw_input('Please enter new row: '))
            new_col = int(raw_input('Please enter new col: '))
            try:
                self.move_worker(worker, new_row, new_col)
                self.change_player()
            except:
                print 'invalid move, place workers again'
                self.game_board = Board()
                self.player1 = Player(self.player1.name)
                self.player2 = Player(self.player2.name)
                self.current_player = self.player1
                break
        else:
            return self.game_board

        print 'Try again'
        return self._initialize_workers()

    def change_player(self):
        '''
        Alternates player turns
        '''
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def move_worker(self, worker, new_row, new_col):
        '''
        Takes in worker, row and column of new space.
        When used in the initialization of Game (worker has no current space), legal movement is not checked.
        In all other cases, movement logic in Board class are checked
        '''
        new_space = self.game_board.board[new_row][new_col]
        if worker.current_space is None:
            if new_row in {0,1,2,3,4} and new_col in {0,1,2,3,4} and self.game_board.board[new_row][new_col].occupant is None:
                self.game_board.board[new_row][new_col].update_occupant(worker)
                worker.current_space = self.game_board.board[new_row][new_col]
                print 'moved worker to {}, {}'.format(new_row,new_col)
            else:
                raise Exception
        else:
            try:
                self.game_board.valid_movement(worker.current_space, new_space)
                worker.current_space.update_occupant()
                new_space.update_occupant(worker)
                worker.past_space = worker.current_space
                worker.current_space = new_space

            except:
                print 'invalid movementt'
                raise Exception

    def build_level(self,worker, build_row, build_col):
        '''
        Checks if build is legal. If so, updates space level
        '''
        if self.game_board.valid_build(worker, self.game_board.board[build_row][build_col]):
            self.game_board.board[build_row][build_col].update_level()
        else:
            print 'cannot build here'
            raise Exception

    def check_winner(self,worker):
        '''
        Game is won when any worker moves onto a level 3 space. Building does not need to occur afterwards.
        '''
        if worker.current_space.level == 3:
            self.finished_game = True
            return True


player1 = raw_input('Please enter Player 1 name: ')
player2 = raw_input('Please enter Player 2 name: ')
test_game = PlayGame(player1, player2)

while not test_game.finished_game:
    test_game.game_board.print_board()

    print '\n'
    print 'Current player is {}'.format(test_game.current_player.name)
    print 'Where is current worker?'
    current_row = int(raw_input('row of current worker?: '))
    current_col = int(raw_input('col of current worker?: '))

    #Player must choose their own worker
    try:
        if test_game.game_board.board[current_row][current_col].occupant.owner == test_game.current_player.name:
            current_worker = test_game.game_board.board[current_row][current_col].occupant
            print 'current worker: {}'.format(current_worker)
        else:
            print 'not your worker'
            continue
    except:
        print 'invalid choice'
        continue

    print '\n'
    print 'Where will worker move?'
    destination_row = int(raw_input('row of destination: '))
    destination_col = int(raw_input('col of destination: '))
    destination = test_game.game_board.board[destination_row][destination_col]

    # Attempts movement, otherwise loop moves to top
    try:
        test_game.move_worker(current_worker,destination_row, destination_col)
    except:
        print 'invalid movement'
        continue

    test_game.game_board.print_board()

    # Check if win condition fulfilled after moving.
    if test_game.check_winner(current_worker):
        print '{} won!'.format(self.current_player.name)
        break

    # Attempts building. If build is illegal, undoes completed movement, turn starts from beginning
    print '\n'
    print 'Where will worker build?'
    build_row = int(raw_input('row to build on: '))
    build_col = int(raw_input('col to build on: '))
    try:
        test_game.build_level(current_worker,build_row,build_col)
    except:
        current_worker.current_space.occupant = None
        current_worker.past_space.occupant = current_worker
        current_worker.current_space = current_worker.past_space
        print 'cannot build here'
        continue

    test_game.change_player()
