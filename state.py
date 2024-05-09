import copy
import math
import random

class State:
    """
    La classe State représente l'état actuel du jeu de serpent. On peut voir cette classe comme un noeud dans l'arbre de recherche. 

    Attributs :
    snakes (list) : Une liste de tous les serpents dans le jeu.
    food (tuple) : La position actuelle de la nourriture sur la grille.
    screen (pygame.Surface) : L'écran de jeu.

    Méthodes :
    update_snake(index, new_snake) : Met à jour le serpent à l'index spécifié.
    update_food(new_food) : Met à jour la position de la nourriture.
    getScore(snakeId) : Retourne le score du serpent spécifié.
    getDistanceToFood(snakeId, grid_size=25) : Calcule la distance de Manhattan entre le serpent spécifié et la nourriture.
    getDistanceToWall(snakeId) : Calcule la distance minimale entre le serpent spécifié et le mur.
    getPossibleMoves(snakeId) : Retourne les mouvements possibles pour le serpent spécifié.
    generate_food(screen, grid_size=25) : Génère une nouvelle position de nourriture qui n'est pas occupée par un serpent.
    on_food(snakeId) : Vérifie si le serpent spécifié est sur la nourriture.
    is_valid_position(pos, snake) : Vérifie si la position spécifiée est valide pour le serpent spécifié.
    is_collision(pos, screen, snake) : Vérifie s'il y a une collision à la position spécifiée pour le serpent spécifié.
    is_wall_collision(pos, screen) : Vérifie s'il y a une collision avec le mur à la position spécifiée.
    is_self_collision(pos, snake) : Vérifie si le serpent spécifié se heurte à lui-même à la position spécifiée.
    is_snake_collision(pos, snake) : Vérifie si le serpent spécifié se heurte à un autre serpent à la position spécifiée.
    game_over() : Vérifie si le jeu est terminé.
    clone() : Crée une copie indépendante de l'état actuel.
    """
    def __init__(self, snakes, food, screen):
        self.snakes = snakes  
        self.food = food
        self.screen = screen

    def update_snake(self, index, new_snake):
        self.snakes[index] = new_snake

    def update_food(self, new_food):
        self.food = new_food

    def getScore(self, snakeId):
        return self.snakes[snakeId].taille

    def getDistanceToFood(self, snakeId,grid_size=25):
        snake = self.snakes[snakeId]
        food = self.food
        # Distance euclidienne : 
        # distance = math.sqrt((snake.posX[snake.head] - food[0])**2 + (snake.posY[snake.head] - food[1])**2)
        # Distance de Manhattan :
        distance = abs(snake.posX[snake.head] - food[0]) + abs(snake.posY[snake.head] - food[1])

        # if distance <= grid_size:
        #     return 0
        return distance
    
    def getDistanceToWall(self,snakeId):
        snake = self.snakes[snakeId]
        x, y = snake.posX[snake.head], snake.posY[snake.head]
        return min(x, y, self.screen.get_width() - x, self.screen.get_height() - y)
    
    def getPossibleMoves(self, snakeId):
        return self.snakes[snakeId].getPossibleMoves()

    def update_food(self,new_food):
        for snake in self.snakes:
            if (snake.posX[snake.head], snake.posY[snake.head]) == self.food:
                snake.extend()
                self.food = new_food

    def generate_food(self,screen,grid_size=25):
        while True:
            x = random.randint(0, screen.get_width() // grid_size - 1) * grid_size
            y = random.randint(0, screen.get_height() // grid_size - 1) * grid_size
            if not any((x, y) in list(zip(snake.posX, snake.posY)) for snake in self.snakes):
                return (x, y)
            
    def on_food(self,snakeId):
        snake = self.snakes[snakeId]
        return (snake.posX[snake.head], snake.posY[snake.head]) == self.food

    def is_valid_position(self, pos,snake):
        return not self.is_collision(pos, self.screen,snake)

    def is_collision(self, pos, screen,snake):
        if self.is_wall_collision(pos,screen):
            return True
        if self.is_self_collision(pos,snake):
            return True
        for snake in self.snakes:
            if self.is_snake_collision(pos,snake):
                return True
        return False
    
    def is_wall_collision(self,pos,screen):
        x, y = pos
        if x < 0 or y < 0 or x >= screen.get_width() or y >= screen.get_height():
            return True
        return False

    def is_self_collision(self, pos, snake):
        for i in range(0, snake.taille-1):
            if snake.posX[i] == pos[0] and snake.posY[i] == pos[1] and i != snake.head:
                # snake.print_snake()
                # print("Snake pos collision: " + str(snake.posX[i]) + " " + str(snake.posY[i]) + " Next pos: " + str(pos[0]) + " " + str(pos[1]) + "Snake Part" + str(i) + "Snake Size: " + str(snake.taille))
                return True
        return False
    
    def is_snake_collision(self, pos, snake):
        for other_snake in self.snakes:
            if other_snake != snake:
                for i in range(other_snake.taille):
                    if pos[0] == other_snake.posX[i] and pos[1] == other_snake.posY[i]:
                        return True
    
    def game_over(self):
        for snake in self.snakes:
            is_dead,cause,id = snake.is_dead(self)
            if is_dead:
                return True,cause,id
        return False,None,None

    # deepcopy permet d'avoir un nouveau State complètement indépendant du premier
    # def clone(self):
    #     new_snakes = copy.deepcopy(self.snakes)
    #     new_food = copy.deepcopy(self.food)
    #     return State(new_snakes, new_food, self.screen) 
    
    # En utilisant une liste en compréhension et en créant juste de nouvelles instances.
    def clone(self):
        new_snakes = [snake.copy() for snake in self.snakes]
        return State(new_snakes, self.food, self.screen)
    