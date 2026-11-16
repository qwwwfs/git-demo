"""4×12 悬崖网格环境。坐标从左上角 (0, 0) 开始。"""

ROWS, COLS = 4, 12
START = (3, 0)
GOAL = (3, 11)
CLIFF = {(3, col) for col in range(1, 11)}
MOVES = ((-1, 0), (0, 1), (1, 0), (0, -1))
ARROWS = ("↑", "→", "↓", "←")


def step(state, action):
    """执行一步，返回 (下一状态, 奖励, 是否到达终点)。"""
    row, col = state
    dr, dc = MOVES[action]
    next_state = (
        min(max(row + dr, 0), ROWS - 1),
        min(max(col + dc, 0), COLS - 1),
    )
    if next_state in CLIFF:
        return START, -100, False
    return next_state, -1, next_state == GOAL
