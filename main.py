#!/bin/python3

import pygame
import time
import random
import copy

import settings
settings.init()
import tests
import gui




gui.calcSettings()

canvas = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]
network = []



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
    for l in range(settings.DEEP_LAYERS + 2):
        if l == 0:
            #create input layer
            network.append([])
            for n in range(settings.FIRST_LAYER_SIZE):
                network[0].append(Neuron())
        elif l == settings.DEEP_LAYERS + 1:
            #create output layer
            network.append([])
            for n in range(settings.LAST_LAYER_SIZE):
                network[-1].append(Neuron())
                for i in range(settings.DEEP_LAYER_SIZE):
                    network[-1][-1].input_mask.append(not bool(random.randint(settings.AXON_MIN, settings.AXON_MAX)))
                    network[-1][-1].activation_level = random.randint(1, settings.DEEP_LAYER_SIZE)
                    network[-1][-1].output_level = random.randint(
                        int(settings.DEEP_LAYER_SIZE * settings.OUTPUT_LEVEL_MIN), int(settings.DEEP_LAYER_SIZE * settings.OUTPUT_LEVEL_MAX))
        else:
            #create deep layers
            network.append([])
            for n in range(settings.DEEP_LAYER_SIZE):
                network[l].append(Neuron())
                #generate neuron's mask
                if len(network[l]) == 0:
                    for i in range(settings.FIRST_LAYER_SIZE):
                        network[l][-1].input_mask.append(not bool(random.randint(settings.AXON_MIN, settings.AXON_MAX)))
                        network[l][-1].activation_level = random.randint(1, settings.FIRST_LAYER_SIZE)
                        network[l][-1].output_level = random.randint(int(
                            settings.FIRST_LAYER_SIZE * settings.OUTPUT_LEVEL_MIN), int(settings.FIRST_LAYER_SIZE * settings.OUTPUT_LEVEL_MAX))
                else:
                    for i in range(settings.DEEP_LAYER_SIZE):
                        network[l][-1].input_mask.append(not bool(random.randint(settings.AXON_MIN, settings.AXON_MAX)))
                        network[l][-1].activation_level = random.randint(1, settings.DEEP_LAYER_SIZE)
                        network[l][-1].output_level = random.randint(
                            int(settings.DEEP_LAYER_SIZE * settings.OUTPUT_LEVEL_MIN), int(settings.DEEP_LAYER_SIZE * settings.OUTPUT_LEVEL_MAX))







def updateInput():
    for y in range(len(canvas)):
        for x in range(len(canvas[y])):
            network[0][y*len(canvas[y])+x].output = canvas[y][x]




def updateNetwork():
    for l in range(1, len(network)):
        prev_output = []
        for n in range(len(network[l-1])):
            prev_output.append(network[l-1][n].output)
        for n in range(len(network[l])):
            network[l][n].calculate(prev_output)




def randomCanvas():
    for y in range(len(canvas)):
        for x in range(len(canvas[y])):
            canvas[y][x] = random.randint(0, 1)




buildNetwork()
updateInput()
updateNetwork()
gui.disp(network, canvas, True)
while(True):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
        if e.type == pygame.VIDEORESIZE:
            settings.WIDTH = e.w
            settings.HIGHT = e.h
            gui.calcSettings()
            surface = pygame.display.set_mode((settings.WIDTH, settings.HIGHT), pygame.RESIZABLE)
            gui.disp(network, canvas, True)
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r:
                randomCanvas()
                updateInput()
                updateNetwork()
            if e.key == pygame.K_n:
                network = []
                buildNetwork()
                updateInput()
                updateNetwork()
                gui.disp(network, canvas, True)
            if e.key == pygame.K_0:
                canvas = copy.deepcopy(tests.shapes[0])
                updateInput()
                updateNetwork()
            if e.key == pygame.K_1:
                canvas = copy.deepcopy(tests.shapes[1])
                updateInput()
                updateNetwork()
            if e.key == pygame.K_2:
                canvas = copy.deepcopy(tests.shapes[2])
                updateInput()
                updateNetwork()
            if e.key == pygame.K_3:
                canvas = copy.deepcopy(tests.shapes[3])
                updateInput()
                updateNetwork()
            if e.key == pygame.K_4:
                canvas = copy.deepcopy(tests.shapes[4])
                updateInput()
                updateNetwork()
            if e.key == pygame.K_5:
                canvas = copy.deepcopy(tests.shapes[5])
                updateInput()
                updateNetwork()
            if e.key == pygame.K_6:
                canvas = copy.deepcopy(tests.shapes[6])
                updateInput()
                updateNetwork()
            if e.key == pygame.K_7:
                canvas = copy.deepcopy(tests.shapes[7])
                updateInput()
                updateNetwork()
            if e.key == pygame.K_8:
                canvas = copy.deepcopy(tests.shapes[8])
                updateInput()
                updateNetwork()
            if e.key == pygame.K_9:
                canvas = copy.deepcopy(tests.shapes[9])
                updateInput()
                updateNetwork()
    gui.disp(network, canvas)
    gui.clock.tick(settings.FPS)
