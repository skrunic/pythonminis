# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
houseScore = 0
playerScore = 0
cardPosition = [75,200]

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    #initializes the Card class starting values and methods
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        # determines card center depending on the suit and rank values (based on index in appropriate list)
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        
        #canvas.draw_image(image URL, center_source, width_height_source, center_dest, width_height_dest)
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    #initializes the Hand class starting values and methods
    def __init__(self):
        self.the_hand = []	# create Hand object

    def __str__(self):
        ans = ""
        for c in range(len(self.the_hand)):
            ans += str(self.the_hand[c]) + " "
        return "hand contains " + ans # return a string representation of a hand

    def add_card(self, card):
        self.the_hand.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        self.hand_total = 0
        aces = 0
        
        for ace in range(len(self.the_hand)):
            if self.the_hand[ace].get_rank() == "A":
                aces += 1
        
        for c in range(len(self.the_hand)):
                card_value = VALUES[self.the_hand[c].get_rank()]
                self.hand_total += card_value
        
        # if there are Aces in hand, calculate if they make the hand bust or no
        # if hand is busted, assume Ace value 1 until hand is not busted
        # if not busted, count Aces with value +10
        if aces == 0:
            return self.hand_total
        else:
            if self.hand_total + 10 <= 21:
                return self.hand_total + 10
            else: 
                return self.hand_total
                    
    def draw(self, canvas, pos):
        # draw a hand on the canvas using the draw method of Card class
        for card in range(len(self.the_hand)):
            # cardInHand stores Card object rank and suit
            cardInHand = Card(self.the_hand[card].get_suit(), self.the_hand[card].get_rank())
            
            # cardInHand stored object is drawn on canvas according to its rank and suit
            cardInHand.draw(canvas, (pos[0] + pos[0] * card, pos[1]))

# define deck class 
class Deck:
    def __init__(self):
        self.deck = []	# create a Deck object
        for s in SUITS:
            for r in RANKS:
                self.deck.append(Card(s,r)) # and populate the list with Card objects; each is given a suit and rank

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        # a card is removed from the deck using .pop method to prevent cards copies being drawn
        return self.deck.pop(random.randrange(len(self.deck)))
    
    def __str__(self):
        deck = ""
        for c in self.deck:
            deck += str(c) + " "
        return "Deck contains " + deck	# return a string representing the deck

#define event handlers for buttons
def deal():
    global game_deck, player, dealer, houseScore, outcome, in_play
    
    #if the game is in progress, and player presses "Deal" button, player is resigned and House scores one point
    # in_play is set to False so that next pressing of "Deal" button starts new game
    if in_play == True:
        outcome = "Player resigned."
        houseScore += 1
        in_play = False
    else:
        #if new game is started, set starting values and shuffle the deck
        game_deck = Deck()
        player = Hand()
        dealer = Hand()
        game_deck.shuffle()
        outcome = "Hit or stand?"
        
        #deal two cards to player and the dealer
        player.add_card(game_deck.deal_card())
        player.add_card(game_deck.deal_card())
        dealer.add_card(game_deck.deal_card())
        dealer.add_card(game_deck.deal_card())
        in_play = True #this one lets the program know the game is in progress

def hit():
    global in_play, outcome, houseScore, playerScore
    # if the hand is in play, hit the player
    if player.get_value() <= 21:
        player.add_card(game_deck.deal_card())
        
        if player.get_value() > 21:
        # if busted, assign a message to outcome, update in_play and dealer score
            outcome = "You busted with hand " + str(player.get_value())
            houseScore += 1
            in_play = False
        
def stand():
    global outcome, houseScore, playerScore, in_play
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # do this if the game is in progress...
    if in_play == True:
        while dealer.get_value() < 17: # while dealer's hand total is less than 17
            if dealer.get_value() > 21: # if over 21 dealer busted and player gets a point
                playerScore += 1
                outcome = "Dealer busted with hand " + str(dealer.get_value()) + "."
                in_play = False # tell the program game is over
            
            # if dealer's still in play
            elif dealer.get_value() >= 17 and dealer.get_value() <= 21:
                
                # dealer also wins ties
                if dealer.get_value() >= player.get_value():
                    houseScore += 1
                    outcome = "Dealer wins with hand " + str(dealer.get_value()) + "."
                    in_play = False
                
                # player wins if dealer's hand is weaker
                else:
                    playerScore += 1
                    outcome = "Player wins with hand " + str(player.get_value()) + "."
                    in_play = False
            
            # if dealer's hand total is less than 17, draw new card
            else:
                dealer.add_card(game_deck.deal_card())
        
        # if dealer's hand is greater than 17, stop /while/ loop and check who wins
        else:
            if dealer.get_value() > 21:
                playerScore += 1
                outcome = "Dealer busted with hand " + str(dealer.get_value()) + "."
                in_play = False
            else:
                if dealer.get_value() >= player.get_value():
                    houseScore += 1
                    outcome = "Dealer wins with hand " + str(dealer.get_value()) + "."
                    in_play = False
                else:
                    playerScore += 1
                    outcome = "Player wins with hand " + str(player.get_value()) + "."
                    in_play = False
                        
    # ... otherwise warn the player to start a new game
    else:
        outcome = "Deal for new game."

# draw handler    
def draw(canvas):
    # draws various messages and player/dealer scores
    canvas.draw_text('Blackjack',(80, 65),40,"White")
    canvas.draw_text("Dealer: " + str(houseScore),(470,50),24,"Yellow")
    canvas.draw_text("Player: " + str(playerScore),(470,80),24,"Yellow")
    canvas.draw_text(outcome,(250,550),28,"White")
    
    # draws cards
    dealer.draw(canvas, cardPosition)
    player.draw(canvas, [cardPosition[0],cardPosition[1] + 200])
    
    # if play is in progress, draws card back over dealer's first card
    if in_play == True:
        #canvas.draw_image(image URL, center_source, width_height_source, center_dest, width_height_dest)
        canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, (cardPosition[0] + CARD_CENTER[0], cardPosition[1] + CARD_CENTER[1]), CARD_SIZE)

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()