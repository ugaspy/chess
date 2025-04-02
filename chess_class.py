class Board:
    def __init__(self):
        """
        Конструктор класса. Инициализирует шахматную доску, создавая начальную расстановку фигур,
        а также пустые списки для истории ходов и отмененных ходов.
        """
        self.board = self.create_board()
        self.move_history = []
        self.redo_history = []

    def create_board(self):
        """
        Создает и возвращает начальную расстановку фигур на шахматной доске.

        Возвращает:
            list: Двумерный список 8x8, представляющий шахматную доску.
        """
        return [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]

    def print_board(self, highlight=[]):
        """
        Выводит текущее состояние доски в консоль.
        Параметры:
            highlight (list): Список кортежей (row, col) для выделения клеток на доске.
        """
        print("    A B C D E F G H")
        print()
        for i in range(8): # Проход по строкам
            print(8 - i, end='   ')
            for j in range(8): # Проход по столбцам
                if (i, j) in highlight:
                    print(f"\033[46m{self.board[i][j]}\033[0m", end=' ') # Выделение клетки (подсветка)
                else:
                    print(self.board[i][j], end=' ')
            print(' ',8 - i)
        print()
        print("    A B C D E F G H")
        print('-----------------------------')

    def parse_position(self, pos):
        """
        Преобразует шахматную нотацию (например, "e4") в индексы строки и столбца.

        Параметры:
            pos (str): Позиция на доске в шахматной нотации (например, "e4").

        Возвращает:
            tuple: Кортеж (row, col), где row — индекс строки (0-7), col — индекс столбца (0-7).
        """
        col = ord(pos[0]) - ord('a')
        row = 8 - int(pos[1])
        return row, col

    def make_move(self, start, end):
        """
        Выполняет ход фигуры с позиции start на позицию end.

        Параметры:
            start (str): Начальная позиция хода (например, "e2").
            end (str): Конечная позиция хода (например, "e4").
        """
        # Позиции в индексы
        start_row, start_col = self.parse_position(start)
        end_row, end_col = self.parse_position(end)

        piece = self.board[start_row][start_col]
        captured_piece = self.board[end_row][end_col]
        
        self.move_history.append((start, end, piece, captured_piece))
        # Выполнение хода
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = '.'

        self.redo_history.clear()

    def undo_move(self):
        """
        Отменяет последний ход.
        """
        if self.move_history:
            start, end, piece, captured_piece = self.move_history.pop()

            start_row, start_col = self.parse_position(start)
            end_row, end_col = self.parse_position(end)
        
            self.board[start_row][start_col] = piece # Возвращаем фигуру на начальную позицию

            self.board[end_row][end_col] = captured_piece # Восстанавливаем взятую фигуру
            
            self.redo_history.append((start, end, piece, captured_piece))

    def redo_move(self):
        """
        Повторяет последний отмененный ход.
        """
        if self.redo_history:
            start, end, piece, captured_piece = self.redo_history.pop()

            start_row, start_col = self.parse_position(start)
            end_row, end_col = self.parse_position(end)
            
            self.board[end_row][end_col] = piece # Выполнение хода
            self.board[start_row][start_col] = '.'
            
            self.move_history.append((start, end, piece, captured_piece))

class Piece:
    def __init__(self, color, position):
        """
        Инициализирует фигуру с указанным цветом и позицией.
        
        Параметры:
            color (str): Цвет фигуры ('white' или 'black').
            position (str): Позиция фигуры в шахматной нотации (например, "e4").
        """
        self.color = color 
        self.position = position

    def is_valid_move(self, board, end):
        """
        Абстрактный метод для проверки допустимости хода.
        
        Параметры:
            board (Board): Объект доски.
            end (str): Конечная позиция хода.
            
        Возвращает:
            bool: True, если ход допустим, иначе False.
        """
        pass

