# -----------
# User Instructions
#
# Modify the hand_rank function so that it returns the
# correct output for the remaining hand types, which are:
# full house, flush, straight, three of a kind, two pair,
# pair, and high card hands.
#
# Do this by completing each return statement below.
#
# You may assume the following behavior of each function:
#
# straight(ranks): returns True if the hand is a straight.
# flush(hand):     returns True if the hand is a flush.
# kind(n, ranks):  returns the first rank that the hand has
#                  exactly n of. For A hand with 4 sevens
#                  this function would return 7.
# two_pair(ranks): if there is a two pair, this function
#                  returns their corresponding ranks as a
#                  tuple. For example, a hand with 2 twos
#                  and 2 fours would cause this function
#                  to return (4, 2).
# card_ranks(hand) returns an ORDERED tuple of the ranks
#                  in a hand (where the order goes from
#                  highest to lowest rank).
#
# Since we are assuming that some functions are already
# written, this code will not RUN. Clicking SUBMIT will
# tell you if you are correct.

# ranks_map = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10,
#              '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4,
#              '3': 3, '2': 2}
import random


def deal(numhands, n=5, deck=[r + s for r in '23456789TJQKA' for s in 'SHDC']):
    random.shuffle(deck)
    # hands = []
    # currCard = 0
    # for hand in range(numhands):
    #     hands.append(deck[currCard:(currCard + n)])
    # return hands
    return [deck[n * i:n * (i + 1)] for i in range(numhands)]


def poker(hands):
    "Return the best hand: poker([hand,...]) => [hand,..]"
    return allmax(hands, key=hand_rank)


def allmax(iterable, key=None):
    "Return a list of all items equal to the max of the iterable."
    result, maxval = [], None
    key = key or (lambda x: x)
    for item in iterable:
        val = key(item)
        if not result or val > maxval:
            result, maxval = [item], val
        elif val == maxval:
            result.append(item)
    return result


def hand_rank(hand):
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):            # straight flush
        return (8, max(ranks))
    elif kind(4, ranks):                           # 4 of a kind
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):        # full house
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):                              # flush
        return (5, ranks)
    elif straight(ranks):                          # straight
        return (4, ranks[0])
    elif kind(3, ranks):                           # 3 of a kind
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):                           # kind
        return (1, kind(2, ranks), ranks)
    else:                        # high card
        return (0, ranks)


def card_ranks(hand):
    # return (tuple(sorted([ranks_map[card[0]] for card in hand], reverse=True)))
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    ranks.sort(reverse=True)
    return [5, 4, 3, 2, 1] if(ranks == [14, 5, 4, 3, 2]) else ranks


def straight(ranks):
    "if all cards are in sequence"
    return ranks == range(max(ranks), min(ranks) - 1, -1)


def flush(hand):
    "if all cards from same suit"
    return len(set([s for r, s in hand])) == 1


def kind(n, ranks):
    '''
    returns the first rank that the hand has
    exactly n of. For A hand with 4 sevens
    this function would return 7.
    '''
    distinct_ranks = set(ranks)
    for rank in distinct_ranks:
        if(ranks.count(rank) == n):
            return rank
    return None


def two_pair(ranks):
    '''
    if there is a two pair, this function
    returns their corresponding ranks as a
    tuple. For example, a hand with 2 twos
    and 2 fours would cause this function
    to return (4, 2).
    '''
    distinct_ranks = set(ranks)
    pairs = []
    for rank in distinct_ranks:
        if(ranks.count(rank) == 2):
            pairs.append(rank)
    if(len(pairs) == 2):
        return tuple(pairs)
    return None


def hand_percentages(n=700 * 1000):
    "Sample n random hands and print out table of percentages for each type of hand"
    hand_names = ['high card', 'pair', '2 pair', '3 kind',
                  'straight', 'Flush', 'Full house', '4 kind', 'Straight flush']

    counts = [0] * 9
    for i in range(n / 10):
        for hand in deal(10):
            ranking = hand_rank(hand)[0]
            counts[ranking] += 1
    for i in reversed(range(9)):
        print "%14s: %6.3f %%" % (hand_names[i], 100. * counts[i] / n)


def test():
    "Test cases for the functions in poker program"
    sf = "6C 7C 8C 9C TC".split()  # Straight Flush
    fk = "9D 9H 9S 9C 7D".split()  # Four of a Kind
    fh = "TD TC TH 7C 7D".split()  # Full House
    tp = "5S 5D 9H 9C 6S".split()  # Two pairs
    al = "AC 2D 4H 3D 5S".split()  # Ace-Low Straight
    assert straight(card_ranks(al)) is True
    fkranks = card_ranks(fk)
    tpranks = card_ranks(tp)
    assert kind(4, fkranks) == 9
    assert kind(3, fkranks) is None
    assert kind(2, fkranks) is None
    assert kind(1, fkranks) == 7
    assert straight([9, 8, 7, 6, 5]) is True
    assert straight([9, 8, 7, 7, 5]) is False
    # print(poker([sf, fk, fh]))
    assert poker([sf, fk, fh]) == [sf]
    assert poker([fk, fh]) == [fk]
    assert poker([fh, fh]) == [fh, fh]
    assert poker([sf]) == [sf]
    assert poker([sf] + 99 * [fh]) == [sf]
    assert hand_rank(sf) == (8, 10)
    assert hand_rank(fk) == (7, 9, 7)
    assert hand_rank(fh) == (6, 10, 7)
    sf1 = "6C 7C 8C 9C TC".split()  # Straight Flush
    sf2 = "6D 7D 8D 9D TD".split()  # Straight Flush
    assert poker([sf1, sf2, fk, fh]) == [sf1, sf2]
    return 'tests pass'


# print(hand_rank("2D 3H 9S 5C 7D".split()))
# print(hand_rank("2D 2H 4S 4C 7D".split()))
print(test())
hand_percentages(5000)
# print(two_pair([10, 10, 5, 5, 2]))
