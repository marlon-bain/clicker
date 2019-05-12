import random

import message_queue
import cv2 as cv
import mss
import numpy as np
import config

from depositor import depositor
from cutter import cutter
from walker import walker

mq = message_queue.MessageQueue()
stages = [
    # Idle(),
    walker.BankWalker(reverse=True),
    cutter.CutLogs(),
    walker.BankWalker(),
    depositor.Depositor(),
]
current_stage_index = 1

debug = False
debug_turns = 1000
if __name__ == "__main__":
    mq.drain()

    number_of_loops = random.randrange(10, 15)
    print("Looping {0} times".format(number_of_loops + 1))

    while number_of_loops > 0:
        stages.append(walker.BankWalker(reverse=True)),
        stages.append(cutter.CutLogs()),
        stages.append(walker.BankWalker()),
        stages.append(depositor.Depositor())
        number_of_loops -= 1

    with mss.mss() as sct:
        while True:
            if debug:
                if debug_turns < 0:
                    exit()
                debug_turns -= 1

            current_stage = stages[current_stage_index]

            # Pass messages to stage
            messages = mq.get_messages()
            for message in messages:
                current_stage.on_message(message)

            # Pass screen data to stage
            img = np.array(sct.grab(config.MONITOR))[:, :, :3]
            processed = current_stage.on_image(img)

            # Execute stage logic
            current_stage.act()

            if current_stage.transition():
                current_stage_index = (current_stage_index + 1) % len(stages)
                print("[Root] Transitioning to the next stage at index {0}".format(current_stage_index))
                if current_stage_index == len(stages):
                    print("All stages complete")
                    exit(0)

            # Press "q" to quit
            if cv.waitKey(config.TURN_LENGTH_MS) & 0xFF == ord("q"):
                cv.destroyAllWindows()
                exit(0)