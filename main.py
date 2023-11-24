from core.game import Game

game = Game(
    pacman_location=(8, 0),
    ghost1_location=(10, 2),
    ghost2_location=(15, 6)
)

# print(game.dist['3']['2']['3']['2'])
game.run()
