import pygame as pg
import sys
import random
import time
import easygui
from Algorithm import *

'''# global options ##############################'''

'''# graph sizes #####'''
WIDTH = HEIGHT = 720
FPS = 60
R = 20  # vertex radius
D = 2 * R
EDGE_WIDTH = 2  # edge width
FILE = open("graphs/graph.txt")
vertexCount = 0
isDeveloping = "the button is in Dev now. It will be ready in soon."

'''# graph structure #####'''
graphMatrix = []
vertexConnections = {}  # v1 : v2, v3 ...
vertexLocations = {}  # v : loc
allVertexLocations = []  # loc1, loc2 ...
FILE_LOADED = False

'''# graph colors #####'''
BG_COLOR = pg.Color(200, 200, 200)
VERTEX_COLOR = pg.Color(100, 100, 250)
EDGE_COLOR = pg.Color(0, 0, 0)
VERTEX_VISITED_COLOR = pg.Color(250, 250, 50)
EDGE_DELETED_COLOR = BG_COLOR

'''# algorithm structure #####'''
runAlgorithm = False
finishAlgo = False
dfsPath = []
vertexes = []
edges = []
graph = Graph(1)

'''# GRAPH LOAD ##############################'''


def graphLoad():
    global graphMatrix, vertexConnections
    global vertexCount, graph
    global FILE_LOADED
    FILE_LOADED = True
    file = FILE
    graphMatrix = []
    cols, rows = list(map(int, file.readline().split()))
    vertexCount = cols  # cols == rows
    for i in range(0, rows):  # [0; rows-1]
        graphMatrix.append(list(map(int, file.readline().split()[:cols])))

    graph = Graph(vertexCount)
    matchingVertex(cols, rows)
    placingVertex()


def matchingVertex(cols, rows):
    global vertexConnections
    for c in range(cols):
        vertexConnections[c + 1] = []

    for c in range(cols):
        for r in range(rows):
            if graphMatrix[c][r] != 0:
                vertexConnections[c + 1].append(r + 1)
                graph.addOneEdge(c, r)


def regenGraph():
    for c in range(vertexCount):
        for r in range(vertexCount):
            if graphMatrix[c][r] != 0:
                graph.addOneEdge(c, r)


def placingVertex():
    global vertexLocations, allVertexLocations
    vertexLocations = {}
    allVertexLocations = []
    for c in range(vertexCount):
        vertexLocations[c + 1] = random.randint(0 + D, WIDTH - D), random.randint(0 + D, HEIGHT - D)
    for key, value in vertexLocations.items():
        allVertexLocations.append(vertexLocations[key])


'''# find start ##############################'''


def findStart():
    oddCnt = 0
    startVertex = finishVertex = 0
    for key, value in vertexLocations.items():
        if len(vertexConnections[key]) % 2 == 1:
            oddCnt += 1
        if len(vertexConnections[key]) % 2 == 1 and oddCnt == 1:
            startVertex = key
        if len(vertexConnections[key]) % 2 == 1 and oddCnt == 2:
            finishVertex = key

    return oddCnt, startVertex, finishVertex


'''# GRAPH BUILD ##############################'''