class Pawn(Piece):
    def is_valid_move(self, board, end):
        """
        Проверяет, является ли ход пешки допустимым.
        
        Параметры:
            board (Board): Объект доски.
            end (str): Конечная позиция хода.
            
        Возвращает:
            bool: True, если ход допустим, иначе False.
        """
        start_row, start_col = board.parse_position(self.position)
        end_row, end_col = board.parse_position(end)
        direction = -1 if self.color == 'white' else 1
        if start_col == end_col:
            if start_row + direction == end_row and board.board[end_row][end_col] == '.':
                return True
            if (start_row == 1 or start_row == 6) and start_row + 2 * direction == end_row and board.board[end_row][end_col] == '.' and board.board[start_row + direction][start_col] == '.':
                return True
        elif abs(start_col - end_col) == 1 and start_row + direction == end_row:
            if board.board[end_row][end_col] != '.' and board.board[end_row][end_col].islower() != self.color == 'white':
                return True
        return False
    
    def get_possible_moves(self, board):
        """
        Возвращает список всех возможных ходов для пешки.
        
        Параметры:
            board (Board): Объект доски.
            
        Возвращает:
            list: Список строк с возможными ходами в шахматной нотации.
        """
        moves = []
        start_row, start_col = board.parse_position(self.position)
        direction = -1 if self.color == 'white' else 1

        # Обычный ход вперёд
        end_row = start_row + direction
        if 0 <= end_row < 8:
            if board.board[end_row][start_col] == '.':
                moves.append(f"{chr(start_col + ord('a'))}{8 - end_row}")

                # Двойной ход вперёд для начальной позиции
                if (self.color == 'white' and start_row == 6) or (self.color == 'black' and start_row == 1):
                    end_row = start_row + 2 * direction
                    if board.board[end_row][start_col] == '.':
                        moves.append(f"{chr(start_col + ord('a'))}{8 - end_row}")

        # Взятие фигур по диагонали
        for delta in [-1, 1]:
            end_col = start_col + delta
            if 0 <= end_col < 8:
                end_row = start_row + direction
                if 0 <= end_row < 8:
                    target_piece = board.board[end_row][end_col]
                    if target_piece != '.' and target_piece.islower() != (self.color == 'white'):
                        moves.append(f"{chr(end_col + ord('a'))}{8 - end_row}")

        return moves


class Rook(Piece):
    def is_valid_move(self, board, end):
        """
        Проверяет, является ли ход ладьи допустимым.
        
        Параметры:
            board (Board): Объект доски.
            end (str): Конечная позиция хода.
            
        Возвращает:
            bool: True, если ход допустим, иначе False.
        """
        start_row, start_col = board.parse_position(self.position)
        end_row, end_col = board.parse_position(end)
        if start_row == end_row:
            for col in range(min(start_col, end_col) + 1, max(start_col, end_col)):
                if board.board[start_row][col] != '.':
                    return False
            return board.board[end_row][end_col] == '.' or board.board[end_row][end_col].islower() != self.color == 'white'
        elif start_col == end_col:
            for row in range(min(start_row, end_row) + 1, max(start_row, end_row)):
                if board.board[row][start_col] != '.':
                    return False
            return board.board[end_row][end_col] == '.' or board.board[end_row][end_col].islower() != self.color == 'white'
        return False

    def get_possible_moves(self, board):
        """
        Возвращает список всех возможных ходов для ладьи.
        
        Параметры:
            board (Board): Объект доски.
            
        Возвращает:
            list: Список строк с возможными ходами в шахматной нотации.
        """
        moves = []
        start_row, start_col = board.parse_position(self.position)

        # Движение по горизонтали и вертикали
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = start_row + dx, start_col + dy
            while 0 <= x < 8 and 0 <= y < 8:
                target_piece = board.board[x][y]
                if target_piece == '.':
                    moves.append(f"{chr(y + ord('a'))}{8 - x}")
                else:
                    if target_piece.islower() != (self.color == 'white'):
                        moves.append(f"{chr(y + ord('a'))}{8 - x}")
                    break
                x += dx
                y += dy

        return moves
    
