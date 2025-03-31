import pygame
import sys
import time
from game import Board, PieceColor, PieceType

# 初始化Pygame
pygame.init()

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 设置游戏窗口
WINDOW_SIZE = (800, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("中国象棋")

# 定义棋盘尺寸
BOARD_WIDTH = 9  # 9列
BOARD_HEIGHT = 10  # 10行
CELL_SIZE = 60
BOARD_OFFSET_X = (WINDOW_SIZE[0] - (BOARD_WIDTH - 1) * CELL_SIZE) // 2
BOARD_OFFSET_Y = (WINDOW_SIZE[1] - (BOARD_HEIGHT - 1) * CELL_SIZE) // 2

# 创建游戏板
board = Board()
selected_piece = None
current_player = PieceColor.RED
ai_thinking = False
game_over = False

# 加载中文字体
try:
    font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 36)  # 使用黑体
except:
    font = pygame.font.Font(None, 36)  # 如果找不到中文字体，使用默认字体

def draw_board():
    # 绘制棋盘背景
    screen.fill(WHITE)
    
    # 绘制横线
    for i in range(BOARD_HEIGHT):
        y = BOARD_OFFSET_Y + i * CELL_SIZE
        pygame.draw.line(screen, BLACK, 
                        (BOARD_OFFSET_X, y),
                        (BOARD_OFFSET_X + (BOARD_WIDTH - 1) * CELL_SIZE, y))
    
    # 绘制竖线
    for i in range(BOARD_WIDTH):
        x = BOARD_OFFSET_X + i * CELL_SIZE
        pygame.draw.line(screen, BLACK,
                        (x, BOARD_OFFSET_Y),
                        (x, BOARD_OFFSET_Y + (BOARD_HEIGHT - 1) * CELL_SIZE))
    
    # 绘制楚河汉界
    text = font.render("楚 河", True, BLACK)
    screen.blit(text, (WINDOW_SIZE[0]//2 - 60, WINDOW_SIZE[1]//2))
    text = font.render("汉 界", True, BLACK)
    screen.blit(text, (WINDOW_SIZE[0]//2 + 20, WINDOW_SIZE[1]//2))
    
    # 绘制棋子
    for piece in board.pieces:
        x = BOARD_OFFSET_X + piece.x * CELL_SIZE
        y = BOARD_OFFSET_Y + piece.y * CELL_SIZE
        
        # 绘制棋子背景
        color = RED if piece.color == PieceColor.RED else BLACK
        pygame.draw.circle(screen, color, (x, y), CELL_SIZE // 2 - 5)
        
        # 绘制棋子文字
        text = font.render(piece.type.value, True, WHITE)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)
        
        # 如果棋子被选中，绘制高亮效果
        if piece == selected_piece:
            pygame.draw.circle(screen, GREEN, (x, y), CELL_SIZE // 2 - 2, 2)
            
        # 绘制可移动位置
        if piece == selected_piece:
            valid_moves = piece.get_valid_moves(board)
            for move_x, move_y in valid_moves:
                move_screen_x = BOARD_OFFSET_X + move_x * CELL_SIZE
                move_screen_y = BOARD_OFFSET_Y + move_y * CELL_SIZE
                pygame.draw.circle(screen, GREEN, (move_screen_x, move_screen_y), 5)
    
    # 显示当前玩家和游戏状态
    if game_over:
        winner = "红方胜利！" if current_player == PieceColor.BLACK else "黑方胜利！"
        text = font.render(winner, True, RED)
    else:
        current_text = "红方回合" if current_player == PieceColor.RED else "黑方回合"
        text = font.render(current_text, True, BLACK)
    screen.blit(text, (10, 10))
    
    # 如果AI正在思考，显示提示
    if ai_thinking:
        text = font.render("AI思考中...", True, BLACK)
        screen.blit(text, (WINDOW_SIZE[0] - 150, 10))

def get_board_position(screen_pos):
    x, y = screen_pos
    board_x = round((x - BOARD_OFFSET_X) / CELL_SIZE)
    board_y = round((y - BOARD_OFFSET_Y) / CELL_SIZE)
    return board_x, board_y

def check_game_over():
    # 检查是否还有将/帅
    red_king = False
    black_king = False
    for piece in board.pieces:
        if piece.type == PieceType.KING:
            if piece.color == PieceColor.RED:
                red_king = True
            else:
                black_king = True
    
    if not red_king:
        return True, PieceColor.BLACK
    if not black_king:
        return True, PieceColor.RED
    return False, None

def main():
    global selected_piece, current_player, ai_thinking, game_over
    clock = pygame.time.Clock()
    running = True
    last_ai_move_time = 0
    
    while running:
        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and current_player == PieceColor.RED and not game_over:  # 只在红方回合响应点击
                    board_x, board_y = get_board_position(event.pos)
                    if 0 <= board_x < BOARD_WIDTH and 0 <= board_y < BOARD_HEIGHT:
                        clicked_piece = board.get_piece(board_x, board_y)
                        
                        if selected_piece is None:
                            # 选择棋子
                            if clicked_piece and clicked_piece.color == current_player:
                                selected_piece = clicked_piece
                        else:
                            # 移动棋子
                            valid_moves = selected_piece.get_valid_moves(board)
                            if (board_x, board_y) in valid_moves:
                                board.move_piece(selected_piece, board_x, board_y)
                                current_player = PieceColor.BLACK
                                ai_thinking = True
                                last_ai_move_time = current_time
                            selected_piece = None
        
        # AI移动
        if current_player == PieceColor.BLACK and not game_over and current_time - last_ai_move_time > 1.0:
            if board.make_ai_move():
                current_player = PieceColor.RED
                ai_thinking = False
        
        # 检查游戏是否结束
        is_over, winner = check_game_over()
        if is_over:
            game_over = True
            current_player = winner
        
        draw_board()
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 