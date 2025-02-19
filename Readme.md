# Python3 Simulator for the Coding Game Challenge "Code vs Zombies"

This project is a Python3 simulator for the coding game challenge ["Code vs Zombies"](https://www.codingame.com/multiplayer/optimization/code-vs-zombies). It allows you to visualize and test your strategies for the game using Pygame.

 ![image](https://github.com/user-attachments/assets/7c7c3524-2936-4872-8228-179f7a5b9a0d)

## Steps to Run Your Solution

1. **Install Pygame**

   Run the following command to install Pygame:

```sh
pip install pygame
```

2. **Create a Class that Extends AbstractAgen**

   Create a class that extends AbstractAgen and use it to instantiate the Simulation. Here is an example:

```Python dummy_agen.py
class DummyAgen(AbstractAgen):
    def play(self, x, y, human_count, humans, zombie_count, zombies):
        return {
            "target_x": x,
            "target_y": y,
        }

# main.py
level_file = 'data/levels/chaos.txt'
with open(level_file, 'r') as file:
    lines = file.readlines()

agen = ClosestZombieAgen()
sim = Simulation(lines, agen)
```
3. **Run the simulation**

```sh
python3 main.py
```

Press the "SPACE" key to move the simulation forward step by step. Note that the space button must be pressed twice to move to the second round (index 1) because the player orientation needs one round to compute (visualized by a yellow dot).

