This was my first ever created game. It was created in java with help from this tutorial series: https://www.youtube.com/watch?v=1gir2R7G9ws
I did this project to practice Java and to learn more about how games work. The game was made over the course of about a week.

Changes I made:

Player health switched to lives, rather than losing health for every tick the player is colliding with an enemy the player only loses one life.

Through out the game, there are points where the player recieves and addition life or has their lives completely refiilled.

After losing a life, the player is immune to damage for a short period.

    -During this period, the player's texture flashes white and red to indicate that damage was taken.

The player cannot take damage immediatly from objects that randomly spawn in, rather the enemy will be harmless for about 1 second.

Added in additional types of enemies and additional spawn waves including: Boss #2, missiles, crazy enemies, smart bullets, walls.

    -Walls and missiles spawn for Boss #2.
    -Missiles track the player and are fast, but cannot turn around.
    -Missiles despawn when hitting walls.
    -The player cannot move through the wall.
    -Crazy Enemies have random and fast movement.
    -Smart bullets are projectiles that slightly curve towards the player.

Added in several difficulty levels.

    -Affects number of lives.
    -Affects Shield duration.
    -Affects enemy and player movement speed.

Added in a shield:

    -Player can't take damage while shielding.
    -Shield has short duration but recharges.
    -Duration of shield changes based on difficulty level.
    -If player uses the shield while it is out of power it is useless.
    -When using the shield and it has power still, the player's texture will change to light blue to indicate they are shielded.
    
Enemies spawn in beat with the music.

Boss #1 changes:

    -Moves faster the longer he is alive.
    -Shoots bullets at a higher rate the longer he is alive.
    -Shoots shotgun-like wave of bullets in beat with music.
    -Color of Boss #1 bullets change in beat with music.
    -Player gaines an additional life twice while fighting the boss.
    -Player's lives compleletly refilled when Boss #1 despawns.
    

    
