from state import State
import pygame
import snake
import random
from minimax import Minimax


class GameWithAi():
    """
    La classe GameWithAi gère le jeu de serpent avec une IA basée sur l'algorithme Minimax. 

    Attributs :
        depth (int) : La profondeur de recherche pour l'algorithme Minimax.
        evaluate_functions (dict) : Un dictionnaire des fonctions d'évaluation à utiliser pour chaque serpent.
        screen (pygame.Surface) : L'écran de jeu.
        fps (int) : Les frames par seconde pour le jeu.
        grid_size (int) : La taille de la grille pour le jeu.
        state (State) : L'état actuel du jeu.
        clock (pygame.time.Clock) : L'horloge pour contrôler le temps dans le jeu.

    Méthodes :
        initialize_game(self) : Initialise une nouvelle partie du jeu.
        update_state(self, use_a_star=False) : Met à jour l'état du jeu en déplaçant les serpents.
        run_game(self) : Lance le jeu.
        screenshot(self, state) : Prend une capture d'écran de l'état actuel du jeu. Utile pour comprendre comment le serpent est mort.
        refresh_window(self) : Rafraîchit la fenêtre du jeu.
        draw_grid(self) : Dessine la grille du jeu.
        draw_food(self) : Dessine la nourriture sur la grille du jeu.
        generate_food(self) : Génère une nouvelle position de nourriture sur la grille.
    """
    
    def __init__(self,depth,evaluate_functions,screen,fps=10,grid_size=25):
        # Attributs pygame
        self.grid_size = grid_size
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = fps
        #Attributs IA
        self.num_snakes = 2
        self.depth = depth
        self.evaluate_functions = evaluate_functions
        self.state = None

    def initialize_game(self):
        food = self.generate_food()
        snakes = []
        for i in range(self.num_snakes):
            while True:
                x = random.randint(0, self.screen.get_width() // self.grid_size - 1) * self.grid_size
                y = random.randint(0, self.screen.get_height() // self.grid_size - 1) * self.grid_size
                snake_pos = (x, y)

                # On vérifie que le serpent n'est pas sur la nourriture
                if snake_pos == food:
                    continue  # Si oui, alors on génère une nouvelle position
                snakes.append(snake.Snake(i,self.screen, self.grid_size, x, y))
                break  # Sinon, on break la boucle

        self.state = State(snakes, food,self.screen)
    
    def update_state(self):
        # Prochaine valeur de la nourriture
        next_food = self.state.generate_food(self.screen)
        # Pour chaque serpent, on calcule le meilleur mouvement à l'aide de Minimax
        for i, snake in enumerate(self.state.snakes):
            _, bestMove = Minimax.minmax(self.state, i,self.depth,float('-inf'),float('inf'),True,self.evaluate_functions[i],next_food)
            # On déplace le serpent en fonction du meilleur mouvement et on met à jour l'état du jeu
            snake.move(bestMove)
            self.state.update_snake(i, snake)
            
            if self.state.on_food(i):
                self.state.update_food(next_food)
                next_food = self.state.generate_food(self.screen)
            
            
    def run_game(self):
        print(f"Snake 0 (bleu) avec {self.evaluate_functions[0].__name__}, Snake 1 (vert) avec {self.evaluate_functions[1].__name__}")
        # Cette boucle permet de relancer automatiquement le jeu après qu'un serpent soit mort
        game_running = True
        while game_running:
            self.initialize_game()

            # La boucle d'une partie
            running = True
            while running and not self.state.game_over()[0]:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        game_running = False
                
                self.update_state()

                game_over, cause,id = self.state.game_over()
                if game_over:
                    print(f"Game over: Snake n°{id} die to {cause}, Highscore: {max([snake.taille for snake in self.state.snakes])}")
                    # Une fois mort, on prend une capture d'écran pour pouvoir analyser
                    self.screenshot(self.state)
                    running = False

                # On refresh la fenêtre du jeu
                self.refresh_window()
                # Clock tick controle la vitesse du jeu
                self.clock.tick(self.fps)
        
    def screenshot(self,state):
        pygame.image.save(state.screen, "dernierInstant.jpg")

    def refresh_window(self):
        self.draw_grid()
        for snake in self.state.snakes:
            snake.draw_snake(self.screen)
        self.draw_food()
        pygame.display.update()

    def draw_grid(self):
        light_green = (169,215,81)
        dark_green = (162,208,73)
        
        for x in range(0, self.screen.get_width(), self.grid_size):
            for y in range(0, self.screen.get_height(), self.grid_size):
                rect = pygame.Rect(x, y, self.grid_size, self.grid_size)
                pygame.draw.rect(self.screen, light_green if (x // self.grid_size % 2 == y // self.grid_size % 2) else dark_green, rect)
    
    def draw_food(self):
        pygame.draw.circle(self.screen, (255, 0, 0), (self.state.food[0] + self.grid_size // 2, self.state.food[1] + self.grid_size // 2), self.grid_size // 2)
    
    def generate_food(self):
        return (random.randint(0, self.screen.get_width() // self.grid_size - 1) * self.grid_size, random.randint(0, self.screen.get_height() // self.grid_size - 1) * self.grid_size)