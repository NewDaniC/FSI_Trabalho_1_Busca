import math
from colorama import Fore, Style
import time
import os

TIME_SLEEP = 0.5
RECONPENSA = -5


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent  # Nó pai para rastrear o caminho
        self.position = position  # Posição na matriz

        self.g = 0  # Custo do caminho do início ao nó atual
        self.h = 0  # Heurística: estimativa do custo do nó atual ao fim
        self.f = 0  # Função de avaliação: f = g + h

    def __eq__(self, other):
        return self.position == other.position


os.system('cls')

def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)  # Cria o nó de início com a posição inicial
    start_node.g = start_node.h = start_node.f = 0  # Inicializa os valores de custo
    end_node = Node(None, end)  # Cria o nó de fim com a posição final
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []  # Lista aberta: nós a serem explorados
    closed_list = []  # Lista fechada: nós já explorados

    # Add the start node
    open_list.append(start_node)  # Adiciona o nó de início à lista aberta

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        # Obtém o nó com menor custo na lista aberta
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item  # Encontra o nó com menor função de avaliação
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)  # Remove o nó atual da lista aberta
        closed_list.append(current_node)  # Adiciona o nó atual à lista fechada

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)  # Constrói o caminho reverso
                current = current.parent
            return path[::-1]  # Retorna o caminho do início ao fim

        # Generate children
        children = []
        # Adjacent squares
        # for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:

            # Get node position
            node_position = (
                current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            # if maze[node_position[0]][node_position[1]] != 0:
            #     continue
            if maze[node_position[0]][node_position[1]] in [1, 10, 4, 20, RECONPENSA]:
                pass  # Permite a navegação em células com valor 1, 10, 4, 20
            else:
                continue  # Impede a navegação em outras células

            # Create new node
            # Cria um novo nó com o nó atual como pai
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)  # Adiciona o novo nó à lista de filhos

        print("---   ---   ---   ---   ---")

        # Loop through children
        for child in children:
            # Child is on the closed list

            for closed_child in closed_list:
                if child == closed_child:
                    continue

            child.g = current_node.g + \
                maze[child.position[0]][child.position[1]]
            
            ''' Heurística Distância de Manhattan   '''
            child.h = ((child.position[0] - end_node.position[0]) **
                       2) + ((child.position[1] - end_node.position[1]) ** 2)

            ''' Heurística Distância de Chebyshev   '''
            # child.h = max(abs(child.position[0] - end_node.position[0]),
            #               abs(child.position[1] - end_node.position[1]))
            
            ''' Heurística Distância de Euclidiana  '''
            # child.h = ((child.position[0] - end_node.position[0]) ** 2 +
            #            (child.position[1] - end_node.position[1]) ** 2) ** 0.5
            
            ''' Heurística Distância de Octile  '''
            # dx = abs(child.position[0] - end_node.position[0])
            # dy = abs(child.position[1] - end_node.position[1])
            # child.h = (dx + dy) + (math.sqrt(2) - 2) * min(dx, dy)
            
            ''' Heurística Distância de Minkowski  '''
            # p = 2  # Pode ser qualquer valor real positivo
            # child.h = (abs(child.position[0] - end_node.position[0]) ** p +
            #            abs(child.position[1] - end_node.position[1]) ** p) ** (1/p)

            ''' Heurística Distância de Diagonal  '''
            # dx = abs(child.position[0] - end_node.position[0])
            # dy = abs(child.position[1] - end_node.position[1])
            # child.h = max(dx, dy)

            
            child.f = child.g + child.h

            # Print the g, h, and f values for each node
            print(
                f"Node at position {child.position}: g = {child.g}, h = {child.h}, f = {child.f}")

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)  # Adiciona o filho à lista aberta

def print_maze_with_info(maze, path, current_node):
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if (i, j) == start:
                print(Fore.GREEN + "S", end=" ")
            elif (i, j) == end:
                print(Fore.RED + "E", end=" ")
            elif (i, j) in path:
                print(Fore.YELLOW + "X", end=" ")
            elif cell == 0:
                print(Fore.WHITE + "#", end=" ")
            elif (i, j) == current_node.position:
                print(Fore.YELLOW + "☺", end=" ")
            else:
                if cell == 1:
                    print(Fore.GREEN + ".", end=" ")
                elif cell == 4:
                    print(Fore.CYAN + ".", end=" ")
                elif cell == 10:
                    print(Fore.MAGENTA + ".", end=" ")
                elif cell == 20:
                    print(Fore.LIGHTWHITE_EX + ".", end=" ")
                elif cell == RECONPENSA:
                    print(Fore.WHITE + "$", end=" ")  # Recompensa negativa
        print()


def main():

    maze = [[0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
            [0,  1,  1,  1,  4,  1,  1,  1,  1,  0],
            [0,  1,  1, 20,  1,  1,  1,  1,  1,  0],
            [0,  1,  1,  1,  0,  1,  1,  1,  1,  0],
            [0,  1,  1,  1,  0,  1,  1,  1,  1,  0],
            [0,  1,  1,  1,  0,  1,  1,  1,  1,  0],
            [0,  1,  1,  1,  0,  1,  1,  1,  1,  0],
            [0,  1,  1,  1,  0,  1,  1,  1,  1,  0],
            [0,  1,  1,  1,  1,  1,  1,  1,  1,  0],
            [0,  0,  0,  0,  0,  0,  0,  0,  0,  0]]

    global start, end
    start = (1, 1)
    end = (4, 7)

    path = astar(maze, start, end)
    # print(path)

    # input("Pressione Enter para continuar...")

    # for i, current_node in enumerate(path):
    #     if i == len(path) - 1:
    #         os.system('cls')  # Limpa o console no Windows
    #         print_maze_with_info(maze, path, Node(None, current_node))
    #     else:
    #         os.system('cls')  # Limpa o console no Windows
    #         print_maze_with_info(maze, [], Node(None, current_node))
    #         time.sleep(TIME_SLEEP)
    
    if path is None:
        print("Não é possível chegar no destino")
    else:
        print(path)
        input("Pressione Enter para continuar...")

        for i, current_node in enumerate(path):
            if i == len(path) - 1:
                os.system('cls')  # Limpa o console no Windows
                print_maze_with_info(maze, path, Node(None, current_node))
            else:
                os.system('cls')  # Limpa o console no Windows
                print_maze_with_info(maze, [], Node(None, current_node))
                time.sleep(TIME_SLEEP)


if __name__ == '__main__':
    main()
