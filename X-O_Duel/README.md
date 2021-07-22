I made X-O Duel on my own without help from online. This was created using Python and Pygame. My purpose for making this was to continue developing my Python skills and put what I had taught myself into practice. Originally I only made this a two player game, but soon went back to add in a computer player to play against.

  Rules of the Game:

    -To win, you have to win 3 tic-tac-toe games in a row.
    -If a mini-board is won it will be replaced with the winners mark (X or an O), if it is a draw it will disappear.
    -If neither player gets 3 mini-board wins in a row on the main board, the winner is whoever won the most mini-boards.

About the Computer Player:
 
  The Computer Player will check for severeal situations in the specified order:
  
    -Can either player play to win the main board.
    -Can either player play to win a mini-board.
    -Can either player play to cause two seperate moves on its next turn that would result in a win

  To make the Computer Player act more human-like, there is a small chance every turn that it makes a "mistake" and plays in a random spot instead of checking the above situations.
  
  It will also play randomly if none of the above situations exist.
