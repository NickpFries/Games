SpaceInvaders was coded using Python and PyGame using this tutorial: https://www.youtube.com/watch?v=Q-__8Xw9KTM&list=PLSaDnN0zFg-VsOeyfGamc5FruPwqlllzN&index=10

I did this as a day project to help myself learn Python and PyGame. This was my first program with PyGame and my second with Python.

I changed much of the code and added some new elements.


Changes I made:

Added the powerups.py file and implemented the powerups in main.py adding in 4 unique powerups.

"HealthBoost" and "ExtraLife" powerups won't spawn if that attribute is already at its maximum.

Window was changed to be fullscreen rather than resizeable.

Many variables in the game are now reliant on the window size rather than an exact number of pixels, this way the game stays the same regardless of the monitor.

Added in the clamp(var, min, max) funciton to help simplify the code.

Added a "Quit" option to the main menu.

Added a pause menu with the ability to restart, resume, or quit.

Lasers despawn after completely exiting screen rather than despawning when the first touch the border.

If an enemy dies, any lasers he shot no longer despawn but continue on as normal.

Enemy spawning has been changed to make the game a better difficulty.

Added additional enemy wave where 5 enemies spawn evenly across the screen at the end of every 8 waves.