class Knight(Piece):
    def is_valid_move(self, board, end):
        """
        Проверяет, является ли ход коня допустимым.
        
        Параметры:
            board (Board): Объект доски.
            end (str): Конечная позиция хода.
            
        Возвращает:
            bool: True, если ход допустим, иначе False.
        """
        start_row, start_col = board.parse_position(self.position)
        end_row, end_col = board.parse_position(end)
        if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):
            return board.board[end_row][end_col] == '.' or board.board[end_row][end_col].islower() != self.color == 'white'
        return False

    def get_possible_moves(self, board):
        """
        Возвращает список всех возможных ходов для коня.
        
        Параметры:
            board (Board): Объект доски.
            
        Возвращает:
            list: Список строк с возможными ходами в шахматной нотации.
        """
        moves = []
        start_row, start_col = board.parse_position(self.position)

        # Все возможные ходы коня
        for dx, dy in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
            x, y = start_row + dx, start_col + dy
            if 0 <= x < 8 and 0 <= y < 8:
                target_piece = board.board[x][y]
                if target_piece == '.' or target_piece.islower() != (self.color == 'white'):
                    moves.append(f"{chr(y + ord('a'))}{8 - x}")

        return moves
    
class Bishop(Piece):
    def is_valid_move(self, board, end):
        """
        Проверяет, является ли ход слона допустимым.
        
        Параметры:
            board (Board): Объект доски.
            end (str): Конечная позиция хода.
            
        Возвращает:
            bool: True, если ход допустим, иначе False.
        """
        start_row, start_col = board.parse_position(self.position)
        end_row, end_col = board.parse_position(end)
        if abs(start_row - end_row) == abs(start_col - end_col):
            row_step = 1 if end_row > start_row else -1
            col_step = 1 if end_col > start_col else -1
            row, col = start_row + row_step, start_col + col_step
            while row != end_row:
                if board.board[row][col] != '.':
                    return False
                row += row_step
                col += col_step
            return board.board[end_row][end_col] == '.' or board.board[end_row][end_col].islower() != self.color == 'white'
        return False
    
    def get_possible_moves(self, board):
        """
        Возвращает список всех возможных ходов для слона.
        
        Параметры:
            board (Board): Объект доски.
            
        Возвращает:
            list: Список строк с возможными ходами в шахматной нотации.
        """
        moves = []
        start_row, start_col = board.parse_position(self.position)

        # Движение по диагоналям
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            x, y = start_row + dx, start_col + dy
            while 0 <= x < 8 and 0 <= y < 8:
                target_piece = board.board[x][y]
                if target_piece == '.':
                    moves.append(f"{chr(y + ord('a'))}{8 - x}")
                else:
                    if target_piece.islower() != (self.color == 'white'):
                        moves.append(f"{chr(y + ord('a'))}{8 - x}")
                    break
                x += dx
                y += dy

        return moves

class Queen(Piece):
    def is_valid_move(self, board, end):
        """
        Проверяет, является ли ход ферзя допустимым.
        
        Параметры:
            board (Board): Объект доски.
            end (str): Конечная позиция хода.
            
        Возвращает:
            bool: True, если ход допустим, иначе False.
        """
        return Rook.is_valid_move(self, board, end) or Bishop.is_valid_move(self, board, end)
    
    def get_possible_moves(self, board):
        """
        Возвращает список всех возможных ходов для ферзя.
        
        Параметры:
            board (Board): Объект доски.
            
        Возвращает:
            list: Список строк с возможными ходами в шахматной нотации.
        """
        # Ферзь объединяет возможности ладьи и слона
        return Rook.get_possible_moves(self, board) + Bishop.get_possible_moves(self, board)


class King(Piece):
    def is_valid_move(self, board, end):
        """
        Проверяет, является ли ход короля допустимым.
        
        Параметры:
            board (Board): Объект доски.
            end (str): Конечная позиция хода.
            
        Возвращает:
            bool: True, если ход допустим, иначе False.
        """
        start_row, start_col = board.parse_position(self.position)
        end_row, end_col = board.parse_position(end)
        if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
            return board.board[end_row][end_col] == '.' or board.board[end_row][end_col].islower() != self.color == 'white'
        return False
    
    def get_possible_moves(self, board):
        """
        Возвращает список всех возможных ходов для короля.
        
        Параметры:
            board (Board): Объект доски.
            
        Возвращает:
            list: Список строк с возможными ходами в шахматной нотации.
        """
        moves = []
        start_row, start_col = board.parse_position(self.position)

        # Все возможные ходы короля
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                x, y = start_row + dx, start_col + dy
                if 0 <= x < 8 and 0 <= y < 8:
                    target_piece = board.board[x][y]
                    if target_piece == '.' or target_piece.islower() != (self.color == 'white'):
                        moves.append(f"{chr(y + ord('a'))}{8 - x}")

        return moves

