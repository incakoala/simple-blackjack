import pytest
from src.blackjack import BlackJack


def test_calculate_total_value():
    """Test that the logic for calculating total hand value is correct"""
    game = BlackJack()
    game.player_hand = {'A': [11, 11], '6': [6], '2': [2]}
    game.assess_hand(game.player_hand)
    assert game.total_value(game.player_hand) == 20


def test_deal_card():
    """Test that the logic for dealing card from a 52-card deck is correct"""
    game = BlackJack()
    game.draw_card(game.dealer_hand)
    game.draw_card(game.dealer_hand)
    # Manually deal Player four 2's
    for i in range(4):
        game.player_hand['2'].append(2)

    # Manually take all four 2's out of the deck
    game.deck = [c for c in game.deck if c != '2']
    # Assert that all 4 cards have been taken out
    assert len(game.deck) == 46

    # Deal again using the deal_card function (randomized)
    card_dealt = game.draw_card(game.player_hand)
    # Assert that 1 card have been taken out
    assert len(game.deck) == 45
    # Assert that the randomly dealt card isn't 2 (there are no more 2's in the deck at this point)
    assert card_dealt != '2'


def test_assess_hand_with_one_ace():
    """Test that assess_hand algorithm will always take a maximum, non-bust value"""
    game = BlackJack()
    game.player_hand['A'].append(11)
    game.player_hand['J'].append(10)
    game.assess_hand(game.player_hand)
    # nothing changes, since current hand is a maximum non-bust value
    assert game.player_hand['A'][0] == 11
    assert game.total_value(game.player_hand) == 21


def test_assess_hand_with_two_aces():
    """
    Test that assess_hand algorithm will adjust the value(s) of Aces(s)
    to ensure a maximum, non-bust value
    """
    game = BlackJack()
    game.dealer_hand['A'].append(11)
    game.dealer_hand['A'].append(11)
    game.dealer_hand['9'].append(9)
    # Before calling assess_hand it should bust
    assert game.is_bust(game.dealer_hand)
    # call assess_hand to adjust value
    game.assess_hand(game.dealer_hand)
    # one of the 11s should be adjusted to 1 to prevent busting
    assert game.dealer_hand['A'][0] == 1
    assert not game.is_bust(game.dealer_hand)
    assert game.total_value(game.dealer_hand) == 21


def test_blackjack():
    """Test the logic of is_blackjack"""
    game = BlackJack()
    game.player_hand['A'].append(11)
    game.player_hand['J'].append(10)
    game.draw_card(game.dealer_hand)
    game.draw_card(game.dealer_hand)
    game.assess_both_hands(game.player_hand, game.dealer_hand)

    assert game.is_blackjack(game.player_hand)


def test_early_not_bust():
    """Initial two cards can never bust"""
    game = BlackJack()
    # Deal hands randomly using deal_card
    for _ in range(2):
        game.draw_card(game.player_hand)
        game.draw_card(game.dealer_hand)
    game.assess_both_hands(game.player_hand, game.dealer_hand)
    # Should never bust since in the worst case A A will adjust to 1 11
    assert not game.is_bust(game.player_hand)


def test_bust():
    """Manually deal hands and test dealer busts"""
    game = BlackJack()
    # Dealer
    game.dealer_hand['6'].append(6)
    game.dealer_hand['J'].append(10)
    # Player
    game.player_hand['10'].append(10)
    game.player_hand['J'].append(10)
    game.assess_both_hands(game.player_hand, game.dealer_hand)
    # Assume Player stood here
    # Dealer's turn
    # Dealer hits because total is still < 17
    game.dealer_hand['6'].append(6)  # to ensure bust
    game.assess_hand(game.dealer_hand)
    # Dealer busts when > 21 assuming Player hasn't busted or blackjacked
    assert game.is_bust(game.dealer_hand)
    assert not game.is_bust(game.player_hand)
    assert not game.is_blackjack(game.player_hand)


def test_tie():
    """Manually deal hands and test for tie"""
    game = BlackJack()
    game.player_hand['7'].append(7)
    game.player_hand['J'].append(10)
    game.dealer_hand['5'].append(5)
    game.dealer_hand['5'].append(5)
    game.dealer_hand['7'].append(7)
    game.assess_both_hands(game.player_hand, game.dealer_hand)
    assert game.total_value(game.player_hand) == game.total_value(game.dealer_hand)


def test_player_higher_than_dealer():
    """Manually deal hands and test that player is higher than dealer"""
    game = BlackJack()
    game.player_hand['A'].append(11)
    game.player_hand['A'].append(11)
    game.player_hand['7'].append(7)
    game.dealer_hand['5'].append(5)
    game.dealer_hand['5'].append(5)
    game.dealer_hand['7'].append(7)
    game.assess_both_hands(game.player_hand, game.dealer_hand)
    assert not game.is_bust(game.player_hand)
    assert game.total_value(game.player_hand) > game.total_value(game.dealer_hand)


def test_dealer_turn_hit():
    """Test that Dealer hits if total value is < 17"""
    game = BlackJack()
    # Manually deal 16 to Dealer
    game.dealer_hand['7'].append(7)
    game.dealer_hand['9'].append(9)
    # Player
    game.draw_card(game.player_hand)
    game.draw_card(game.player_hand)
    game.assess_both_hands(game.player_hand, game.dealer_hand)
    # Assume Player stood here
    # start Dealer's turn
    game.dealer_turn()
    # Dealer will continue hitting because value is under 17
    assert game.total_value(game.dealer_hand) >= 17


def test_dealer_turn_stand():
    """Test that Dealer stands when total value is >= 17"""
    game = BlackJack()
    # Manually deal 17 to Dealer
    game.dealer_hand['7'].append(7)
    game.dealer_hand['Q'].append(10)
    # Player
    game.draw_card(game.player_hand)
    game.draw_card(game.player_hand)
    game.assess_both_hands(game.player_hand, game.dealer_hand)
    # Assume Player stood here
    # start Dealer's turn
    game.dealer_turn()
    # Dealer will automatically hold at 17
    assert game.total_value(game.dealer_hand) == 17
