#!/bin/python3

import pygame
import time
import random
import copy

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
def calcSettings():
    global HSPACE, FIRST_VSPACE, DEEP_VSPACE, LAST_VSPACE
    HSPACE = int((WIDTH - MARGIN*2) / (DEEP_LAYERS + 1))
    FIRST_VSPACE = int((HIGHT - MARGIN*4) / FIRST_LAYER_SIZE+2)
    DEEP_VSPACE = int((HIGHT - MARGIN*2) / DEEP_LAYER_SIZE)
    LAST_VSPACE = int((HIGHT - MARGIN*2) / LAST_LAYER_SIZE)

calcSettings()

network = []

pygame.init()
surface = pygame.display.set_mode((WIDTH, HIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()

class Neuron:
    def __init__(self):
        self.input_mask = []
        self.activation_level = 1
        self.output_level = 1
        self.low_level = 0
        self.output = 0

    def calculate(self, inputs):
        activation_sum = 0
        for input, mask in zip(inputs, self.input_mask):
            activation_sum += input * mask
        if activation_sum >= self.activation_level:
            self.output = self.output_level
        else:
            self.output = self.low_level




def buildNetwork():
    for l in range(DEEP_LAYERS + 2):
        if l == 0:
            #create input layer
            network.append([])
            for n in range(FIRST_LAYER_SIZE):
                network[0].append(Neuron())
        elif l == DEEP_LAYERS + 1:
            #create output layer
            network.append([])
            for n in range(LAST_LAYER_SIZE):
                network[-1].append(Neuron())
                for i in range(DEEP_LAYER_SIZE):
                    network[-1][-1].input_mask.append(not bool(random.randint(AXON_MIN, AXON_MAX)))
                    network[-1][-1].activation_level = random.randint(1, DEEP_LAYER_SIZE)
                    network[-1][-1].output_level = random.randint(
                        int(DEEP_LAYER_SIZE * OUTPUT_LEVEL_MIN), int(DEEP_LAYER_SIZE * OUTPUT_LEVEL_MAX))
        else:
            #create deep layers
            network.append([])
            for n in range(DEEP_LAYER_SIZE):
                network[l].append(Neuron())
                #generate neuron's mask
                if len(network[l]) == 0:
                    for i in range(FIRST_LAYER_SIZE):
                        network[l][-1].input_mask.append(not bool(random.randint(AXON_MIN, AXON_MAX)))
                        network[l][-1].activation_level = random.randint(1, FIRST_LAYER_SIZE)
                        network[l][-1].output_level = random.randint(int(
                            FIRST_LAYER_SIZE * OUTPUT_LEVEL_MIN), int(FIRST_LAYER_SIZE * OUTPUT_LEVEL_MAX))
                else:
                    for i in range(DEEP_LAYER_SIZE):
                        network[l][-1].input_mask.append(not bool(random.randint(AXON_MIN, AXON_MAX)))
                        network[l][-1].activation_level = random.randint(1, DEEP_LAYER_SIZE)
                        network[l][-1].output_level = random.randint(
                            int(DEEP_LAYER_SIZE * OUTPUT_LEVEL_MIN), int(DEEP_LAYER_SIZE * OUTPUT_LEVEL_MAX))





def neuronPos(l, n):
    x = 0
    y = 0
    if l == 0:
        x = MARGIN
        y = MARGIN + n * FIRST_VSPACE
    if l > 0 and l <= DEEP_LAYERS:
        x = MARGIN + (l) * HSPACE
        y = MARGIN + n * DEEP_VSPACE
    if l == DEEP_LAYERS + 1:
        x = WIDTH - MARGIN
        y = MARGIN + n * LAST_VSPACE
    return (x, y)


def disp(all = False):
    if all == True:
        surface.fill((0, 0, 0))
        #show connections

        for l in range(DEEP_LAYERS+2):
            if l == 1 and l <= DEEP_LAYERS:
                for n in range(DEEP_LAYER_SIZE):
                    for i in range(FIRST_LAYER_SIZE):
                        if network[l][n].input_mask[i] != 0:
                            pygame.draw.line(surface, (255, 255, 255), neuronPos(l, n), neuronPos(l-1, i))
            if l > 1 and l <= DEEP_LAYERS:
                for n in range(DEEP_LAYER_SIZE):
                    for i in range(DEEP_LAYER_SIZE):
                        if network[l][n].input_mask[i] != 0:
                            pygame.draw.line(surface, (255, 255, 255), neuronPos(l, n), neuronPos(l-1, i))
            if l == DEEP_LAYERS+1:
                for n in range(LAST_LAYER_SIZE):
                    for i in range(DEEP_LAYER_SIZE):
                        if network[l][n].input_mask[i] != 0:
                            pygame.draw.line(surface, (255, 255, 255), neuronPos(l, n), neuronPos(l-1, i))

    #show neurons
    for l in range(DEEP_LAYERS+2):
        for n in range(len(network[l])):
            pygame.draw.circle(surface, (0, 255, 0) if network[l][n].output==network[l][n].output_level else (255, 0, 0), neuronPos(l, n), NEURON_RADIUS)
    pygame.display.update()




buildNetwork()
disp(True)
while(True):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
        if e.type == pygame.VIDEORESIZE:
            WIDTH = e.w
            HIGHT = e.h
            calcSettings()
            surface = pygame.display.set_mode((WIDTH, HIGHT), pygame.RESIZABLE)
            disp(True)
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r:
                for n in range(len(network[0])):
                    network[0][n].output = random.getrandbits(1)
                for l in range(1, len(network)):
                    prev_output = []
                    for n in range(len(network[l-1])):
                        prev_output.append(network[l-1][n].output)
                    for n in range(len(network[l])):
                        network[l][n].calculate(prev_output)
            if e.key == pygame.K_n:
                network = []
                buildNetwork()
                disp(True)
    disp()
    clock.tick(FPS)
