import pickle
import config
from pynput.mouse import Listener

is_clicked = False
current_path = []
normalized_path = []

def normalize():
    global min_x, max_x, min_y, max_y
    first_index = 0
    last_index = len(current_path) - 1

    if last_index <= first_index:
        return

    min_x = float(current_path[first_index][0])
    min_y = float(current_path[first_index][1])
    max_x = float(current_path[last_index][0])
    max_y = float(current_path[last_index][1])
    x_extent = float(current_path[first_index][0] - current_path[last_index][0])
    y_extent = float(current_path[first_index][1] - current_path[last_index][1])

    for i in range(len(current_path)):
        normalized_x = -(current_path[i][0] - min_x) / x_extent
        normalized_y = -(current_path[i][1] - min_y) / y_extent
        normalized_path.append((normalized_x, normalized_y))

def on_move(x, y):
    global is_clicked
    if is_clicked:
        current_path.append((x, y))

def on_click(x, y, button, pressed):
    global is_clicked
    is_clicked = pressed
    if not pressed:
        return False

def reset():
    global is_clicked, current_path, normalized_path
    is_clicked = False
    current_path = []
    normalized_path = []


if __name__ == '__main__':
    print("To record a mouse vector, just drag your mouse and release it to save. To stop, click once in place.")

    paths = []
    while True:
        with Listener(
                on_move=on_move,
                on_click=on_click) as listener:
            listener.join()

        normalize()
        if len(normalized_path) > 0:
            print("Saving path.")
            paths.append(normalized_path)
            reset()
        else:
            break

    if len(paths) >= 3:
        print("Saving all paths")
        pickle.dump(paths, open(config.MOUSE_VECTORS_FILENAME, "wb"))
    else:
        print("Record at least 3 vectors before we save")