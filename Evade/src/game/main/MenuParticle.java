package game.main;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Rectangle;
import java.util.Random;

// Creates particles to bounce around in the background on the main menu
public class MenuParticle extends GameObject {

	private Handler handler;
	private int safe = 50;
	Random r = new Random();
	private int red = r.nextInt(255);
	private int green = r.nextInt(255);
	private int blue = r.nextInt(255);
	Color c;
	
	
	public MenuParticle(int x, int y, ID id, Handler handler) {
		super(x, y, id);
		this.handler = handler;
		
		velX = 2*(r.nextInt(12) - 10)+5;
		velY = 2*(r. nextInt(12) - 10)+5;
		c = new Color(red, green, blue);
	}

	@Override
	public void tick() {
		x += velX;
		y += velY;
		
		if(safe != 0)
			safe--;
		
		if(y <= 0 || y >= Game.HEIGHT - 48) velY *= -1;
		if(x <= 0 || x >= Game.WIDTH - 32) velX *= -1;
		
		handler.addObject(new Trail((int)x, (int)y, ID.Trail, c, 16, 16, 0.05f, handler));
	}

	@Override
	public void render(Graphics g) {
		g.setColor(c);
		g.fillRect((int)x, (int)y, 16, 16);
		
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
