package game.main;

import java.awt.image.BufferedImage;


// Handles the sprite sheet which gives game objects their textures
public class SpriteSheet {

	private BufferedImage sprite;
	
	public SpriteSheet(BufferedImage ss) {
		this.sprite = ss;
	}
	
	public BufferedImage grabImage(int col, int row, int width, int height) {
		BufferedImage img = sprite.getSubimage((row*32)-31, (col*32)-31, width, height);
		return img;
	}
	
}
