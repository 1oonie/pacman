# pacman

pacman is pacman what i made

## Requirements

To install the requirements from the `requirements.txt` file:
```
python -m pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.org --user
```

Packages required by pacman are:
- Pillow (Version 8.2.0)
- pygame (Version 2.0.1)

## TODO

- [x] Scoring
  - [x] Update title every time pacman eats a coin
  - [x] ~~Stop the game when pacman eats all the coins~~
- [x] Ghosts
  - [x] Implement pathfinding for ghosts to find the tile they want to head for
  - [x] Only choose between paths that can be taken
  - [x] Ghost Types
    - [x] Blinky
    - [x] Pinky
    - [x] Inky
    - [x] Clyde
- [x] Fix the coins to make them better somehow
- [ ] Make the wall look better
- [ ] Power pellets
  - [ ] "Frightened" ghost sprite
  - [ ] Pacman gets faster in this state
  - [ ] Eating ghosts
  - [ ] Power pellet sprite/tile

 
Other stuff will get added to this list.

## Images

![image](https://user-images.githubusercontent.com/71032999/124361404-fc053600-dc26-11eb-9c0d-d1b859e478ef.png)
