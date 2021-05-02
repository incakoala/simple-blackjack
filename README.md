# Simple Blackjack

A command-line version of a simple game of Blackjack. The only two players are the Player(user) and 
Dealer. The Player will be prompted to interact with the command-line throughout the game, and all dealing,
drawing, and other game play will be handled automatically by the program.


<details>
    <summary>Gameplay Overview</summary>
    
    1. Deal initial cards (two cards to each player)
    2. Display initial hands (hiding dealer's second card and score)
    3. Prompt user (Hit or Stand?)
        * Hit: add card to hand (check if busted)
        * Stand: end turn
        * show updated hand and value
        * repeat until player has stood, won (score == 21), or busted (score > 21)
    4. Dealer plays (if player has neither busted nor won)
        * print dealer's full hand, score
        * dealer keeps hitting until score >= 17
    5. Decide and report the winner, including hands and scores where relevant
</details>


## How to use
### Requirements
* [python3](https://www.python.org/downloads/)
* [pytest](https://pypi.org/project/pytest/)
    * Install pytest by running `pip3 install pytest` at project's root
    * Check that it was successfully installed: `pytest --version`
    
### Run
1. Navigate to the root of the folder where this README is located
2. Run the program by typing `python3 src/blackjack.py` on the command line
    > or run the file directly using your IDE

### Test
#### Automated tests
Make sure that pytest is installed

1. Navigate to the root of the folder where this README is located
2. Simply run `pytest` on the command line to start a series of unit and integration tests defined in `/tests`
    > or run `pytest -s` to run all tests and see game-related print statements
