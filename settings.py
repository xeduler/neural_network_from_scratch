def init():
    global WIDTH, HIGHT, FPS
    global FIRST_LAYER_SIZE, DEEP_LAYERS, DEEP_LAYER_SIZE, LAST_LAYER_SIZE
    global AXON_MIN, AXON_MAX, OUTPUT_LEVEL_MIN, OUTPUT_LEVEL_MAX
    global NEURON_RADIUS, MARGIN

    #window settings
    WIDTH = 1000
    HIGHT = 1000
    FPS = 30

    #neural network settings
    FIRST_LAYER_SIZE = 25
    DEEP_LAYERS = 4
    DEEP_LAYER_SIZE = 30
    LAST_LAYER_SIZE = 10

    AXON_MIN = 0
    AXON_MAX = 4
    OUTPUT_LEVEL_MIN = -0.25  # actually it's LAYER_SIZE * OUTPUT_LEVEL_MIN
    OUTPUT_LEVEL_MAX = 0.25   # and this is LAYER_SIZE * OUTPUT_LEVEL_MAX

    #gui settings
    NEURON_RADIUS = 10
    MARGIN = 100