class Game:
    def __init__(self):
        """
        Инициализирует игру, создавая доску и устанавливая начальные значения.
        """
        self.board = Board()
        self.turn = 'white'
        self.move_count = 0

    def play(self):
        """
        Основной игровой цикл, обрабатывающий ходы игроков и команды.
        """
        while True:
            self.board.print_board()
            print(f"Ход {'белых' if self.turn == 'white' else 'черных'}. Введите ход (например, e2 e4) или команду (back, next, hint, threats, save, load, exit):")
            command = input().strip().lower()
            
            if command == 'exit':
                break
            elif command.startswith('back'):
                self.board.undo_move()
                self.move_count -= 1
                self.turn = 'black' if self.turn == 'white' else 'white'
            elif command.startswith('next'):
                self.board.redo_move()
                self.move_count += 1
                self.turn = 'black' if self.turn == 'white' else 'white'
            elif command.startswith('hint'):
                pos = command.split()[1]
                self.hint(pos)
            elif command.startswith('threats'):
                pos = command.split()[1]
                self.threats(pos)
            elif command.startswith('save'):
                filename = command.split()[1]
                self.save_game(filename)
            elif command.startswith('load'):
                filename = command.split()[1]
                self.load_game(filename)
            else:
                try:
                    start, end = command.split()
                    if self.is_valid_move(start, end):
                        self.board.make_move(start, end)
                        self.move_count += 1
                        
                        # Проверяем шах и мат после хода
                        if self.is_check('black' if self.turn == 'white' else 'white'):
                            if self.is_checkmate('black' if self.turn == 'white' else 'white'):
                                print(f"Мат! {'Белые' if self.turn == 'black' else 'Черные'} победили!")
                                print(f"Количество ходов: {self.move_count}")
                                break
                            else:
                                print("Шах!")
                        
                        self.turn = 'black' if self.turn == 'white' else 'white'
                    else:
                        print("Неверный ход. Повторите попытку.")
                except ValueError:
                    print("Неверный формат команды. Повторите попытку.")

    def is_valid_move(self, start, end):
        """
        Проверяет, является ли ход допустимым.
        
        Параметры:
            start (str): Начальная позиция хода.
            end (str): Конечная позиция хода.
            
        Возвращает:
            bool: True, если ход допустим, иначе False.
        """
        start_row, start_col = self.board.parse_position(start)
        end_row, end_col = self.board.parse_position(end)
        piece = self.board.board[start_row][start_col]
        
        if piece == '.':
            return False
        
        # Проверяем, принадлежит ли фигура текущему игроку
        if (self.turn == 'white' and piece.islower()) or (self.turn == 'black' and piece.isupper()):
            return False

        # Проверяем, является ли ход легальным для данной фигуры
        is_legal = False
        if piece.lower() == 'p':
            is_legal = Pawn('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'r':
            is_legal = Rook('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'n':
            is_legal = Knight('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'b':
            is_legal = Bishop('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'q':
            is_legal = Queen('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'k':
            is_legal = King('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)

        if not is_legal:
            return False

        # Проверяем, не оставляет ли ход короля под шахом
        temp_board = [row[:] for row in self.board.board]
        temp_board[end_row][end_col] = piece
        temp_board[start_row][start_col] = '.'
        
        # Находим позицию короля
        king_pos = None
        for i in range(8):
            for j in range(8):
                if (self.turn == 'white' and temp_board[i][j] == 'K') or \
                   (self.turn == 'black' and temp_board[i][j] == 'k'):
                    king_pos = (i, j)
                    break
            if king_pos:
                break

        # Проверяем, находится ли король под шахом после хода
        for i in range(8):
            for j in range(8):
                if temp_board[i][j] != '.' and \
                   temp_board[i][j].islower() != (self.turn == 'black'):
                    # Проверяем, может ли фигура атаковать короля
                    if self.is_piece_attacking_king(temp_board, (i, j), king_pos):
                        return False

        return True

    def is_piece_attacking_king(self, board, piece_pos, king_pos):
        """
        Проверяет, может ли фигура атаковать короля.
        
        Параметры:
            board (list): Двумерный список, представляющий доску.
            piece_pos (tuple): Позиция фигуры (row, col).
            king_pos (tuple): Позиция короля (row, col).
            
        Возвращает:
            bool: True, если фигура может атаковать короля, иначе False.
        """
        piece = board[piece_pos[0]][piece_pos[1]]
        piece_type = piece.lower()
        
        if piece_type == 'p':
            # Для пешки проверяем только взятие по диагонали
            direction = -1 if piece.isupper() else 1
            for delta in [-1, 1]:
                x = piece_pos[0] + direction
                y = piece_pos[1] + delta
                if (x, y) == king_pos:
                    return True
        elif piece_type == 'r':
            # Для ладьи проверяем прямые линии
            if piece_pos[0] == king_pos[0] or piece_pos[1] == king_pos[1]:
                return self.is_path_clear(board, piece_pos, king_pos)
        elif piece_type == 'n':
            # Для коня проверяем L-образные ходы
            dx = abs(piece_pos[0] - king_pos[0])
            dy = abs(piece_pos[1] - king_pos[1])
            return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)
        elif piece_type == 'b':
            # Для слона проверяем диагонали
            if abs(piece_pos[0] - king_pos[0]) == abs(piece_pos[1] - king_pos[1]):
                return self.is_path_clear(board, piece_pos, king_pos)
        elif piece_type == 'q':
            # Для ферзя проверяем прямые линии и диагонали
            if piece_pos[0] == king_pos[0] or piece_pos[1] == king_pos[1] or \
               abs(piece_pos[0] - king_pos[0]) == abs(piece_pos[1] - king_pos[1]):
                return self.is_path_clear(board, piece_pos, king_pos)
        elif piece_type == 'k':
            # Для короля проверяем соседние клетки
            dx = abs(piece_pos[0] - king_pos[0])
            dy = abs(piece_pos[1] - king_pos[1])
            return dx <= 1 and dy <= 1

        return False

    def is_path_clear(self, board, start, end):
        """
        Проверяет, свободен ли путь между двумя позициями.
        
        Параметры:
            board (list): Двумерный список, представляющий доску.
            start (tuple): Начальная позиция (row, col).
            end (tuple): Конечная позиция (row, col).
            
        Возвращает:
            bool: True, если путь свободен, иначе False.
        """
        if start[0] == end[0]:  # Горизонтальное движение
            step = 1 if end[1] > start[1] else -1
            for y in range(start[1] + step, end[1], step):
                if board[start[0]][y] != '.':
                    return False
        elif start[1] == end[1]:  # Вертикальное движение
            step = 1 if end[0] > start[0] else -1
            for x in range(start[0] + step, end[0], step):
                if board[x][start[1]] != '.':
                    return False
        else:  # Диагональное движение
            step_x = 1 if end[0] > start[0] else -1
            step_y = 1 if end[1] > start[1] else -1
            x, y = start[0] + step_x, start[1] + step_y
            while x != end[0] and y != end[1]:
                if board[x][y] != '.':
                    return False
                x += step_x
                y += step_y
        return True

    def is_check(self, color):
        """Проверяет, находится ли король под шахом"""
        # Находим позицию короля
        king_pos = None
        for i in range(8):
            for j in range(8):
                if (color == 'white' and self.board.board[i][j] == 'K') or \
                   (color == 'black' and self.board.board[i][j] == 'k'):
                    king_pos = (i, j)
                    break
            if king_pos:
                break

        if not king_pos:
            return False

        # Проверяем, может ли какая-либо фигура противника атаковать короля
        for i in range(8):
            for j in range(8):
                if self.board.board[i][j] != '.' and \
                   self.board.board[i][j].islower() != (color == 'black'):
                    if self.is_piece_attacking_king(self.board.board, (i, j), king_pos):
                        return True

        return False

    def is_checkmate(self, color):
        """Проверяет, является ли шах матом"""
        if not self.is_check(color):
            return False

        # Проверяем все возможные ходы всех фигур
        for i in range(8):
            for j in range(8):
                if self.board.board[i][j] != '.' and \
                   self.board.board[i][j].islower() == (color == 'black'):
                    start = f"{chr(j + ord('a'))}{8 - i}"
                    for x in range(8):
                        for y in range(8):
                            end = f"{chr(y + ord('a'))}{8 - x}"
                            if self.is_valid_move(start, end):
                                # Пробуем сделать ход
                                temp_board = [row[:] for row in self.board.board]
                                self.board.make_move(start, end)
                                # Проверяем, все еще ли король под шахом
                                still_in_check = self.is_check(color)
                                # Возвращаем доску в исходное состояние
                                self.board.board = temp_board
                                # Если есть ход, который выводит из-под шаха, то это не мат
                                if not still_in_check:
                                    return False

        return True

    def hint(self, pos):
        row, col = self.board.parse_position(pos)
        piece = self.board.board[row][col]
        moves = []
        
        if piece.lower() == 'p':
            moves = Pawn('white' if piece.isupper() else 'black', pos).get_possible_moves(self.board)
        elif piece.lower() == 'r':
            moves = Rook('white' if piece.isupper() else 'black', pos).get_possible_moves(self.board)
        elif piece.lower() == 'n':
            moves = Knight('white' if piece.isupper() else 'black', pos).get_possible_moves(self.board)
        elif piece.lower() == 'b':
            moves = Bishop('white' if piece.isupper() else 'black', pos).get_possible_moves(self.board)
        elif piece.lower() == 'q':
            moves = Queen('white' if piece.isupper() else 'black', pos).get_possible_moves(self.board)
        elif piece.lower() == 'k':
            moves = King('white' if piece.isupper() else 'black', pos).get_possible_moves(self.board)
        
        highlight = [(self.board.parse_position(move)[0], self.board.parse_position(move)[1]) for move in moves]
        self.board.print_board(highlight)

    def threats(self, pos):
        row, col = self.board.parse_position(pos)
        piece = self.board.board[row][col]
        threats = []

        for i in range(8):
            for j in range(8):
                other_piece = self.board.board[i][j]
                # Проверяем, что это фигура противника
                if other_piece != '.' and other_piece.islower() != piece.islower():
                    # Получаем возможные ходы для этой фигуры
                    if other_piece.lower() == 'p':
                        # Для пешки учитываем только взятие по диагонали
                        direction = -1 if other_piece.isupper() else 1  # Направление движения пешки
                        for delta in [-1, 1]:  # Проверяем обе диагонали
                            x = i + direction
                            y = j + delta
                            if 0 <= x < 8 and 0 <= y < 8:
                                if (x, y) == (row, col):
                                    threats.append((i, j))
                    elif other_piece.lower() == 'r':
                        # Для ладьи проверяем прямые линии
                        if i == row or j == col:
                            # Проверяем, нет ли фигур на пути
                            if i == row:
                                step = 1 if j < col else -1
                                y = j + step
                                while y != col:
                                    if self.board.board[i][y] != '.':
                                        break
                                    y += step
                                if y == col:
                                    threats.append((i, j))
                            elif j == col:
                                step = 1 if i < row else -1
                                x = i + step
                                while x != row:
                                    if self.board.board[x][j] != '.':
                                        break
                                    x += step
                                if x == row:
                                    threats.append((i, j))
                    elif other_piece.lower() == 'n':
                        # Для коня проверяем все возможные ходы
                        knight_moves = [
                            (i + 2, j + 1), (i + 2, j - 1),
                            (i - 2, j + 1), (i - 2, j - 1),
                            (i + 1, j + 2), (i + 1, j - 2),
                            (i - 1, j + 2), (i - 1, j - 2)
                        ]
                        for x, y in knight_moves:
                            if 0 <= x < 8 and 0 <= y < 8:
                                if (x, y) == (row, col):
                                    threats.append((i, j))
                    elif other_piece.lower() == 'b':
                        # Для слона проверяем диагонали
                        if abs(i - row) == abs(j - col):
                            step_x = 1 if row > i else -1
                            step_y = 1 if col > j else -1
                            x, y = i + step_x, j + step_y
                            while x != row and y != col:
                                if self.board.board[x][y] != '.':
                                    break
                                x += step_x
                                y += step_y
                            if x == row and y == col:
                                threats.append((i, j))
                    elif other_piece.lower() == 'q':
                        # Для ферзя проверяем прямые линии и диагонали
                        if i == row or j == col or abs(i - row) == abs(j - col):
                            if i == row:
                                step = 1 if j < col else -1
                                y = j + step
                                while y != col:
                                    if self.board.board[i][y] != '.':
                                        break
                                    y += step
                                if y == col:
                                    threats.append((i, j))
                            elif j == col:
                                step = 1 if i < row else -1
                                x = i + step
                                while x != row:
                                    if self.board.board[x][j] != '.':
                                        break
                                    x += step
                                if x == row:
                                    threats.append((i, j))
                            else:
                                step_x = 1 if row > i else -1
                                step_y = 1 if col > j else -1
                                x, y = i + step_x, j + step_y
                                while x != row and y != col:
                                    if self.board.board[x][y] != '.':
                                        break
                                    x += step_x
                                    y += step_y
                                if x == row and y == col:
                                    threats.append((i, j))
                    elif other_piece.lower() == 'k':
                        # Для короля проверяем все соседние клетки
                        king_moves = [
                            (i + 1, j), (i - 1, j),
                            (i, j + 1), (i, j - 1),
                            (i + 1, j + 1), (i + 1, j - 1),
                            (i - 1, j + 1), (i - 1, j - 1)
                        ]
                        for x, y in king_moves:
                            if 0 <= x < 8 and 0 <= y < 8:
                                if (x, y) == (row, col):
                                    threats.append((i, j))

        # Подсветим угрозы на доске
        self.board.print_board(threats)
        if threats:
            print(f"Фигура на позиции {pos} под угрозой от следующих фигур:")
            for threat in threats:
                print(f"{self.board.board[threat[0]][threat[1]]} на {chr(threat[1] + ord('a'))}{8 - threat[0]}")
        else:
            print(f"Фигура на позиции {pos} не под угрозой.")

    def save_game(self, filename):
        try:
            with open(filename, 'w') as file:
                file.write(f"{self.turn}\n")
                file.write(f"{self.move_count}\n")
                for move in self.board.move_history:
                    start, end, piece, captured_piece = move

                    start_row, start_col = self.board.parse_position(start)
                    end_row, end_col = self.board.parse_position(end)
                    
                    start_pos = f"{chr(start_col + ord('a'))}{8 - start_row}"
                    end_pos = f"{chr(end_col + ord('a'))}{8 - end_row}"
                    full_notation = f"{piece}{start_pos}{end_pos}"
                    file.write(f"{full_notation}\n")
            print(f"Партия сохранена в файл {filename}")
        except Exception as e:
            print(f"Ошибка при сохранении партии: {e}")

    def load_game(self, filename):
        try:
            with open(filename, 'r') as file:
                self.turn = file.readline().strip()
                self.move_count = int(file.readline().strip())
                self.board = Board()
                for line in file:
                    move = line.strip()
                    piece = move[0]
                    start_pos = move[1:3]
                    end_pos = move[3:5]
                    self.board.make_move(start_pos, end_pos)
            print(f"Партия загружена из файла {filename}")
        except Exception as e:
            print(f"Ошибка при загрузке партии: {e}")

if __name__ == "__main__":
    game = Game()
    game.play()