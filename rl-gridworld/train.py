"""在同一个悬崖环境中训练并比较 SARSA 和 Q-learning。"""

import argparse
from collections import defaultdict
from random import Random
from statistics import mean

from gridworld import ARROWS, CLIFF, COLS, GOAL, MOVES, ROWS, START, step

ALPHA = 0.5
GAMMA = 0.99
MAX_STEPS = 500


def choose_action(values, epsilon, rng):
    if epsilon > 0 and rng.random() < epsilon:
        return rng.randrange(len(values))
    best_value = max(values)
    # 并列最大时随机选，避免初始 Q 全为零时总挑同一个方向。
    return rng.choice([i for i, value in enumerate(values) if value == best_value])


def train(algorithm, episodes, epsilon, seed):
    rng = Random(seed)
    q = defaultdict(lambda: [0.0] * len(MOVES))
    returns = []
    for _ in range(episodes):
        state = START
        action = choose_action(q[state], epsilon, rng)
        total_reward = 0
        for _ in range(MAX_STEPS):
            next_state, reward, done = step(state, action)
            total_reward += reward
            target = reward
            if not done:
                next_action = choose_action(q[next_state], epsilon, rng)
                # 两种算法都用 ε-贪婪行动，差别在更新目标取哪个值。
                if algorithm == "sarsa":
                    next_value = q[next_state][next_action]
                else:
                    next_value = max(q[next_state])
                target += GAMMA * next_value

            q[state][action] += ALPHA * (target - q[state][action])
            if done:
                break
            state, action = next_state, next_action

        returns.append(total_reward)
    return q, returns


def evaluate(q, epsilon, seed, episodes=100):
    rng = Random(seed)
    returns = []
    reached_goal = 0
    falls = 0
    for _ in range(episodes):
        state = START
        total_reward = 0
        for _ in range(MAX_STEPS):
            action = choose_action(q[state], epsilon, rng)
            state, reward, done = step(state, action)
            total_reward += reward
            falls += reward == -100
            if done:
                reached_goal += 1
                break
        returns.append(total_reward)
    return mean(returns), reached_goal / episodes, falls


def print_policy(q):
    markers = {START: "S", GOAL: "G", **dict.fromkeys(CLIFF, "X")}
    for row in range(ROWS):
        cells = []
        for col in range(COLS):
            state = (row, col)
            if state in markers:
                cells.append(markers[state])
            elif state in q and any(q[state]):
                values = q[state]
                cells.append(ARROWS[values.index(max(values))])
            else:
                cells.append("·")
        print(" ".join(cells))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--algorithm", choices=("sarsa", "q-learning", "both"), default="both")
    parser.add_argument("--episodes", type=int, default=3000)
    parser.add_argument("--epsilon", type=float, default=0.1, help="训练时的随机探索概率")
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()
    if args.episodes < 1:
        parser.error("--episodes 必须至少为 1")
    if not 0 <= args.epsilon <= 1:
        parser.error("--epsilon 必须在 0 和 1 之间")

    algorithms = ("sarsa", "q-learning") if args.algorithm == "both" else (args.algorithm,)
    window = min(100, args.episodes)
    for algorithm in algorithms:
        q, returns = train(algorithm, args.episodes, args.epsilon, args.seed)
        print(f"\n{algorithm.upper()}")
        print(f"训练前 {window} 回合平均回报 {mean(returns[:window]):.1f}")
        print(f"训练后 {window} 回合平均回报 {mean(returns[-window:]):.1f}")
        print_policy(q)
        for label, epsilon in (("贪婪评估", 0.0), ("带探索评估", args.epsilon)):
            avg_return, success_rate, falls = evaluate(q, epsilon, args.seed + 1)
            print(f"{label} 100 回合  平均回报 {avg_return:.1f}  到达率 {success_rate:.0%}  掉崖 {falls} 次")


if __name__ == "__main__":
    main()
