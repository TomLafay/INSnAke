
import numpy as np
import math
import random
from collections import deque

class Minimax:
    """
    La classe Minimax implémente l'algorithme Minimax pour le jeu de serpent. Cet algorithme est utilisé pour déterminer
    le meilleur mouvement possible pour un serpent à un certain état (State) du jeu.

    Méthodes :
    minmax(state, snakeId, depth, alpha, beta, maximizingPlayer, evaluate, next_food) : 
        Cette méthode implémente l'algorithme Minimax avec élagage alpha-beta. Elle prend en paramètres l'état actuel du jeu, 
        l'ID du serpent, la profondeur de recherche maximale, les valeurs alpha et beta pour l'élagage, 
        un booléen indiquant si le joueur actuel est le joueur maximisant, la fonction d'évaluation à utiliser, et la position de la prochaine nourriture.
        Elle retourne la meilleure valeur que le joueur actuel peut obtenir et le meilleur mouvement que le joueur actuel peut faire.
    
    evaluate_simple(state, snakeId) :
        Cette méthode calcule une évaluation simple de l'état du jeu pour le serpent spécifié. Elle prend en compte la distance de Manhattan 
        entre le serpent et la nourriture, et la taille du serpent.

    evaluate_distance(state, snakeId) :
        Cette méthode calcule une évaluation de l'état du jeu basée sur la distance euclidienne entre le serpent spécifié et la nourriture, 
        et la taille du serpent.
    
    evaluate_compact(state, snake_id) :
        Cette méthode calcule une évaluation de l'état du jeu basée sur la compacité du serpent spécifié et la distance à la nourriture.

    evaluate_compact_center(state, snake_id) :
        Pareil que evaluate_compact mais on ajoute la distance de la tête du serpent au centre de l'écran.

    evaluate_better(state, snake_id, radius=2, compactness=0.6) :
        Cette méthode calcule une évaluation plus complexe de l'état du jeu pour le serpent spécifié. Elle prend en compte plusieurs facteurs, 
        tels que la distance de Manhattan à la nourriture, si le serpent se déplace vers la nourriture, la distance de Manhattan à l'autre serpent, 
        la compactness du serpent, et si le serpent peut tuer l'autre serpent au prochain tour.

    evaluate_overall(state, snakeId) :
        Cette méthode calcule une évaluation globale de l'état du jeu pour le serpent spécifié. 
        Elle combine plusieurs facteurs avec des poids appropriés, tels que la distance de Manhattan à la nourriture,
        la distance de Manhattan au mur le plus proche, et la taille du serpent.
    
    evaluate_survivalist(state, snakeId) :
        Cette méthode calcule une évaluation de l'état du jeu basée sur la survie du serpent spécifié. Elle prend en compte plusieurs facteurs, 
        tels que le nombre de cases bloquées autour de la tête du serpent, l'espace libre autour de la tête du serpent, 
        la distance minimale à l'autre serpent, le nombre de mouvements possibles pour le serpent, et la distance à la nourriture.

    evaluate_path_to_food(state, snake_id) :
        Cette méthode calcule une évaluation de l'état du jeu basée sur le chemin le plus court du serpent spécifié à la nourriture.
        Attention, cette méthode utilise un algorithme de recherche en largeur (BFS) pour calculer le chemin, donc je conseille de diminuer
        la profondeur de minmax pour ne pas trop ralentir le jeu. (python3 main.py --depth 4)
    
    TODO:
     - evaluate_avoid_wall(state, snake_id):
     - evaluate_avoid_snake(state, snake_id):
     - evaluate_AStar(state, snake_id):
     - evaluate_tail(state, snake_id): # Plus le serpent est loin de sa queue, plus l'évaluation sera élevée
     - evaluate_encirclement(state, snake_id): #Capacité du serpent à encercler l'autre serpent
    """
         
    def minmax(state, snakeId, depth, alpha, beta, maximizingPlayer, evaluate,next_food):
        if depth == 0 or state.game_over()[0]:
            eval = evaluate(state, snakeId)
            return (eval if maximizingPlayer else -eval), None
        else:
            bestValue = -float('inf') if maximizingPlayer else float('inf')
            bestMove = None
            actions = state.snakes[snakeId].getPossibleMoves(state)
            random.shuffle(actions)
            for action in actions:
                newState = state.clone()
                newState.snakes[snakeId].move(action)
                newState.update_food(next_food)
                nextSnakeId = 1 - snakeId
                eval, _ = Minimax.minmax(newState, nextSnakeId, depth - 1, alpha, beta, not maximizingPlayer, evaluate, next_food)
                if (maximizingPlayer and eval > bestValue) or (not maximizingPlayer and eval < bestValue):
                    bestValue = eval
                    bestMove = action
                alpha, beta = (max(alpha, bestValue), beta) if maximizingPlayer else (alpha, min(beta, bestValue))
                if beta <= alpha:
                    break
            return bestValue, bestMove
        
    # @staticmethod. Cela signifie que la méthode appartient à la classe Minimax, 
    # mais ne nécessite pas une instance de cette classe pour être appelée
    @staticmethod
    def evaluate_simple(state,snakeId):
        snake = state.snakes[snakeId]
        food = state.food
        # Distance de Manhattan entre le serpent et la nourriture
        distance_to_food = abs(snake.posX[snake.head] - food[0]) + abs(snake.posY[snake.head] - food[1])
        # Le score du serpent est simplement sa taille
        score = snake.taille
            
        # Retourner une valeur plus élevée pour les distances plus courtes et les scores plus élevés
        return 100*score - distance_to_food/25
    
    @staticmethod
    def evaluate_distance(state,snakeId):
        snake = state.snakes[snakeId]
        food = state.food
        # Distance euclidienne
        # On peut aussi utiliser l'inverse de la distance plutôt que l'opposé
        distance_euclidean = math.sqrt((snake.posX[snake.head] - food[0])**2 + (snake.posY[snake.head] - food[1])**2)
        return 100*snake.taille-distance_euclidean/25
    
    @staticmethod
    def evaluate_better(state, snake_id, radius=2, compactness=0.6):
        snake = state.snakes[snake_id]
        food = state.food

        # Distance de Manhattan à la nourriture
        distance_to_food = abs(snake.posX[snake.head] - food[0]) + abs(snake.posY[snake.head] - food[1])

        # On vérifie si le serpent se déplace vers la nourriture
        direction_to_food = (np.sign(food[0] - snake.posX[snake.head]), np.sign(food[1] - snake.posY[snake.head]))
        moving_towards_food = direction_to_food == (snake.vx, snake.vy)

        # Distance de Manhattan à l'autre serpent
        other_snake_id = (snake_id + 1) % len(state.snakes)
        other_snake = state.snakes[other_snake_id]
        distance_to_other_snake = abs(snake.posX[snake.head] - other_snake.posX[other_snake.head]) + abs(snake.posY[snake.head] - other_snake.posY[other_snake.head])

        # Compactness
        compactness_rate = 0
        for i in range(len(snake.posX)):
            for j in range(i + 1, len(snake.posX)):
                compactness_rate += abs(snake.posX[i] - snake.posX[j]) + abs(snake.posY[i] - snake.posY[j])
        compactness_rate = 1 / compactness_rate if compactness_rate != 0 else 0

        # Bonus si le serpent peut tuer l'autre serpent au prochain tour
        can_kill_other_snake = distance_to_other_snake == 1

        # Artéfact de calcul quand il y avait plus que 2 serpents dans le jeu : on vérifie si dans un certain radius autour de la tête du serpent, il y a d'autres serpents
        dangerous_snakes = [other_snake_id for other_snake_id, other_snake in enumerate(state.snakes) if other_snake_id != snake_id and abs(snake.posX[snake.head] - other_snake.posX[other_snake.head]) + abs(snake.posY[snake.head] - other_snake.posY[other_snake.head]) <= radius]

        # Est-ce que le serpent est suffisamment compact ? (Au dessus d'un certain seuil à tuner)
        is_compact = compactness_rate > compactness

        # On veut minimiser la distance à la nourriture, maximiser la distance à l'autre serpent, et maximiser la compactness et on ajoute les bonus
        return (100*state.getScore(snake_id) - distance_to_food/25 + moving_towards_food + (distance_to_other_snake/25 if distance_to_other_snake/25 < 5 else 0) + (1000 if can_kill_other_snake else 0) + compactness_rate + (1000 if is_compact else 0) + len(dangerous_snakes))
    
    @staticmethod
    def evaluate_overall(state, snakeId):
        snake = state.snakes[snakeId]
        food = state.food
        food_distance = math.sqrt((snake.posX[snake.head] - food[0])**2 + (snake.posY[snake.head] - food[1])**2)/25 # Distance euclidienne
        nearest_wall_distance = state.getDistanceToWall(snakeId)/25 # Distance de Manhattan
        score = snake.taille
        # Combine the factors with appropriate weights
        evaluation = -food_distance +  nearest_wall_distance + 100 * score 
        # print(f"food_distance: {-food_distance}, nearest_wall_distance: {nearest_wall_distance}, score: {score}, evaluation: {evaluation}")
            
        return evaluation 
    
    @staticmethod
    def evaluate_survivalist(state, snakeId):
        snake = state.snakes[snakeId]
        head_x, head_y = snake.posX[snake.head], snake.posY[snake.head]

        # On regarde le nombre de cases bloquées autour de la tête du serpent.
        # Gridsize = 25
        blocked_cells = 0
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x, y = head_x + dx * 25, head_y + dy * 25
            if not state.is_valid_position((x, y),snake):
                blocked_cells += 1

        # On pénalise si beaucoup de cases sont bloquées
        penalty = blocked_cells * 100

        # Le calcul de l'espace libre autour de la tête du serpent est effectué 
        # en parcourant une grille de 7x7 cellules centrée sur la tête du serpent 
        # (3 cellules dans chaque direction à partir de la tête du serpent). 
        # Pour chaque cellule de cette grille, le code vérifie si la cellule est une position valide
        # (c'est-à-dire qu'elle est à l'intérieur des limites du plateau de jeu) 
        # et si elle n'est pas occupée par le corps du serpent. 
        # Si ces deux conditions sont remplies, la cellule est considérée comme un espace libre 
        # et le compteur free_space est incrémenté.
        free_space = 0
        for dx in range(max(0, head_x - 3 * 25), min(state.screen.get_width(), head_x + 4 * 25), 25):
            for dy in range(max(0, head_y - 3 * 25), min(state.screen.get_height(), head_y + 4 * 25), 25):
                x, y = head_x + dx, head_y + dy
                if state.is_valid_position((x, y),snake):
                    free_space += 1

        # On favorise les états avec plus d'espace libre
        bonus = free_space * 10 

        # On calcule la distance minimale à l'autre snake
        other_snake_id = 1 - snakeId # 1 ou 0
        other_snake = state.snakes[other_snake_id]
        min_distance_to_snake = float('inf')
        for x, y in zip(other_snake.posX, other_snake.posY):
            distance = abs(head_x - x) + abs(head_y - y)
            min_distance_to_snake = min(min_distance_to_snake, distance)

        # On favorise les états avec une plus grande distance à l'autre serpent
        distance_bonus = min_distance_to_snake * 5

        # Le nombre de mouvements possibles pour le serpent
        possible_moves = len(snake.getPossibleMoves(state))
        moves_bonus = possible_moves * 20

        # Calcul de la distance à la nourriture
        food_x, food_y = state.food
        distance_to_food = abs(head_x - food_x) + abs(head_y - food_y)
        food_bonus = -distance_to_food * 100  # On favorise les états où la nourriture est proche
        # Taille du serpent
        taille_bonus = snake.taille * 10000
        # Score final
        score = bonus + distance_bonus/25 + moves_bonus + food_bonus/25 - penalty + taille_bonus
        return score

    def evaluate_compact(state, snake_id):
        snake = state.snakes[snake_id]
        other_snake_id = 1 - snake_id
        other_snake = state.snakes[other_snake_id]
        food_x, food_y = state.food

        # Distances de Manhattan à la nourriture
        snake_distance_to_food = abs(snake.posX[snake.head] - food_x) + abs(snake.posY[snake.head] - food_y)
        other_snake_distance_to_food = abs(other_snake.posX[other_snake.head] - food_x) + abs(other_snake.posY[other_snake.head] - food_y)

        # Si l'autre serpent est plus proche de la nourriture, on favorise la compacité
        if other_snake_distance_to_food < snake_distance_to_food:
            # Plus la valeur de "compactness" est faible mieux c'est
            compactness = 0
            for i in range(len(snake.posX) - 1):
                compactness += abs(snake.posX[i] - snake.posX[i+1]) + abs(snake.posY[i] - snake.posY[i+1])
            # On inverse la valeur de "compactness" pour favoriser les états avec la plus grande compacité
            return -compactness
        else:
            # Pareil, on inverse pour que l'algorithme favorise quand il est plus proche de la nourriture
            # Distance 100 > Distance 10 mais distance -100 < distance -10. 
            # MinMax choisira bien la distance de 1O !
            return (100*snake.taille)-(snake_distance_to_food/25)
    
    def evaluate_compact_center(state, snake_id):
        snake = state.snakes[snake_id]
        other_snake_id = 1 - snake_id
        other_snake = state.snakes[other_snake_id]
        food_x, food_y = state.food

        # Distances de Manhattan à la nourriture
        snake_distance_to_food = abs(snake.posX[snake.head] - food_x) + abs(snake.posY[snake.head] - food_y)
        other_snake_distance_to_food = abs(other_snake.posX[other_snake.head] - food_x) + abs(other_snake.posY[other_snake.head] - food_y)

        # Distance de Manhattan au centre
        center_x, center_y = state.screen.get_width() // 2, state.screen.get_height() // 2
        snake_distance_to_center = abs(snake.posX[snake.head] - center_x) + abs(snake.posY[snake.head] - center_y)
        # Si l'autre serpent est plus proche de la nourriture, on favorise la compacité
        if other_snake_distance_to_food < snake_distance_to_food:
            # Plus la valeur de "compactness" est faible mieux c'est
            compactness = 0
            for i in range(len(snake.posX) - 1):
                compactness += abs(snake.posX[i] - snake.posX[i+1]) + abs(snake.posY[i] - snake.posY[i+1])
            # On inverse la valeur de "compactness" pour favoriser les états avec la plus grande compacité
            return -compactness - snake_distance_to_center/25
        else:
            return 200*snake.taille-snake_distance_to_food/25 - snake_distance_to_center/25

    
    def evaluate_path_to_food(state, snake_id):
        snake = state.snakes[snake_id]
        head_x, head_y = snake.posX[snake.head], snake.posY[snake.head]
        food_x, food_y = state.food

        # On initialise la file pour notre algorithme de recherche en largeur (BFS)
        # et notre ensemble de cellules visitées
        queue = deque([(head_x, head_y)])
        visited = set([(head_x, head_y)])

        while queue:
            x, y = queue.popleft()

            # Si on atteint la nourriture, on retourne positif
            if x == food_x and y == food_y:
                return 1000+Minimax.evaluate_distance(state,snake_id)

            # On ajoute les voisins valides et non visités à la file
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx * 25, y + dy * 25
                if state.is_valid_position((nx, ny),snake) and (nx, ny) not in zip(snake.posX, snake.posY) and (nx, ny) not in visited:
                    queue.append((nx, ny))
                    visited.add((nx, ny))

        # Si on ne trouve pas de chemin jusqu'à la nourriture, on retourne valeur négative
        return -1000+Minimax.evaluate_distance(state,snake_id)

   
    


    
