#!/bin/python3

import pygame
import time
import random
import copy
import json

import settings
settings.init()
import tests
import gui




class Node:
    def __init__(self):
        self.output_level = 1
        self.low_level = 0
        self.output = 0


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
                network[0].append(Node())
        elif l == settings.DEEP_LAYERS + 1:
            #create output layer
            network.append([])
            for n in range(settings.LAST_LAYER_SIZE):
                network[-1].append(Neuron())
                for i in range(settings.DEEP_LAYER_SIZE):
                    network[-1][-1].input_mask.append(0)#(not bool(random.randint(settings.AXON_MIN, settings.AXON_MAX)))
                    #network[-1][-1].activation_level = random.randint(1, settings.DEEP_LAYER_SIZE)
                    #network[-1][-1].output_level = 1
        else:
            #create deep layers
            network.append([])
            for n in range(settings.DEEP_LAYER_SIZE):
                network[l].append(Neuron())
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



def mutate(network_input):
    network = copy.deepcopy(network_input)
    for l in range(1, len(network)):
        for n in range(len(network[l])):
            if settings.MUTATE_AXONS:
                for i in range(len(network[l-1])):
                    if not bool(random.randint(0, settings.AXON_MUTATION_RATE)):
                        network[l][n].input_mask[i] = random.randint(settings.AXON_MIN, settings.AXON_MAX)
            if settings.MUTATE_NEURON_OUTPUT and not bool(random.randint(0, settings.OUTPUT_MUTATION_RATE)) and l < len(network):
                network[l][n].output_level = random.randint(
                    int(settings.DEEP_LAYER_SIZE * settings.OUTPUT_LEVEL_MIN), int(settings.DEEP_LAYER_SIZE * settings.OUTPUT_LEVEL_MAX))
            if settings.MUTATE_NEURON_ACTIVATION and not bool(random.randint(0, settings.ACTIVATION_MUTATION_RATE)):
                network[l][n].activation_level = random.randint(1, settings.DEEP_LAYER_SIZE)
    return network



def train():
    rivals = []
    global network, canvas
    for i in range(settings.GENERATION_SIZE):
        rivals.append([copy.deepcopy(network), 0])


    for g in range(1, settings.GENERATIONS):
        #print best accuracy
        tst = rivals[0][1]
        for test in rivals:
            if test[1] > tst:
                tst = test[1]
        print(f"generation: {g}, best accuracy: {tst}")
        ###################
        random.shuffle(rivals)
        tmp_rivals = []
        for selection in range(settings.SELECTION_SIZE):
            best_acc = 0
            for best in range(len(rivals)):
                if rivals[best][1] > rivals[best_acc][1]:
                    best_acc = best
            tmp_rivals.append(rivals.pop(best_acc))
            tmp_rivals[-1][1] = 0
        while len(tmp_rivals) < settings.GENERATION_SIZE:
            for selection in range(settings.SELECTION_SIZE):
                if len(tmp_rivals) < settings.GENERATION_SIZE:
                    tmp_rivals.append([mutate(tmp_rivals[selection][0]), 0])
                else:
                    break
        rivals = copy.deepcopy(tmp_rivals)


        for rival in rivals:
            network = copy.deepcopy(rival[0])
            for shape in range(10):
                canvas = copy.deepcopy(tests.shapes[shape])
                updateInput()
                updateNetwork()
                #gui.disp(network, canvas, True)

                for out in range(10):
                    if shape == out:
                        if network[-1][out].output:
                            rival[1] += 10  # activation on right output node
                        else:
                            rival[1] -= 1  # no activation on right output node
                    else:
                        if not bool(network[-1][out].output):
                            rival[1] += 1  # no activation on wrong output node
                        else:
                            rival[1] -= 3  # activation on wrong output node
    network = copy.deepcopy(rivals[0][0])
    gui.disp(network, canvas, True)
            



gui.calcSettings()


canvas = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

network = []

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
            if e.key == pygame.K_m:
                network = mutate(network)
                updateNetwork()
                gui.disp(network, canvas, True)
            if e.key == pygame.K_t:
                train()
            if e.key == pygame.K_s:
                with open("save.json", "w") as file:
                    json.dump(network, file)
            if e.key == pygame.K_l:
                with open("save.json") as file:
                    network = json.load(file)
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
