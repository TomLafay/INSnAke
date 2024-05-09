import pygame
import random


class Snake():
    """
    La classe Snake représente un serpent è_é

    Attributs :
        id (int) : L'identifiant unique du serpent.
        screen (pygame.Surface) : L'écran de jeu.
        grid_size (int) : La taille de la grille pour le jeu.
        posX (list) : La liste des positions x du serpent.
        posY (list) : La liste des positions y du serpent.
        head (int) : L'index de la tête du serpent dans les listes posX et posY.
        vx (int) : La vitesse du serpent en x (0 ou 1).
        vy (int) : La vitesse du serpent en y (0 ou 1).
        taille (int) : La taille du serpent.

    Méthodes :
        copy(self) : Crée une copie du serpent.
        directionSnake(self, dx, dy) : Change la direction du serpent.
        moveSnake(self) : Déplace le serpent dans la direction actuelle.
        move(self, direction) : Déplace le serpent dans une direction spécifiée.
        extend(self) : Étend le serpent d'une unité.
        getPossibleMoves(self, state) : Renvoie une liste des mouvements possibles pour le serpent.
        is_dead(self, state) : Vérifie si le serpent est mort.
        print_snake(self) : Affiche les informations du serpent dans la console.
        draw_snake(self, screen) : Dessine le serpent sur la fenêtre.
    """

    def __init__(self, id, screen, grid_size, x=None, y=None):
        if x is None:
            x = ((screen.get_width() // 2) // grid_size) * grid_size
        if y is None:
            y = ((screen.get_height() // 2) // grid_size) * grid_size
        orientation = random.choice(['horizontal', 'vertical'])
        if orientation == 'horizontal':
            self.posX = [x, x-grid_size, x-grid_size*2]
            self.posY = [y, y, y]
        else:  # vertical
            self.posX = [x, x, x]
            self.posY = [y, y-grid_size, y-grid_size*2]

        self.head = 0
        self.vx = 0
        self.vy = 0
        self.taille = 3
        self.screen = screen
        self.grid_size = grid_size
        self.id = id

    def copy(self):
        new_snake = Snake(self.id, self.screen, self.grid_size)
        new_snake.posX = self.posX.copy()
        new_snake.posY = self.posY.copy()
        new_snake.head = self.head
        new_snake.vx = self.vx
        new_snake.vy = self.vy
        new_snake.taille = self.taille
        return new_snake

    def directionSnake(self, dx, dy):
        if (self.vx, self.vy) != (-dx, -dy):
            self.vx = dx
            self.vy = dy

    # La méthode moveSnake met à jour l'index de la tête du serpent pour suivre le mouvement du serpent.
    # L'index de la tête est incrémenté de 1 à chaque mouvement pour pointer vers la nouvelle position de la tête.
    # L'opérateur modulo est utilisé pour s'assurer que l'index de la tête reste dans les limites de la liste des positions.
    # Cela permet de réutiliser les positions précédentes du serpent pour représenter la nouvelle position de la tête,
    # ce qui est efficace en termes de mémoire car il n'est pas nécessaire de créer de nouvelles listes ou d'ajouter de nouveaux éléments à la liste.
    def moveSnake(self):
        if self.vx != 0 or self.vy != 0:
            h = self.head
            x = self.posX[h]
            y = self.posY[h]
            h = (h + 1) % len(self.posX)

            self.posX[h] = x + self.vx * self.grid_size
            self.posY[h] = y + self.vy * self.grid_size
            self.head = h

    # Mise à jour de la direction du serpent en fonction de la direction spécifiée.
    # Puis appel de la méthode moveSnake pour déplacer le serpent dans la nouvelle direction.
    def move(self, direction):
        if direction == 'up':
            self.directionSnake(0, -1)
        elif direction == 'down':
            self.directionSnake(0, 1)
        elif direction == 'left':
            self.directionSnake(-1, 0)
        elif direction == 'right':
            self.directionSnake(1, 0)

        self.moveSnake()

    def extend(self):
        self.posX.append(self.posX[-1])
        self.posY.append(self.posY[-1])
        self.taille += 1

    # DIRECTION : (vx, vy)
    # UP : (0, -1)
    # DOWN : (0, 1)
    # LEFT : (-1, 0)
    # RIGHT : (1, 0)
    def getPossibleMoves(self, state):
        possibleMoves = []
        x, y = self.posX[self.head], self.posY[self.head]
        # UP
        if self.vy != 1 and not state.is_collision((x, y-self.grid_size), self.screen, self):
            possibleMoves.append('up')
        # DOWN
        if self.vy != -1 and not state.is_collision((x, y+self.grid_size), self.screen, self):
            possibleMoves.append('down')
        # LEFT
        if self.vx != 1 and not state.is_collision((x-self.grid_size, y), self.screen, self):
            possibleMoves.append('left')
        # RIGHT
        if self.vx != -1 and not state.is_collision((x+self.grid_size, y), self.screen, self):
            possibleMoves.append('right')

        return possibleMoves

    def is_dead(self, state):
        head_pos = (self.posX[self.head], self.posY[self.head])

        if state.is_wall_collision(head_pos, self.screen):
            return True, "wall", self.id

        elif state.is_self_collision(head_pos, self):
            return True, "self", self.id

        elif state.is_snake_collision(head_pos, self):
            return True, "other_snake", self.id

        return False, None, None

    def print_snake(self):
        print("Snake id: " + str(self.id) + " Head: " + str(self.head) + " Taille: " +
              str(self.taille) + " PosX: " + str(self.posX) + " PosY: " + str(self.posY))

    def draw_snake(self, screen):
        colors = [(67, 112, 229), (0, 160, 2)]
        # head_colors = [(45, 95, 226), (0,135,2)]
        # Couleur en fonction de l'id
        body_color = colors[self.id % len(colors)]
        # head_color = head_colors[self.id % len(head_colors)]

        for i in range(self.taille):
            # color = head_color if i == self.head else body_color
            color = body_color
            pygame.draw.rect(
                screen, color, (self.posX[i], self.posY[i], self.grid_size, self.grid_size))

        # On dessine les yeux
        eye_color = (255, 255, 255)  # Blanc

        if self.vx == 0 and self.vy == 0:
            pygame.draw.circle(
                screen, eye_color, (self.posX[self.head] + 12, self.posY[self.head] + 8), 3)
        elif self.vx == 1:
            # Right
            pygame.draw.circle(
                screen, eye_color, (self.posX[self.head] + 20, self.posY[self.head] + 8), 3)
        elif self.vy == 1:
            # Up
            pygame.draw.circle(
                screen, eye_color, (self.posX[self.head] + 12, self.posY[self.head] + 20), 3)
        elif self.vx == -1:
            # Left
            pygame.draw.circle(
                screen, eye_color, (self.posX[self.head] + 4, self.posY[self.head] + 8), 3)
        elif self.vy == -1:
            # Down
            pygame.draw.circle(
                screen, eye_color, (self.posX[self.head] + 12, self.posY[self.head] + 4), 3)
