import random
from collections import defaultdict


class BlackJack:
    """Game class containing game variables and all game play methods"""
    def __init__(self):
        # 52-card deck
        self.deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4
        # mapping to store how much each card type is worth
        self.mapping = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
                        'J': 10, 'Q': 10, 'K': 10, 'A': 11}
        # Player's and Dealer hands
        self.player_hand = defaultdict(list)
        self.dealer_hand = defaultdict(list)
        self.aces_drawn = 0

    def draw_card(self, hand):
        """Draw and add a card to hand"""
        # shuffle and draw a random card from the deck
        random.shuffle(self.deck)
        idx = random.randint(0, len(self.deck) - 1)
        card = self.deck[idx]
        if card == 'A': self.aces_drawn += 1
        # take the drawn card out of deck
        del self.deck[idx]
        # add card to hand
        hand[card].append(self.mapping[card])
        return card

    def total_value(self, hand):
        """
        Calculate total value of hand
        :return total value of hand
        """
        ret = 0
        for val in hand.values():
            for num in val:
                ret += num
        return ret

    def assess_hand(self, hand):
        """
        Assess and readjust ace(s) so that hand has a maximum, non-bust total value
        """
        aces_adjusted = 0
        if self.aces_drawn > 0:
            for key, val in hand.items():
                    for i in range(len(val)):
                        # if an Ace(11) is present and total value is a bust, adjust it to 1
                        if val[i] == 11 and self.total_value(hand) > 21:
                            val[i] = 1
                            aces_adjusted += 1
                            if aces_adjusted == self.aces_drawn:
                                break

    def assess_both_hands(self, hand1, hand2):
        """Assess two hands"""
        self.assess_hand(hand1)
        self.assess_hand(hand2)

    def is_bust(self, hand):
        """
        Check if hand is a bust
        :return True if it's a bust, False otherwise
        """
        return self.total_value(hand) > 21

    def is_blackjack(self, hand):
        """
        Check if hand is a Blackjack
        :return True if it's a Blackjack, False otherwise
        """
        return self.total_value(hand) == 21

    def player_turn(self):
        """Main logic of the game play and Player's turn"""
        ans = input("\nWould you like to (H)it or (S)tand? ")
        if ans[0].upper() == "H" or ans[0].upper() == "S":
            while ans[0].upper() == "H":
                print("\nPlayer hits")
                self.draw_card(self.player_hand)
                self.assess_hand(self.player_hand)
                self.print_hand(self.player_hand, "Player")

                if self.is_blackjack(self.player_hand):
                    self.print_blackjack("Player")
                    return "Game Exit"
                if self.is_bust(self.player_hand):
                    print("\nPlayer busts with %d" % self.total_value(self.player_hand))
                    self.print_dealer_win()
                    return "Game Exit"

                ans = input("\nWould you like to (H)it or (S)tand? ")

            print("\nPlayer stands with %s = %d" % (
                " ".join(self.convert_hand_to_list(self.player_hand)),
                self.total_value(self.player_hand)))

            # Player has stood, start Dealer's turn
            return self.dealer_turn()

        print("\nPlease only enter (H)it or (S)tand")
        return self.player_turn()

    def dealer_turn(self):
        """Main logic for Dealer's turn and End of game"""
        print("\n### Dealer's turn ###")
        self.print_hand(self.dealer_hand, "Dealer")
        if self.is_blackjack(self.dealer_hand):
            self.print_blackjack("Dealer")
            return "Game Exit"

        # Dealer will keep hitting as long as value is less than 17
        while self.total_value(self.dealer_hand) < 17:
            print("\nDealer hits")
            self.draw_card(self.dealer_hand)
            self.assess_hand(self.dealer_hand)
            self.print_hand(self.dealer_hand, "Dealer")

            if self.is_blackjack(self.dealer_hand):
                self.print_blackjack("Dealer")
                return "Game Exit"
            if self.is_bust(self.dealer_hand):
                print("\nDealer busts with %d" % self.total_value(self.dealer_hand))
                self.print_player_win()
                return "Game Exit"

        print("\nDealer stands with %s = %d" % (
            " ".join(self.convert_hand_to_list(self.dealer_hand)),
            self.total_value(self.dealer_hand)))

        # Dealer has stood, analyze scores and announce results
        self.announce_results()
        return "Game Exit"

    def announce_results(self):
        """Analyze final scores and announce winner"""
        if self.total_value(self.player_hand) > self.total_value(self.dealer_hand):
            self.print_player_win()
        elif self.total_value(self.dealer_hand) > self.total_value(self.player_hand):
            self.print_dealer_win()
        else:
            self.print_tie()

    def print_player_win(self):
        """Print Player's winning message and both scores"""
        print("\nPlayer Wins!\n%s = %d to Dealer's %s = %d" % (
            " ".join(self.convert_hand_to_list(self.player_hand)), self.total_value(self.player_hand),
            " ".join(self.convert_hand_to_list(self.dealer_hand)),
            self.total_value(self.dealer_hand)))

    def print_dealer_win(self):
        """Print Dealer's winning message and both scores"""
        print("\nDealer Wins!\n%s = %d to Player's %s = %d" % (
            " ".join(self.convert_hand_to_list(self.dealer_hand)), self.total_value(self.dealer_hand),
            " ".join(self.convert_hand_to_list(self.player_hand)),
            self.total_value(self.player_hand)))

    def print_tie(self):
        """Print tie and both scores"""
        print("\nTie!\nPlayer: %s = %d vs Dealer: %s = %d" % (
            " ".join(self.convert_hand_to_list(self.player_hand)), self.total_value(self.player_hand),
            " ".join(self.convert_hand_to_list(self.dealer_hand)),
            self.total_value(self.dealer_hand)))

    def print_blackjack(self, person):
        """Print Blackjack winning message"""
        print("\n%s Wins!\nBlackjack!" % person)

    def convert_hand_to_list(self, hand):
        """Convert hand defaultdict(list) into list() for ease of printing"""
        ret = list()
        for key, val in hand.items():
            for _ in val:
                ret.append(str(key))
        return ret

    def print_hand(self, hand, person):
        """Print any hand's cards and total value"""
        ret = self.convert_hand_to_list(hand)
        print("\n%s has: %s = %d" % (person, " ".join(ret), self.total_value(hand)))

    def print_hidden_hand(self, hand):
        """Print Dealer's initial hidden hand"""
        ret = list()
        ret.append(next(iter(hand)))
        ret.append('?')
        print("\nDealer has: %s = ?" % " ".join(ret))


def main():
    # Init a game
    game = BlackJack()

    # Deal two random cards each to Player and Dealer
    for _ in range(2):
        game.draw_card(game.player_hand)
        game.draw_card(game.dealer_hand)

    # game.dealer_hand['A'].append(11)
    # game.dealer_hand['10'].append(10)

    # print(player_hand)

    # Assess both Player's and Dealer's hands and readjust Aces if necessary
    game.assess_both_hands(game.player_hand, game.dealer_hand)

    print("\nGame Started!")
    print("\nDealing cards...")
    print("\n____________________")
    game.print_hand(game.player_hand, "Player")
    game.print_hidden_hand(game.dealer_hand)
    print("\n____________________")

    # Player immediately wins if got a Blackjack
    if game.is_blackjack(game.player_hand):
        game.print_blackjack("Player")
        """"
        I was confused about this part at first. 
        What if the Dealer also got a Blackjack? Does the Player still win or is it a tie?
        However it does make sense that the Player should win, because the Dealer's turn technically
        hasn't started yet and one card is still hidden.
        """
        return "Game Exit"

    # Start Player's turn
    print("\n### Player's turn ###")
    return game.player_turn()


if __name__ == "__main__":
    main()