def graphBuilder():
    global runAlgorithm, vertexes, edges, dfsPath, finishAlgo
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BG_COLOR)
    pg.display.set_caption("graph builder")
    pg.display.update()
    clock = pg.time.Clock()

    txt_font = pg.font.SysFont("menu_font", 32)
    txt_colors = [(10, 10, 10), (50, 250, 250), (250, 160, 0)]

    relocation()
    numStep = 0
    numVert = 0
    numEdge = 0
    selectedVertex = None
    runAlgorithm = False
    finishAlgo = False

    run = True
    while run:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    run = False
                if e.key == pg.K_r:
                    screen.fill(BG_COLOR)
                    numStep = 0
                    numVert = 0
                    numEdge = 0
                    selectedVertex = None
                    runAlgorithm = False
                    finishAlgo = False
                    relocation()

            elif e.type == pg.MOUSEBUTTONDOWN:
                mx, my = pg.mouse.get_pos()
                loc = [mx, my]
                if e.button == 1:

                    for v in allVertexLocations:
                        if v[0] - D <= loc[0] <= v[0] + D and v[1] - D <= loc[1] <= v[1] + D:
                            if finishAlgo:
                                numStep = 0
                                numVert = 0
                                numEdge = 0
                                selectedVertex = None
                                runAlgorithm = False
                                finishAlgo = False
                                graph.path = []
                                dfsPath = []
                                vertexes = []
                                edges = []

                            loc = v
                            oddCount, sv, fv = findStart()
                            print(oddCount)
                            if oddCount > 2:
                                print("There are no Euler Path")
                                finishAlgo = True
                                dfsPath = "[absent]"
                                break
                            elif oddCount == 0:
                                print("There are Euler Tour!")
                                graph.printEulerTour()
                                dfsPath = graph.path
                                regenGraph()
                                finishAlgo = True
                                break
                            elif oddCount == 1:
                                sv, fv = sv + fv, -1
                            elif oddCount == 2:
                                pass
                            if loc == vertexLocations[sv]:  # or
                                graph.printEulerTour()
                                dfsPath = graph.path
                                regenGraph()
                                runAlgorithm = True
                            elif loc == vertexLocations[fv]:
                                print("It will be finish vertex")
                            else:
                                print("can't be start vertex")

        if vertexes == dfsPath and runAlgorithm:
            time.sleep(0.5)
            drawText("path is " + str(dfsPath), txt_font, txt_colors[1], screen, 100, 100)
            numStep = 0
            runAlgorithm = False
            finishAlgo = True

        if runAlgorithm and numStep <= vertexCount * 2:
            if numStep % 2 == 0:
                vertexes.append(dfsPath[numVert])
                selectedVertex = dfsPath[numVert]
                numVert += 1
            else:
                numEdge += 1
                edges.append((dfsPath[numEdge - 1], dfsPath[numEdge]))
            numStep += 1
            time.sleep(0.2)

        drawGraph(screen, selectedVertex)  # vertexConnections, vertexLocations
        clock.tick(FPS)
        pg.display.flip()


def relocation():
    global runAlgorithm, dfsPath, vertexes, edges
    placingVertex()
    runAlgorithm = False
    graph.path = []
    dfsPath = []
    vertexes = []
    edges = []


'''# GRAPH DRAW ##############################'''


def drawGraph(screen, selectedVertex):  # vertexConnections, vertexLocations
    txt_font = pg.font.SysFont("menu_font", 32)
    txt_color = VERTEX_COLOR
    screen.fill(BG_COLOR)
    drawAllEdges(screen)  # vertexConnections
    drawAllVertexes(screen, selectedVertex)  # vertexConnections
    if finishAlgo:
        drawText("path is " + str(dfsPath)[1:-1:1], txt_font, txt_color, screen, 10, 10)
    drawText("click 'R' to rebuild graph", txt_font, txt_color, screen, 10, HEIGHT - 32)


def drawAllVertexes(screen, selectedVertex):
    num_font = pg.font.SysFont("numeration", R)
    for key, value in vertexConnections.items():
        vertexNumber = str(key)
        vertexValue = str((len(vertexConnections[key])))
        drawVertex(screen, VERTEX_COLOR, vertexLocations[key])
        '''drawVertex(screen, color, loc)'''
        drawText(vertexNumber, num_font, "Black", screen, vertexLocations[key][0] - 4, vertexLocations[key][1] - 4)
        drawText(vertexValue, num_font, "Red", screen, vertexLocations[key][0] + R, vertexLocations[key][1] - R)

    if runAlgorithm:
        for v in vertexes:
            vertexNumber = str(v)
            vertexValue = str((len(vertexConnections[v])))
            drawVertex(screen, VERTEX_VISITED_COLOR, vertexLocations[v])
            if vertexes != dfsPath:
                drawVertex(screen, "Cyan", vertexLocations[selectedVertex])
            drawText(vertexNumber, num_font, "Black", screen, vertexLocations[v][0] - 4, vertexLocations[v][1] - 4)
            drawText(vertexValue, num_font, "Red", screen, vertexLocations[v][0] + R, vertexLocations[v][1] - R)


