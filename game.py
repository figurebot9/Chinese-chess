from enum import Enum
from typing import List, Tuple, Optional
import random

class PieceType(Enum):
    KING = "帅"      # 将/帅
    ADVISOR = "仕"   # 士/仕
    ELEPHANT = "相"  # 象/相
    HORSE = "傌"     # 马
    CHARIOT = "俥"   # 车
    CANNON = "炮"    # 炮
    PAWN = "兵"      # 兵/卒

class PieceColor(Enum):
    RED = "红"
    BLACK = "黑"

class Piece:
    def __init__(self, piece_type: PieceType, color: PieceColor, x: int, y: int):
        self.type = piece_type
        self.color = color
        self.x = x
        self.y = y
        self.selected = False

    def get_valid_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        valid_moves = []
        
        if self.type == PieceType.KING:
            valid_moves = self._get_king_moves(board)
        elif self.type == PieceType.ADVISOR:
            valid_moves = self._get_advisor_moves(board)
        elif self.type == PieceType.ELEPHANT:
            valid_moves = self._get_elephant_moves(board)
        elif self.type == PieceType.HORSE:
            valid_moves = self._get_horse_moves(board)
        elif self.type == PieceType.CHARIOT:
            valid_moves = self._get_chariot_moves(board)
        elif self.type == PieceType.CANNON:
            valid_moves = self._get_cannon_moves(board)
        elif self.type == PieceType.PAWN:
            valid_moves = self._get_pawn_moves(board)
            
        return valid_moves

    def _get_king_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dx, dy in directions:
            new_x, new_y = self.x + dx, self.y + dy
            if self._is_valid_king_move(new_x, new_y, board):
                moves.append((new_x, new_y))
                
        return moves

    def _get_advisor_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dx, dy in directions:
            new_x, new_y = self.x + dx, self.y + dy
            if self._is_valid_advisor_move(new_x, new_y, board):
                moves.append((new_x, new_y))
                
        return moves

    def _get_elephant_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        moves = []
        directions = [(2, 2), (2, -2), (-2, 2), (-2, -2)]
        
        for dx, dy in directions:
            new_x, new_y = self.x + dx, self.y + dy
            if self._is_valid_elephant_move(new_x, new_y, board):
                moves.append((new_x, new_y))
                
        return moves

    def _get_horse_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        moves = []
        directions = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        
        for dx, dy in directions:
            new_x, new_y = self.x + dx, self.y + dy
            if self._is_valid_horse_move(new_x, new_y, board):
                moves.append((new_x, new_y))
                
        return moves

    def _get_chariot_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dx, dy in directions:
            x, y = self.x + dx, self.y + dy
            while 0 <= x < 9 and 0 <= y < 10:
                if board.get_piece(x, y) is None:
                    moves.append((x, y))
                else:
                    if board.get_piece(x, y).color != self.color:
                        moves.append((x, y))
                    break
                x += dx
                y += dy
                
        return moves

    def _get_cannon_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dx, dy in directions:
            x, y = self.x + dx, self.y + dy
            found_piece = False
            
            while 0 <= x < 9 and 0 <= y < 10:
                piece = board.get_piece(x, y)
                if piece is None:
                    if not found_piece:
                        moves.append((x, y))
                else:
                    if not found_piece:
                        found_piece = True
                    elif piece.color != self.color:
                        moves.append((x, y))
                        break
                x += dx
                y += dy
                
        return moves

    def _get_pawn_moves(self, board: 'Board') -> List[Tuple[int, int]]:
        moves = []
        direction = 1 if self.color == PieceColor.RED else -1
        
        # 向前移动
        new_y = self.y + direction
        if 0 <= new_y < 10:
            moves.append((self.x, new_y))
            
        # 过河后可以左右移动
        if (self.color == PieceColor.RED and self.y > 4) or \
           (self.color == PieceColor.BLACK and self.y < 5):
            for dx in [-1, 1]:
                new_x = self.x + dx
                if 0 <= new_x < 9:
                    moves.append((new_x, self.y))
                    
        return moves

    def _is_valid_king_move(self, x: int, y: int, board: 'Board') -> bool:
        # 检查是否在九宫格内
        if self.color == PieceColor.RED:
            if not (3 <= x <= 5 and 0 <= y <= 2):
                return False
        else:
            if not (3 <= x <= 5 and 7 <= y <= 9):
                return False
                
        # 检查目标位置是否有己方棋子
        target_piece = board.get_piece(x, y)
        if target_piece and target_piece.color == self.color:
            return False
            
        return True

    def _is_valid_advisor_move(self, x: int, y: int, board: 'Board') -> bool:
        # 检查是否在九宫格内
        if self.color == PieceColor.RED:
            if not (3 <= x <= 5 and 0 <= y <= 2):
                return False
        else:
            if not (3 <= x <= 5 and 7 <= y <= 9):
                return False
                
        # 检查目标位置是否有己方棋子
        target_piece = board.get_piece(x, y)
        if target_piece and target_piece.color == self.color:
            return False
            
        # 检查移动距离是否为1
        dx = abs(x - self.x)
        dy = abs(y - self.y)
        if dx != 1 or dy != 1:
            return False
            
        return True

    def _is_valid_elephant_move(self, x: int, y: int, board: 'Board') -> bool:
        # 检查是否过河
        if self.color == PieceColor.RED and y > 4:
            return False
        if self.color == PieceColor.BLACK and y < 5:
            return False
            
        # 检查象眼是否被堵
        dx = (x - self.x) // 2
        dy = (y - self.y) // 2
        if board.get_piece(self.x + dx, self.y + dy):
            return False
            
        # 检查目标位置是否有己方棋子
        target_piece = board.get_piece(x, y)
        if target_piece and target_piece.color == self.color:
            return False
            
        # 检查移动距离是否为2
        dx = abs(x - self.x)
        dy = abs(y - self.y)
        if dx != 2 or dy != 2:
            return False
            
        return True

    def _is_valid_horse_move(self, x: int, y: int, board: 'Board') -> bool:
        # 检查马腿
        dx = abs(x - self.x)
        dy = abs(y - self.y)
        if not ((dx == 2 and dy == 1) or (dx == 1 and dy == 2)):
            return False
            
        # 检查马腿是否被堵
        if dx == 2:
            leg_x = self.x + (1 if x > self.x else -1)
        else:
            leg_x = self.x + (2 if x > self.x else -2)
            
        if board.get_piece(leg_x, self.y):
            return False
            
        # 检查目标位置是否有己方棋子
        target_piece = board.get_piece(x, y)
        if target_piece and target_piece.color == self.color:
            return False
            
        return True

