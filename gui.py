import pygame
import settings

pygame.init()
surface = pygame.display.set_mode(
    (settings.WIDTH, settings.HIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()



def calcSettings():
    settings.HSPACE = int(
        (settings.WIDTH - settings.MARGIN*2) / (settings.DEEP_LAYERS + 1))
    settings.FIRST_VSPACE = int(
        (settings.HIGHT - settings.MARGIN*4) / settings.FIRST_LAYER_SIZE+2)
    settings.DEEP_VSPACE = int(
        (settings.HIGHT - settings.MARGIN*2) / settings.DEEP_LAYER_SIZE)
    settings.LAST_VSPACE = int(
        (settings.HIGHT - settings.MARGIN*2) / settings.LAST_LAYER_SIZE)



def neuronPos(l, n):
    x = 0
    y = 0
    if l == 0:
        x = settings.MARGIN
        y = settings.MARGIN + n * settings.FIRST_VSPACE
    if l > 0 and l <= settings.DEEP_LAYERS:
        x = settings.MARGIN + (l) * settings.HSPACE
        y = settings.MARGIN + n * settings.DEEP_VSPACE
    if l == settings.DEEP_LAYERS + 1:
        x = settings.WIDTH - settings.MARGIN
        y = settings.MARGIN + n * settings.LAST_VSPACE
    return (x, y)



def disp(network, canvas, all=False):
    if all == True:
        surface.fill((0, 0, 0))
        #show connections

        for l in range(settings.DEEP_LAYERS+2):
            if l == 1 and l <= settings.DEEP_LAYERS:
                for n in range(settings.DEEP_LAYER_SIZE):
                    for i in range(settings.FIRST_LAYER_SIZE):
                        if network[l][n].input_mask[i] != 0:
                            pygame.draw.line(surface, (255, 255, 255), neuronPos(
                                l, n), neuronPos(l-1, i))
            if l > 1 and l <= settings.DEEP_LAYERS:
                for n in range(settings.DEEP_LAYER_SIZE):
                    for i in range(settings.DEEP_LAYER_SIZE):
                        if network[l][n].input_mask[i] != 0:
                            pygame.draw.line(surface, (255, 255, 255), neuronPos(
                                l, n), neuronPos(l-1, i))
            if l == settings.DEEP_LAYERS+1:
                for n in range(settings.LAST_LAYER_SIZE):
                    for i in range(settings.DEEP_LAYER_SIZE):
                        if network[l][n].input_mask[i] != 0:
                            pygame.draw.line(surface, (255, 255, 255), neuronPos(
                                l, n), neuronPos(l-1, i))

    #show neurons
    for l in range(settings.DEEP_LAYERS+2):
        for n in range(len(network[l])):
            pygame.draw.circle(surface, (0, 255, 0) if network[l][n].output == network[l][n].output_level else (
                255, 0, 0), neuronPos(l, n), settings.NEURON_RADIUS)

    #show canvas
    for y in range(len(canvas)):
        for x in range(len(canvas[y])):
            if canvas[y][x]:
                pygame.draw.rect(surface, (255, 255, 255),
                                 (x * 10, y*10, 10, 10))
            else:
                pygame.draw.rect(surface, (0, 0, 0), (x * 10, y*10, 10, 10))

    pygame.display.update()