def drawVertex(screen, color, loc):
    pg.draw.circle(screen, color, loc, R)


def drawAllEdges(screen):
    for key, value in vertexConnections.items():
        for i in range(len(vertexConnections[key])):
            drawEdge(screen, EDGE_COLOR, vertexLocations[key], vertexLocations[vertexConnections[key][i]],
                     EDGE_WIDTH)
            '''drawEdge(screen, color, startLoc, finishLoc, width)'''
    if runAlgorithm:
        for i in range(len(edges)):
            drawEdge(screen, EDGE_DELETED_COLOR, vertexLocations[edges[i][0]], vertexLocations[edges[i][1]], EDGE_WIDTH)


def drawEdge(screen, color, startLoc, finishLoc, width):
    pg.draw.line(screen, color, startLoc, finishLoc, int(width))


def drawText(text, font, color, surface, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


'''# MENU ##############################'''


def mainMenu():
    global graphMatrix, vertexConnections, vertexCount, graph
    global FILE
    pg.init()
    pg.display.set_caption('Euler Path')
    screen = pg.display.set_mode((WIDTH, HEIGHT), 0, 32)
    font_graph = pg.font.SysFont("menu_font", 32)
    bg_image = pg.transform.scale(pg.image.load("images/bg_image_dark.jpg"), (WIDTH, HEIGHT))

    txt_colors = [(10, 10, 10), (50, 250, 250), (220, 120, 0), (30, 150, 150)]
    '''txt_colors = black, cyan, orange, darkCyan'''

    bWidth = WIDTH // 6
    bHeight = HEIGHT // 20
    bx = WIDTH // 2 - bWidth * 2
    by = HEIGHT // 3 - bHeight
    shadow = 3
    filePath = r"\graphs\graph.txt"
    fileLoc = r"C:\Users\Kirill_07\PycharmProjects\graphEilerionianPath" + filePath

    click = False

    while True:
        screen.fill("black")
        screen.blit(bg_image, pg.Rect(0, 0, WIDTH, HEIGHT))

        mx, my = pg.mouse.get_pos()

        button_build = pg.Rect(bx, by, bWidth, bHeight)
        button_options = pg.Rect(bx, by + bHeight * 2, bWidth, bHeight)

        if button_build.collidepoint((mx, my)):
            if click:
                if FILE_LOADED:
                    graphBuilder()
                else:
                    graphLoad()
                    graphBuilder()
                    print("choose file")
        if button_options.collidepoint((mx, my)):
            if click:
                filePath = ""
                filePath = easygui.fileopenbox(filetypes=["*.txt"], default=r"graphs\*.txt")
                if filePath:
                    fileLoc = filePath
                    FILE = open(filePath)
                    graphMatrix = []
                    vertexConnections = {}
                    vertexCount = 0
                    graph = Graph(vertexCount)
                    graphLoad()
                else:
                    filePath = r"\graphs\graph.txt"

        drawText('Build Graph', font_graph, txt_colors[0], screen, bx + shadow, by + shadow)
        drawText('Build Graph', font_graph, txt_colors[1], screen, bx, by)
        drawText('Choose File', font_graph, txt_colors[0], screen, bx + shadow, by + bHeight * 2 + shadow)
        drawText('Choose File', font_graph, txt_colors[1], screen, bx, by + bHeight * 2)

        drawText('   chosen : ', font_graph, txt_colors[0], screen, bx + shadow, by + bHeight * 3 + shadow)
        drawText('   chosen : ', font_graph, txt_colors[1], screen, bx, by + bHeight * 3)
        drawText(fileLoc[63::], font_graph, txt_colors[0], screen, bx + bWidth + shadow, by + bHeight * 3 + shadow)
        drawText(fileLoc[63::], font_graph, txt_colors[1], screen, bx + bWidth, by + bHeight * 3)

        clock = pg.time.Clock()
        click = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                pass
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pg.display.update()
        clock.tick(FPS)


'''# RUN ##############################'''

if __name__ == '__main__':
    mainMenu()
