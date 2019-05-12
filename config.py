# Part of the screen to capture
MONITOR = {"top": 40, "left": 0, "width": 800, "height": 640}

# Pixels from where you right click to where you click "bank"
DISTANCE_TO_BANK_OPTION = 40

TURN_LENGTH_MS = 10
SETTLING_LATENCY_S = 2
MAX_NONE_TIME_S = 60

MOUSE_SPEED_SCALE = 4.0

FOCUS_LENGTH_MEAN =  10 # 60 * 60 * 1000
FOCUS_LENGTH_STD = 3

# We don't want to spend more than one round panning
MAX_TURNS_PANNING = 1

# Set the maximum turns such that the longest hibernation is two minutes
MAX_TURNS_HIBERNATED = int(2 * 60 * 1000 / float(TURN_LENGTH_MS))

RABBITMQ_CHANNEL = 'YEWTEW'

# When toggled, the program does not perform any actual clicks
DEBUG_CLICK = False

# When toggled, the program only prints messages
DEBUG_MESSAGE_PRINT = True

LOCATION_TAG = "[LOCATION]"
SETTLED_TAG = "[SETTLED]"

MOUSE_VECTORS_FILENAME = "mouse_vectors.shart"
