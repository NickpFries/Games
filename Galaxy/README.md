This was my first program written in Python and also the first app I created. I used it to learn Python as well as Kivy. The code seen here is optimized for desktop, however I also have another version that I optimized for mobile and made into an .apk file.
This is the tutorial I watched to learn Kivy and make this app: https://www.youtube.com/watch?v=l8Imtec4ReQ&list=PLSaDnN0zFg-VsOeyfGamc5FruPwqlllzN&index=9


Changes I made:


Optimized the code for mobile by improving runtime (origianlly there was lagging when running on mobile).
 
    -Reduced run time by lowering number of tiles allowed to be generated 
    -Reduced run time by not updating the ships position every frame. This only applies to the mobile verison because it causes issues on desktop if you resize the window (ships position no longer updates when the window changes).

Created an .apk file.

Added a new way for the tiles to generate: A tile-land generates 5 tiles wide with holes that need to be avoided.

    -When tiles generate this way it requires more to be generated at a single time, resulting in lag for mobile. This is why I created a seperate version that was optimized for mobile.

Added a method that switches between generating tiles the original way and generating tiles in the way described above.

Made the players speed increase with time. Originally I made it increase with score but I didn't like that this made the speed increase exponentially.

Changed the horizontal movement speed to be a ratio of the forward speed so that the player can move fast enough to stay on path even when the forward speed increases.

Changed the hitbox on the player ship. Originally, only one of the triangle corners needed to be on a tile for the player to be alive. Now, one of two positions needs to be on a tile. Rather the front corner, or the midpoint between the lower corners.

    -This prevents the player from being able to stay alive on 2 seperate columns of tiles at once wihtout moving.
    -Player can still survive moving between two tiles that are only connected by a single corner, although it is more challenging.

Added in a "Pause" button that changes to be a "Resume" button after being pressed

    -Audio stops when game is paused

Added in "Exit" button to main menu and to the game over menu.

Changed ships color.