class Board:
    def __init__(self):
        self.pieces: List[Piece] = []
        self._initialize_board()

    def _initialize_board(self):
        # 初始化红方棋子
        red_pieces = [
            (PieceType.CHARIOT, 0, 9), (PieceType.HORSE, 1, 9),
            (PieceType.ELEPHANT, 2, 9), (PieceType.ADVISOR, 3, 9),
            (PieceType.KING, 4, 9), (PieceType.ADVISOR, 5, 9),
            (PieceType.ELEPHANT, 6, 9), (PieceType.HORSE, 7, 9),
            (PieceType.CHARIOT, 8, 9), (PieceType.CANNON, 1, 7),
            (PieceType.CANNON, 7, 7), (PieceType.PAWN, 0, 6),
            (PieceType.PAWN, 2, 6), (PieceType.PAWN, 4, 6),
            (PieceType.PAWN, 6, 6), (PieceType.PAWN, 8, 6)
        ]
        
        # 初始化黑方棋子
        black_pieces = [
            (PieceType.CHARIOT, 0, 0), (PieceType.HORSE, 1, 0),
            (PieceType.ELEPHANT, 2, 0), (PieceType.ADVISOR, 3, 0),
            (PieceType.KING, 4, 0), (PieceType.ADVISOR, 5, 0),
            (PieceType.ELEPHANT, 6, 0), (PieceType.HORSE, 7, 0),
            (PieceType.CHARIOT, 8, 0), (PieceType.CANNON, 1, 2),
            (PieceType.CANNON, 7, 2), (PieceType.PAWN, 0, 3),
            (PieceType.PAWN, 2, 3), (PieceType.PAWN, 4, 3),
            (PieceType.PAWN, 6, 3), (PieceType.PAWN, 8, 3)
        ]
        
        # 添加红方棋子
        for piece_type, x, y in red_pieces:
            self.pieces.append(Piece(piece_type, PieceColor.RED, x, y))
            
        # 添加黑方棋子
        for piece_type, x, y in black_pieces:
            self.pieces.append(Piece(piece_type, PieceColor.BLACK, x, y))

    def get_piece(self, x: int, y: int) -> Optional[Piece]:
        for piece in self.pieces:
            if piece.x == x and piece.y == y:
                return piece
        return None

    def move_piece(self, piece: Piece, new_x: int, new_y: int):
        # 移除目标位置的棋子（如果有）
        target_piece = self.get_piece(new_x, new_y)
        if target_piece:
            self.pieces.remove(target_piece)
            
        # 移动选中的棋子
        piece.x = new_x
        piece.y = new_y

    def get_ai_move(self) -> Tuple[Piece, int, int]:
        # 获取当前AI玩家的所有棋子
        ai_pieces = [piece for piece in self.pieces if piece.color == PieceColor.BLACK]
        if not ai_pieces:
            return None

        # 随机选择一个棋子
        piece = random.choice(ai_pieces)
        
        # 获取该棋子的所有有效移动
        valid_moves = piece.get_valid_moves(self)
        if not valid_moves:
            return None
            
        # 随机选择一个有效移动
        new_x, new_y = random.choice(valid_moves)
        return piece, new_x, new_y

    def make_ai_move(self):
        move = self.get_ai_move()
        if move:
            piece, new_x, new_y = move
            self.move_piece(piece, new_x, new_y)
            return True
        return False 