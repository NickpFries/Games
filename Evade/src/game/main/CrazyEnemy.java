package game.main;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Rectangle;
import java.util.Random;


// Enemy that has random movement
public class CrazyEnemy extends GameObject {

	private Handler handler;
	private Random r;
	private int change = 0;
	private int safe = 70;
	
	public CrazyEnemy(int x, int y, ID id, Handler handler) {
		super(x, y, id);
		this.handler = handler;
		this.r = new Random();
		
		velX = 2;
		velY = 2;
	}

	@Override
	public void tick() {
		change++;
		if(change == 15) {
			change = 0;
			velX = r.nextInt(20)-10;
			velY = r.nextInt(20)-10;
		}
		x += velX;
		y += velY;
		if(safe != 0)
			safe--;
		
		x = Game.clamp(x, 0, Game.WIDTH - 48);
		y = Game.clamp(y, 0, Game.HEIGHT - 68);
		
		handler.addObject(new Trail((int)x, (int)y, ID.Trail, Color.green, 16, 16, 0.04f, handler));
	}

	@Override
	public void render(Graphics g) {
		g.setColor(Color.green);
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
