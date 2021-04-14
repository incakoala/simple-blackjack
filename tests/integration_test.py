import pytest
from src import blackjack
from src.blackjack import BlackJack


def test_game_player_keeps_hitting(monkeypatch):
    """
    Automate the entire game flow
    when Player keeps hitting until they either bust/blackjack
    """

    def gen_input(prompt):
        return 'H\n'

    monkeypatch.setattr('builtins.input', gen_input)
    GAME = blackjack.main()
    assert GAME == "Game Exit"


def test_game_player_stands_right_away(monkeypatch):
    """
    Automate the entire game flow
    when Player stands as soon as their turn starts
    """

    def gen_input(prompt):
        return 'S\n'

    monkeypatch.setattr('builtins.input', gen_input)
    GAME = blackjack.main()
    assert GAME == "Game Exit"


def test_game_player_stands_at_some_point(monkeypatch):
    """
    Automate the entire game flow
    when Player hits and then stands
    """

    def gen_input():
        for ans in ['H', 'S']:
            yield ans

    GEN = gen_input()

    monkeypatch.setattr('builtins.input', lambda x: next(GEN))
    GAME = blackjack.main()
    assert GAME == "Game Exit"


def test_game_player_holds_at_17(monkeypatch):
    """
    Automate the entire game flow
    when Player keeps hitting until value is >= 17
    """
    game = BlackJack()
    game.draw_card(game.dealer_hand)
    game.draw_card(game.dealer_hand)
    game.player_hand["2"].append(2)
    game.player_hand["2"].append(2)
    game.assess_both_hands(game.player_hand, game.dealer_hand)
    game.print_hand(game.player_hand, "Player")
    game.print_hidden_hand(game.dealer_hand)

    def gen_input(prompt):
        if game.total_value(game.player_hand) < 17:
            return 'H\n'
        return 'S\n'

    monkeypatch.setattr('builtins.input', gen_input)
    GAME = game.player_turn()
    assert GAME == "Game Exit"
