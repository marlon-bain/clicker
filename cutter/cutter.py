import mouse
import cut
import pan
import time
import config
import human_input

class CutLogs:
    def __init__(self):
        self.mouse = mouse.Mouse()
        self.exit = False
        self.current_stage = None
        self.stage_time = time.time()
        self.stage_limit = 300
        self.set_stage(cut.Cut(self))

    def on_image(self, img):
        if self.current_stage is None:
            return

        self.current_stage.on_image(img)

    def on_message(self, body):
        if "is now idle" in body or "log out from idling" in body:
            self.set_stage(cut.Cut(self))
            print("Setting stage to cut")
        elif "inventory" in body:
            self.exit = True
        else:
            if self.current_stage is None:
                return

            self.current_stage.on_message(body)

    def transition(self):
        return self.exit

    def set_stage(self, stage):
        self.current_stage = stage
        self.stage_time = time.time()
        self.stage_limit = human_input.sample_normal(
            config.MAX_NONE_TIME_S, config.MAX_NONE_TIME_S / 4
        )

    def act(self):
        stage_time_left = self.stage_limit - (time.time() - self.stage_time)
        if stage_time_left <= 0:
            print("Timing out stage")
            self.set_stage(cut.Cut(self))
            print("Setting stage to cut")
            return

        if self.current_stage is None:
            return

        self.current_stage.act()

        should_transition, should_pan, should_cut = self.current_stage.transition()
        if should_transition:
            if should_pan:
                self.set_stage(pan.Pan(self))
                print("Setting stage to pan")
            elif should_cut:
                self.set_stage(cut.Cut(self))
                print("Setting stage to cut")
            else:
                self.set_stage(None)
                print("Setting stage to none")

