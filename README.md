# Connect-4-AI-Game
This is a artificial intelligence game which is $ Connect Game using pygame to design graphical mode

First of all, we go to the program itself 

In the firts step we choose between two game mode :  (AI vs Human) or (AI vs AI) :

![AI-AI or Human-AI](https://github.com/6amir6hosein6/Connect-4-AI-Game/blob/master/image/1.png)

In the second step, we choose between two other options to choose which one to start first :

![AI or Human](https://github.com/6amir6hosein6/Connect-4-AI-Game/blob/master/image/2.png)
:
In the third step, we determine how hard the artificial intelligence should be :

![Easy or Hard](https://github.com/6amir6hosein6/Connect-4-AI-Game/blob/master/image/3.png)

and then game will start :  By choosing one of the squares with number above, the bead will enter that column:

![Choose column](https://github.com/6amir6hosein6/Connect-4-AI-Game/blob/master/image/5.png)

After that artificial intelligence will start thinking for its own movement, and then it will choose that.
(The thinking time is proportional to the selected difficulty level)

After several steps, as you can see, artificial intelligence will win the game

![Choose column](https://github.com/6amir6hosein6/Connect-4-AI-Game/blob/master/image/6.png)

## Documentation:

### playGame(bo):
#### Inputs:

bo : The board of game

This function is the mainest function in the project witch after calling this function the graphic model og game will start and after choosing the type of game by user the game will start

the option of game contains:

1 - AI vs Human

I-Firstone : human

II-Firstone : AI

2 - AI vs human

### human_choose(bo, col):
#### Inputs:

bo : The board of game

col : choosen culomn by user

This function get the choosen column by user and put in the board and check if the user is winner or not and then give the turn to the other player

### check_piece():
#### Inputs:

bo : The board of game

column : The current column that will check

row : The current row that will check

length : the size of pice we want (defult=4)

checks given the piece of board and return the piece that there is some winner inside it ;-)

### find_winner():
#### Inputs:

bo : The board of game


length : the size of pice we want (defult=4)

This funvtion will ittrate all col and row by giving to check_piece() and check if exist a winner of not
Output:

the winner existing , winner marker(+1 or -1)

### printBoard(bo):
#### Inputs:

bo : The board of game

This function will print the board in terminal as beutiful one ;-)
ai_choose(bo, self, rival):
Inputs:

bo : The board of game

self : Witch AI is this (usage in : AI vs AI)

rival : Who is the rival of AI in this game (AI or human)

This function will di the move of ai by using MiniMAx() function and changes the board and like human_choose() check if the user is winner or not and then give the turn to the other player

### available(bo):
#### Inputs:

bo : The board of game

This function will check if table is full or not

### all_possible_move(bo):
#### Inputs:

bo : The board of game

This function get the board of game and return the all column that the AI can put it's marker in there
Output:

possible : array of all possible moves

### MIN(bo, max_depth, current_depth, alpha , beta)
### MAX(bo, max_depth, current_depth, alpha , beta)
##### Inputs:

bo : The board of game

max_depth : The maximum depth we want to check

current_depth : The current depth we are in now

alpha , beta : in order to Implement the alpha beta method

This function is playing with eachother at the end they will found the best way

### number_of_n_beside(bo, n, who, m):

#### Inputs:

bo : The board of game

n : The looking for goal

who : For witch player we will look

m :The Coefficient

this function is a little compelicated!!
in this function we will ittrate all 4 place of board in order to find the threats and after calculating and summing all of them will use it in MIN() and MAX() function in order to getting the best road
Thanks for reading :-D

