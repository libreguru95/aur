import curses
import random
import time

def main(stdscr):
    # Очищаем экран
    curses.curs_set(0)
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Создаем список для хранения позиций капель
    drops = [random.randint(0, width - 20) for _ in range(100)]
    symbols = ['@', '#', '$', '%', '&', '*', '+', '=', '-', '~', '!', '?']

    while True:
        stdscr.clear()
        for drop in drops:
            # Генерируем случайную высоту для каждой капли
            y = random.randint(0, height - 1)
            symbol = random.choice(symbols)  # Выбираем случайный символ
            
            # Проверяем, чтобы координаты были в пределах экрана
            if 0 <= y < height and 0 <= drop < width:
                stdscr.addstr(y, drop, symbol)
        
        stdscr.refresh()
        time.sleep(0.1)

if __name__ == "__main__":
    curses.wrapper(main)
