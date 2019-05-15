import random

import message_queue
import cv2 as cv
import mss
import numpy as np
import config

from depositor import depositor
from cutter import cutter
from walker import walker
from location_checker import LocationChecker

class Orchestrator:
    def __init__(self):
        self.debug = False
        self.debug_turns = 1000

        self.location = None
        self.invariants = [LocationChecker(self, config.BOTTOM_LEFT, config.TOP_RIGHT)]
        self.remediation_stage = None

        self.current_stage_index = 1
        self.stages = []

    def on_message(self, message):
        if config.LOCATION_TAG in message:
            index = message.index(config.LOCATION_TAG) + len(config.LOCATION_TAG)
            coordinates = message[index:].strip().split(",")
            coordinates = map(int, coordinates)

            self.location = (coordinates[0], coordinates[1])

    def add_looped_stages(self):
        number_of_loops = random.randrange(10, 15)
        print("Looping {0} times, yielding {1} logs".format(number_of_loops, number_of_loops * 28))

        for i in range(number_of_loops):
            self.stages.append(walker.BankWalker(self, reverse=True)),
            self.stages.append(cutter.CutLogs()),
            self.stages.append(walker.BankWalker(self)),
            self.stages.append(depositor.Depositor())

    def go(self):
        mq = message_queue.MessageQueue()
        mq.drain()

        self.add_looped_stages()
        with mss.mss() as sct:
            while True:
                if self.debug:
                    if self.debug_turns < 0:
                        exit()
                    self.debug_turns -= 1

                current_stage = self.stages[self.current_stage_index] if \
                    self.remediation_stage is None else \
                    self.remediation_stage

                # Pass messages to stage
                messages = mq.get_messages()
                for message in messages:
                    self.on_message(message)
                    current_stage.on_message(message)

                # Pass screen data to stage
                img = np.array(sct.grab(config.MONITOR))[:, :, :3]
                current_stage.on_image(img)

                # Execute stage logic
                current_stage.act()

                # Enforce invariants
                if self.remediation_stage is None:
                    for checker in self.invariants:
                        remediation = checker.remediate()

                        if remediation:
                            self.remediation_stage = remediation
                            continue

                if current_stage.transition():
                    if self.remediation_stage:
                        desired_resume_stage = self.remediation_stage.to_stage_index()
                        while (self.current_stage_index % 4) != desired_resume_stage:
                            print("Incrementing stage index since it isn't equal to {0} mod {1}: stage index is {2}"
                                  .format(desired_resume_stage, len(self.stages), self.current_stage_index + 1))
                            self.current_stage_index += 1
                            if self.current_stage_index == len(self.stages):
                                print("We ran out of stages while resuming from remediation")
                                exit(0)

                        self.remediation_stage = None
                    else:
                        self.current_stage_index = self.current_stage_index + 1
                        if self.current_stage_index == len(self.stages):
                            print("All stages complete")
                            exit(0)
                        print("[Root] Transitioning to the next stage at index {0}".format(self.current_stage_index))

                # Press "q" to quit
                if cv.waitKey(config.TURN_LENGTH_MS) & 0xFF == ord("q"):
                    cv.destroyAllWindows()
                    exit(0)


if __name__ == "__main__":
    Orchestrator().go()