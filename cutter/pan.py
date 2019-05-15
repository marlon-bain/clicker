class Pan:
    def __init__(self, parent):
        self.parent = parent

    def on_image(self, img):
        pass

    def on_message(self, message):
        pass

    def act(self):
        self.parent.mouse.pan()

    def transition(self):
        return True, False, True