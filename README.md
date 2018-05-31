# LongestRookCheckmate
Finds the longest optimal checkmate for king and rook vs king.

# Running this code on your machine:
1. Have a functioning Python 2.7+ version installed
2. Clone this repository
3. Open a terminal and cd into src
4. Run "python gen_positions.py"

# Problem Explanation
A rook and king vs king will always be a forced win for the side with the rook, no matter where the pieces exist or which side it is to move. The only exceptions to this are positions where the defending king can immediately capture the rook and positions with stalemate on the board.

Since every normal position is a forced win, then each position evaluates to some "mate in x" value, where x is the lowest number assuming perfect play from both sides. Perfect play is defined as the attacking side aiming to checkmate in as few moves as possible, and the defending side aiming to survive for as many moves as possible.

For the finite number of positions with an optimal "mate in x" value, there must be some maximum value of x. The goal of this program to figure out what that value is. Then, it can be claimed that every rook endgame can be won in x moves or less, for the lowest true value of x.

# Explanation of the Code
First and foremost, this program does not use any third party libraries, so all of the chess logic is hardcoded. The rook and king are pretty simple pieces, and I wanted to avoid the overhead of using a chess library to represent the positions. For obvious reasons, I'm not using something like a chess engine or endgame tablebase (since this program is essentially creating a tablebase of its own!).

With that being said, all of the positions are just represented via a dictionary, containing coordinates of where that specific piece exists (0 to 7 for both axes). All of the moves, captures, checks, etc are manually calculated manually (and I've tried to keep all of that work in position_util.py to keep things cleaner).

The first step is to generate every possible position with the three pieces (upperbound of about half a million). Then, I filter out all of the garbage positions (illegal, immediate rook captures, stalemates, etc). Some of this work is done in the loop itself that generates the positions (such as checking for adjacent kings). All of this work is done in gen_positions.py.

After the generation/filtering of the positions, I can be sure that I am only left with legal, "mate in x" style positions. It's at this point that I should mention that I am measuring in half moves to make categorizing easier. So all positions with black to move are an even number of moves from checkmate (including 0) and all positions with white to move are an odd number of moves from checkmate.

From here, I just categorize from the bottom up. Identify the mate in 0 positions (checkmate on the board) by looking for check and legal move count. Each time I identify the mating depth of a position, I move it (pop) from the unsorted structure to the mating depth structure. I can be sure the problem is solved when I run out of unsorted positions.

I identify the mate in 1s by checking to see if a given position can transition into any mate in 0 position (if white can deliver checkmate, white will deliver checkmate). I check for mate in 2s by doing nearly the opposite. If black can't avoid escaping the forced mating structure, then obviously black won't. Mate in 3s will have the same logic as mate in 1s, mate in 4s the same as mate in 2s, etc. Eventually, all of the positions will be sorted and we'll have the answer.

# Examples of Deepest Cases
Spoiler, there are 3056 positions at the deepest level of 32 half moves (16 full moves), all of which are obviously black to move (assuming black is defending). None are particularly special (that I've found), but here are just a few examples (FENs):

8/1R6/4k3/8/8/8/8/K7 b - - 0 1  
8/8/5R2/8/1k6/8/K7/8 b - - 0 1  
7K/8/8/8/8/2R2k2/8/8 b - - 0 1  
