# python-santorini
Python beginner implementation of "Santorini" board game

Santorini is a fun, simple game for two players. Used to practice python programming

[Santorini](https://roxley.com/product/santorini/): board game published by Roxley Games, designed by Dr. Gordon Hamilton 

## Rules
- Two players are in control of two workers, racing to be first to climb the top of a three level building
- 5 x 5 board, all spaces start at building level zero, players alternate placing workers in any space
- Each turn:
    - Player will choose one worker and complete two actions, in order
    - First, worker will move
        - Workers can move one space away, diagonally or orthogonally
        - Space must be unoccupied
        - Can only move up one level
        - Can move down any number of levels
        - Cannot move onto a space with building level of four
     - Same worker will then build:
        - Worker can build one space away, diagonally or orthogonally
        - Space must be unoccupied
        - Cannot build past level four
        - Can build regardless of level of current space
            - Example: worker moved to space with level zero, can build in adjacent space of level three, making adjacent space level four

- Winning the game
    - Game is won if a worker moves onto a space of level three


## Currently
- Creates board, workers
- Allows moving and building, checks for legal moves
    - if illegal build is attempted, past move is reset, player turn starts over
- Switches turns until winner
- Code is very rough, printing of board state/game flow is also difficult to read

## Future Goals
- homogenize use of if/else and try/except blocks (trying both, learning clearer usage of both. Should also look for specific exceptions in except blocks, especially with raising of exceptions)
- streamline error messages (prints invalid movement/invalid build in two/three places, resulting in too much yelling at the player)
- continue to look for bugs
- reconsider if Worker objects need to store location and Space objects need to store occupant, seems redundant
- fix printing of new lines to make game more readable
- is a while loop the best way to play the game?
- Consider if coordinates should be taken in together, rather than first inputting row, then inputting column
