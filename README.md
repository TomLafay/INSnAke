# INSnAke: Snake avec Minimax

Ce projet présente une version de Snake où deux serpents contrôlés par des IA s'affrontent pour obtenir la plus grande taille possible. Chaque serpent est géré par une IA basée sur l'algorithme Minimax.

L'IA de chaque serpent évalue chaque mouvement possible en fonction de la fonction d'évaluation choisi afin de déterminer le mouvement optimal. Ce processus se répète à chaque tour, permettant aux serpents de prendre des décisions intelligentes et calculées pour maximiser leurs chances de survie et de croissance.

Dans l'état actuel du projet, les deux serpents sont entièrement contrôlés par des IA Cependant, dans le futur, une fonctionnalité prévue est l'ajout d'un mode multijoueur où un humain pourra contrôler l'un des deux serpents, permettant ainsi de se défier à l'IA.

De plus, avec les performances actuelles obtenues, le jeu peut être joué en temps réel, offrant une expérience de jeu fluide.

## Algorithme Minimax

L'algorithme Minimax est au cœur de la conception des intelligences artificielles pour les jeux à deux joueurs, où chaque joueur attend son tour pour agir, comme c'est le cas dans le jeu Snake. Son rôle principal est d'explorer les différentes possibilités de coups disponibles pour chaque joueur, en anticipant les conséquences à plusieurs étapes à venir. L'objectif ultime est de trouver le meilleur coup possible qui maximise les gains potentiels pour le joueur tout en minimisant les pertes potentielles (les scénarios où l'adversaire prendrait les décisions les plus défavorables pour le joeur courant), en tenant compte des actions de l'adversaire.

Pour augmenter les performances de l'algorithme, j'ai implementé l'élagage alpha-bêta, une technique qui permet de réduire considérablement le nombre de nœuds évalués, tout en préservant l'optimalité de la décision. L'élagage alpha-bêta fonctionne en maintenant deux valeurs, alpha et bêta, qui représentent respectivement la valeur minimale garantie pour le joueur maximisant et la valeur maximale garantie pour le joueur minimisant. Ainsi, lors de la recherche des mouvements optimaux, l'algorithme élimine les branches d'arbre qui ne peuvent pas influencer la décision finale, améliorant ainsi les performances de l'IA.

Voici l'implémentation de l'algorithme utilisée dans le projet :

```python
def minmax(state, snakeId, depth, alpha, beta, maximizingPlayer, evaluate, next_food):
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
```

## Fonctions d'évaluation

Ce projet propose plusieurs fonctions d'évaluation qui évaluent l'état actuel du jeu et attribuent un score à chaque mouvement possible. Voici les fonctions d'évaluation disponibles :

0. **evaluate_simple** : Évalue l'état du jeu en se basant sur la distance de Manhattan entre le serpent et la nourriture, et la taille du serpent.
1. **evaluate_distance** : Évalue l'état du jeu en se basant sur la distance euclidienne entre le serpent et la nourriture, et la taille du serpent.
2. **evaluate_better** : Évalue l'état du jeu en prenant en compte plusieurs facteurs, tels que la distance de Manhattan à la nourriture, si le serpent se déplace vers la nourriture, la distance de Manhattan à l'autre serpent, la compacité du serpent, et si le serpent peut tuer l'autre serpent au prochain tour.
3. **evaluate_overall** : Évalue l'état du jeu en combinant plusieurs facteurs avec des poids appropriés, tels que la distance de Manhattan à la nourriture, la distance de Manhattan au mur le plus proche, et la taille du serpent.
4. **evaluate_survivalist** : Évalue l'état du jeu en se basant sur la survie du serpent. Elle prend en compte plusieurs facteurs, tels que le nombre de cases bloquées autour de la tête du serpent, l'espace libre autour de la tête du serpent, la distance minimale à l'autre serpent, le nombre de mouvements possibles pour le serpent, et la distance à la nourriture.
5. **evaluate_compact** : (Ne fonctionne pas correctement actuellement) Évalue l'état du jeu en se basant sur la compacité du serpent et la distance à la nourriture.
6. **evaluate_compact_center** : (Ne fonctionne pas correctement actuellement) Évalue l'état du jeu en se basant sur la compacité du serpent, la distance à la nourriture, et la distance au centre du plateau de jeu.
7. **evaluate_path_to_food** : (Je conseille de réduire la profondeur si vous utilisez cette évaluation) Évalue l'état du jeu en se basant sur le chemin le plus court du serpent à la nourriture.

## Utilisation

Pour voir les deux IA jouer, suivez ces étapes :

1. Clonez ce dépôt sur votre machine locale.
2. Avoir python et pygame installés sur votre machine.
Vous pouvez installer pygame en utilisant `python3 -m pip install -U pygame --user` ou `sudo apt-get install python3-pygame`
3. Lancez le jeu en exécutant le script principal.

Voici comment vous pouvez utiliser le script avec différents paramètres depuis le terminal :

```bash
python main.py --depth 6 --width 500 --height 450 --grid_size 25 --fps 10 --eval_func 2 --eval_func_2 2
```

- `--depth`: Spécifie la profondeur pour l'algorithme Minimax. Assurez-vous que c'est un multiple de 2.
- `--width`: Définit la largeur de la fenêtre de jeu. Doit être un multiple de `grid_size`, donc ici nécessairement multiple de 25.
- `--height`: Définit la hauteur de la fenêtre de jeu. Doit être un multiple de `grid_size`, donc ici nécessairement multiple de 25.
- `--grid_size`: Taille de la grille pour le jeu. Ne modifiez pas pour l'instant.
- `--profile`: Active le profiler.
- `--fps`: Réglage de la vitesse du jeu.
- `--eval_func`: Choix de la première fonction d'évaluation en utilisant les indices fournis dans la liste des fonctions d'évaluation.
- `--eval_func_2`: Choix de la deuxième fonction d'évaluation en utilisant les indices fournis dans la liste des fonctions d'évaluation.

N'hésitez pas à expérimenter avec différentes fonctions d'évaluation et paramètres pour observer comment ils affectent les performances de l'IA.

Également, vous pouvez observer comment le serpent est mort avec le screenshot `dernierInstant.png` qui est généré à la fin de la partie.

## Crédits

Ce projet a été créé par Tom Lafay. N'hésitez pas à contribuer en soumettant des rapports de bogues, des demandes de fonctionnalités ou des pull requests.
