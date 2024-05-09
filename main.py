
import argparse
import gameWithAi
import pygame
import cProfile
import pstats
from minimax import Minimax

def main():
    evaluate_functions = {
    0: Minimax.evaluate_simple,
    1: Minimax.evaluate_distance,
    2: Minimax.evaluate_better,
    3: Minimax.evaluate_overall,
    4: Minimax.evaluate_survivalist,
    5: Minimax.evaluate_compact,
    6: Minimax.evaluate_compact_center,
    7: Minimax.evaluate_path_to_food,
    }
    evaluate_functions_descriptions = {
    0: "evaluate_simple",
    1: "evaluate_distance",
    2: "evaluate_better",
    3: "evaluate_overall",
    4: "evaluate_survivalist",
    5: "evaluate_compact (Ne fonctionne pas correctement actuellement)",
    6: "evaluate_compact_center (Ne fonctionne pas correctement actuellement)",
    7: "evaluate_path_to_food (Je conseille de réduire la depth si vous utilisez cette évaluation)"
}
    eval_func_help = "Quelle fonction d'évaluation à utiliser pour le snake 0. Options possibles :\n" + "\n".join(f"{k}: {v}" for k, v in evaluate_functions_descriptions.items())  
    eval_func_help_bis = "Quelle fonction d'évaluation à utiliser pour le snake 1. Options possibles :\n" + "\n".join(f"{k}: {v}" for k, v in evaluate_functions_descriptions.items())  
    parser = argparse.ArgumentParser(description="Paramètres du jeu INSnAke.", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--depth', type=int, default=6, help='Profondeur pour l\'algorithme Minimax. Attention, nécessairement un multiple de 2.')
    parser.add_argument('--width', type=int, default=500, help='Largeur de la fenêtre du jeu. Attention, doit être un multiple de grid_size. Donc ici nécessairement multiple de 25.')
    parser.add_argument('--height', type=int, default=450, help='Hauteur de la fenêtre du jeu. Attention, doit être un multiple de grid_size. Donc ici nécessairement multiple de 25.')
    parser.add_argument('--grid_size', type=int, default=25, help='Taille de la grille pour le jeu. Ne pas modifier pour l\'instant.')
    parser.add_argument('--profile', action='store_true', help='Activer le profiler')
    parser.add_argument('--fps', type=int, default=10, help='Vitesse du jeu')
    parser.add_argument('--eval_func', type=int, default=2, help=eval_func_help)
    parser.add_argument('--eval_func_2', type=int, default=2, help=eval_func_help_bis)
    
    args = parser.parse_args()
    
    pygame.init()
    pygame.display.set_caption('IA RUMBLE INSnAke')
    screen = pygame.display.set_mode((args.width, args.height))
    
    evaluate_functions = {
    0: evaluate_functions[args.eval_func],
    1: evaluate_functions[args.eval_func_2],
    } 
    SnakeGame = gameWithAi.GameWithAi(args.depth, evaluate_functions, screen, args.fps,args.grid_size)
    
    if args.profile:
        profiler = cProfile.Profile()
        profiler.enable()
    
    SnakeGame.run_game()
    
    if args.profile:
        profiler.disable()
        profiler.dump_stats("Docs/profiling_results.txt")
        p = pstats.Stats('Docs/profiling_results.txt')
        p.sort_stats('time').print_stats(10)
    # Pour afficher le profilage dans le navigateur : snakeviz profiling_results.txt

if __name__ == "__main__":
	main()