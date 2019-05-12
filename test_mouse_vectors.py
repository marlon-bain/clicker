import config
import mouse
import pickle
import time

if __name__ == '__main__':
    print("Loading vectors")
    mouse_paths = pickle.load(open(config.MOUSE_VECTORS_FILENAME, "rb"))
    if len(mouse_paths) < 3:
        print("Record some mouse paths first")
        exit(0)
    print("Done.")

    m = mouse.Mouse()
    for mouse_path in mouse_paths:
        m.move_using_path(mouse_path, (0, 0), (800, 800))
        time.sleep(0.5)
