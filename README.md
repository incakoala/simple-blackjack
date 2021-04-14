# Freenome Coding Challenge
**Vy Thai**

A command-line version of a single game of Blackjack. The only two players are the Player(user) and 
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

### Contents
* [Overview](#overview)
    * Assumptions/choices to overcome lack of clarity
    * What I did well
    * [Design Choices and Algorithm](#design)
        * Tradeoffs and how I resolved them
        * [Complexity analysis](#complexity-analysis)
    * [Improvements](#improvements)
* [How to use](#how-to-use)
    * [Requirements](#requirements)
    * [Run](#run)
    * [Test](#test)
        * [Manual tests](#manual-tests)
        * [Automated tests](#automated-tests)

## Overview
Without playing Blackjack (and barely any card game) before, the provided instructions did a really 
good job explaining the gameplay and its intricacies.

A couple small points of confusion and the assumptions I made:

* After dealing the initial two cards to each player, would the Dealer see their own hidden card?

    * Assumption: No, since Dealer's turn technically hasn't started yet

* In the case where both Player and Dealer got a Blackjack when their initial cards are dealt,
does the Player still win or is it a tie?
    ```
    Dealer has: J ? = ? (or J A = 21)
    Player has: 10 A = 21
    ```
   * Assumption: Same as above, since the ? value seems to be hidden to both players until Dealer's turn
starts

After fully understanding the requirements, I defined some of the main areas that the code should 
entail:

* Randomized card-dealing logic
* Ace-assessing logic to ensure a hand always has a maximum, non-bust value
* Keeping track of and printing a hand's cards and their corresponding values
* General flow of the game (game starts, taking turns, winning/losing conditions, game ends, etc.)


### Design Choices and Algorithm
I started out by deciding on the data structures needed to store the game's global assets (ie. part of 
the game state), which are **deck**, **player_hand**, and **dealer_hand**

Since we're using a 52-card deck and cards are drawn one by one throughout the game (and won't be put
back into the pile), I simply used an array to store the '1'-'10', 'J', 'Q', 'K', 'A' cards. The benefits
of using array is that we can easily mutate or 'shuffle' the orders of the cards, randomly pick a 
card using random.randint, as well as permanently deleting a card after it's been drawn in O(1).

As for the two hands, we needed a way to represent the actual card names, as well as their corresponding
values ('J' for 10, 'A' for 11 or 1, etc.), I chose to use defaultdict(list) to store card names as
keys and card values as arrays of values. This would simply data access later on as a player draws 
multiple cards of the same type, or draws multiple A's that can worth either 11 or 1. For example:

    player_hand = {'9': [9], '2': [2, 2], 'A': [11, 1]}
    
#### Ace-assessing algorithm
An important logic of the game deals with assessing and adjusting the value of an Ace. After observing
the maximum, non-bust values of [A A = 12], [A A A = 13], [A A A A = 14], and so on, it's clear that
regardless of the number of Aces present in a hand, as long as there are more than 1 Aces, only one
of which should be valued 11 in order to prevent busting. The idea is to greedily start out with
the great possible value, and readjust/lower the value as necessary. The algorithm is then simply as follows:

    All newly drawn A's value defaults as 11
    Call assess_hand(hand):
        If any Aces at all have been drawn (aces_drawn > 0):
            Traverse through each card in the hand:
                If at any time an 11 is present and total_value of hand is a bust, adjust it to 1
                Break the loop if number of aces_adjusted == aces_drawn (no more aces to look for)

Note that another global variable **aces_drawn** comes in handy here to help us break from the loop early
as necessary.

<ins>Time Complexity:</ins> O(1) or constant
   * The worst case where a single hand has 4 A's and assess_hand has to traverse 
the whole dictionary to find entry 'A' is: **O(# of card type * # of A's) or O(13 * 4)**

### Reflection & Future Improvements
Overall, I think I did a good job on choosing the data structures that are intuitive, efficient, and 
serve the purpose of the game. Similarly, I like the overall structure and separation of concerns of 
my code. I think that it helped that I took the time to understand all the requirements and explored 
different design choices and structures first before actually writing the code. Last but not least, 
the unit and integration tests were very extensive and I found them helpful in testing the correctness 
of the code, despite some shortcomings that I'm gonna talk about soon.

Given more time, I would convert the code into an object-oriented design pattern to further modularize
the code and its entities, with classes such as Cards, Deck, Hands, and Game flow. Furthermore, I would
like to experiment the full capacities of pytest and mock libraries, to further improve the automated 
testing of the gameplay under different scenarios. For now, the unit tests carry most of the 
responsibilities for these scenarios (tie, bust, blackjack, etc.), but I know that this can be automated at
the integration level with mocking random.choice, for example. 

## How to use
### Requirements
* [python3](https://www.python.org/downloads/)
* [pytest](https://pypi.org/project/pytest/)
    * Install pytest by running `pip3 install pytest` at project's root
    * Check that it was successfully installed `pytest --version`
    
### Run
1. Navigate to the root of the folder where this README is located
2. Run the program by typing `python3 src/blackjack.py` on the command line

### Test
#### Automated tests
Make sure that pytest is installed

1. Navigate to the root of the folder where this README is located
2. Simply run `pytest` on the command line to start a series of unit and integration tests defined in `/tests`
> Run `pytest -s` to run all tests and see game-related print statements

#### Manual tests
I manually played a bunch of mock games, each time with a strategy such as:
* Hit once and stand
* Stand as soon as my turn starts
* Keep hitting until I feel that it's a good place to stand (personally it's around 18)
* Keep hitting until bust or Blackjack
* Purposely enter a character other than (H)it or (S)tand
* Manually deal myself A 10 = 21 and get a Blackjack (again this could've been automated using mocks)

I also made sure to observe that the game behavior was to be expected, especially:
* Any Ace's values should be correctly adjusted
* Progression of the game: Dealer's turn only starts once I have stood, etc.
* Correct print statements in cases of bust, blackjack, winning, losing, game starts/ends, etc.
