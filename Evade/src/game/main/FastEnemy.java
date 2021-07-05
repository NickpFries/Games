package game.main;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Rectangle;
import java.awt.image.BufferedImage;


// Enemy that is fast and moves more veritcally then horizontally
public class FastEnemy extends GameObject {

	private Handler handler;
	private int safe = 70;
	public static int speed = 1;
	private BufferedImage player_image;
	
	public FastEnemy(int x, int y, ID id, Handler handler) {
		super(x, y, id);
		this.handler = handler;
		
		velX = speed;
		velY = 3*speed;
		
		SpriteSheet ss = new SpriteSheet(Game.sprite_sheet);
		player_image = ss.grabImage(1, 3, 16, 16);
	}

	@Override
	public void tick() {
		x += velX;
		y += velY;
		
		if(safe != 0)
			safe--;
		
		if(y <= 0 || y >= Game.HEIGHT - 48) velY *= -1;
		if(x <= 0 || x >= Game.WIDTH - 32) velX *= -1;
		
		handler.addObject(new Trail((int)x, (int)y, ID.Trail, Color.BLUE, 16, 16, 0.03f, handler));
	}

	@Override
	public void render(Graphics g) {
		//g.setColor(Color.cyan);
		//g.fillRect((int)x, (int)y, 16, 16);
		g.drawImage(player_image, (int)x, (int)y, null);
		
	}

	public Rectangle getBounds() {
		return new Rectangle((int)x, (int)y, 16, 16);
	}
	
	public boolean getSafe() {
		if(safe == 0)
			return false;
		return true;
	}
}
