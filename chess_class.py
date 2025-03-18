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
            
            self.board[end_row][end_col] = piece
            self.board[start_row][start_col] = '.'
            
            self.move_history.append((start, end, piece, captured_piece))

class Piece:
    def __init__(self, color, position):
        self.color = color
        self.position = position

    def is_valid_move(self, board, end):
        pass

class Pawn(Piece):
    def is_valid_move(self, board, end):
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
        start_row, start_col = board.parse_position(self.position)
        end_row, end_col = board.parse_position(end)
        if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):
            return board.board[end_row][end_col] == '.' or board.board[end_row][end_col].islower() != self.color == 'white'
        return False

    def get_possible_moves(self, board):
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
        return Rook.is_valid_move(self, board, end) or Bishop.is_valid_move(self, board, end)
    
    def get_possible_moves(self, board):
        # Ферзь объединяет возможности ладьи и слона
        return Rook.get_possible_moves(self, board) + Bishop.get_possible_moves(self, board)


class King(Piece):
    def is_valid_move(self, board, end):
        start_row, start_col = board.parse_position(self.position)
        end_row, end_col = board.parse_position(end)
        if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
            return board.board[end_row][end_col] == '.' or board.board[end_row][end_col].islower() != self.color == 'white'
        return False
    
    def get_possible_moves(self, board):
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
        self.board = Board()
        self.turn = 'white'
        self.move_count = 0

    def play(self):
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
                    start_row, start_col = self.board.parse_position(start)
                    piece = self.board.board[start_row][start_col]
                    
                    if (self.turn == 'white' and piece.islower()) or (self.turn == 'black' and piece.isupper()):
                        print("Неверный ход. Нельзя трогать фигуры противника.")
                        continue
                    
                    if self.is_valid_move(start, end):
                        end_row, end_col = self.board.parse_position(end)
                        if self.board.board[end_row][end_col] == 'k':
                            print("Черный король повержен! Белые победили!")
                            print("Количество ходов - ", self.move_count + 1)
                            break
                        elif self.board.board[end_row][end_col] == 'K':
                            print("Белый король повержен! Черные победили!")
                            print("Количество ходов - ", self.move_count + 1)
                            break
                        self.board.make_move(start, end)
                        self.move_count += 1
                        self.turn = 'black' if self.turn == 'white' else 'white'
                    else:
                        print("Неверный ход. Повторите попытку.")
                except ValueError:
                    print("Неверный формат команды. Повторите попытку.")

    def is_valid_move(self, start, end):
        start_row, start_col = self.board.parse_position(start)
        end_row, end_col = self.board.parse_position(end)
        piece = self.board.board[start_row][start_col]
        
        if piece == '.':
            return False
        
        if piece.lower() == 'p':
            return Pawn('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'r':
            return Rook('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'n':
            return Knight('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'b':
            return Bishop('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'q':
            return Queen('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        elif piece.lower() == 'k':
            return King('white' if piece.isupper() else 'black', start).is_valid_move(self.board, end)
        
        return False

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

            def is_check(self, color):
                king_pos = None
                threats = []
                
                # Найдём позицию короля
                for i in range(8):
                    for j in range(8):
                        if (color == 'white' and self.board.board[i][j] == 'K') or (color == 'black' and self.board.board[i][j] == 'k'):
                            king_pos = (i, j)
                            break
                    if king_pos:
                        break
                
                if not king_pos:
                    return False
                
                # Проверим, атакована ли позиция короля
                for i in range(8):
                    for j in range(8):
                        piece = self.board.board[i][j]
                        if piece != '.' and piece.islower() != (color == 'white'):
                            moves = self.get_possible_moves(f"{chr(j + ord('a'))}{8 - i}")
                            for move in moves:
                                if self.board.parse_position(move) == king_pos:
                                    threats.append((i, j))
                
                if threats:
                    print(f"Король {'белых' if color == 'white' else 'черных'} находится под шахом!")
                else:
                    print("Шаха нет.")
                
                return bool(threats)

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