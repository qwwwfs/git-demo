from .core import MockDriver, JOINTS, forward_kinematics


def main():
    driver = MockDriver()
    driver.command(JOINTS, [0.3, -0.2])
    print("SIMULATION ONLY — no CAN messages")
    for i in range(50):
        q = driver.step(0.02)
        if i % 10 == 0 or i == 49:
            x, y = forward_kinematics(*q)
            print(f"t={(i+1)*0.02:.2f}s q={q} tip=({x:.4f}, {y:.4f})m")


if __name__ == "__main__":
    main()
