import pygame
import numpy as np

np.set_printoptions(threshold=np.inf)


class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0
    open_list = []
    closed_list = []
    open_list.append(start_node)
    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        open_list.pop(current_index)
        closed_list.append(current_node)
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue
            if maze[node_position[0]][node_position[1]] != 0:
                continue
            new_node = Node(current_node, node_position)
            children.append(new_node)
        for child in children:
            for closed_child in closed_list:
                if child == closed_child:
                    continue
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                    (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue
            open_list.append(child)


class Screen:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.screen = 0

        self.start = tuple()
        self.end = tuple()
        self.adj = 0 * np.ones((self.x, self.y), dtype='bool')

    def display(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.x, self.y))

        pygame.display.set_caption("Maze Solver")

        icon = pygame.image.load('maze.png')
        pygame.display.set_icon(icon)

        self.screen.fill((0, 0, 0))
        pygame.display.flip()

        # Game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        pos = pygame.mouse.get_pos()
                        self.start = pos
                        pygame.draw.rect(self.screen, (0, 100, 0), (pos[0], pos[1], 10, 10))

                    elif event.key == pygame.K_e:
                        pos = pygame.mouse.get_pos()
                        self.end = pos
                        pygame.draw.rect(self.screen, (100, 0, 0), (pos[0], pos[1], 10, 10))
                    elif event.key == pygame.K_RETURN:
                        path = astar(self.adj, self.start, self.end)
                        for i in path:
                            pygame.draw.rect(self.screen, (0, 0, 100), (i[0], i[1], 10, 10))

            # To draw
            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()

                pygame.draw.rect(self.screen, (100, 100, 100), (position[0], position[1], 10, 10))

                for i in range(position[0], position[0] + 10):
                    for j in range(position[1], position[1] + 10):
                        if (i < self.x and j < self.y) and (i >= 0 and j >= 0):
                            self.adj[i][j] = 1

            # To erase
            if pygame.mouse.get_pressed()[2]:
                position = pygame.mouse.get_pos()

                pygame.draw.rect(self.screen, (0, 0, 0), (position[0], position[1], 20, 20))

                for i in range(position[0], position[0] + 20):
                    for j in range(position[1], position[1] + 20):
                        if (i < self.x and j < self.y) and (i >= 0 and j >= 0):
                            self.adj[i][j] = 0

            pygame.display.flip()
