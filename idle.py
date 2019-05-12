import mouse

class Idle:
    def __init__(self):
        self.mouse = mouse.Mouse()
        pass

    def on_image(self, img):
        pass

    def on_message(self, body):
        pass

    def transition(self):
        return False

    def act(self):
        print(self.mouse.position())
        pass

