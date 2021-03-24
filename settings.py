def init():
    global WIDTH, HIGHT, FPS
    global FIRST_LAYER_SIZE, DEEP_LAYERS, DEEP_LAYER_SIZE, LAST_LAYER_SIZE
    global AXON_MIN, AXON_MAX, OUTPUT_LEVEL_MIN, OUTPUT_LEVEL_MAX
    global NEURON_RADIUS, MARGIN
    global MUTATE_AXONS, AXON_MUTATION_RATE, MUTATE_NEURON_OUTPUT, OUTPUT_MUTATION_RATE, MUTATE_NEURON_ACTIVATION, ACTIVATION_MUTATION_RATE
    global GENERATION_SIZE, GENERATIONS, SELECTION_SIZE


    #window settings
    WIDTH = 1000
    HIGHT = 1000
    FPS = 30

    #neural network settings
    FIRST_LAYER_SIZE = 25
    DEEP_LAYERS = 4
    DEEP_LAYER_SIZE = 30
    LAST_LAYER_SIZE = 10

    #first generation settings
    AXON_MIN = 0
    AXON_MAX = 10
    OUTPUT_LEVEL_MIN = 0#-0.25  # actually it's LAYER_SIZE * OUTPUT_LEVEL_MIN
    OUTPUT_LEVEL_MAX = 0.25   # and this is LAYER_SIZE * OUTPUT_LEVEL_MAX

    #gui settings
    NEURON_RADIUS = 10
    MARGIN = 100

    #mutation settings
    MUTATE_AXONS = True
    AXON_MUTATION_RATE = 10

    MUTATE_NEURON_OUTPUT = True
    OUTPUT_MUTATION_RATE = 10

    MUTATE_NEURON_ACTIVATION = True
    ACTIVATION_MUTATION_RATE = 10

    #generation settings
    GENERATION_SIZE = 10
    GENERATIONS = 20
    SELECTION_SIZE = 2

