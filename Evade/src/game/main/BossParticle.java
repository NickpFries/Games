package game.main;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Rectangle;
import java.util.Random;


// Background particles that show up during boss #1, no collisions possible
public class BossParticle extends GameObject {

	private Handler handler;
	Random r = new Random();
	Color c;
	
	
	public BossParticle(int x, int y, ID id, Handler handler) {
		super(x, y, id);
		this.handler = handler;
		if(HUD.score < 8000)
			c = new Color(0f, 0.5f, 0.5f, 0.08f);
		else
			c = new Color(1f, 0.7f, 0f, 0.07f);
		
		velX = 0;
		velY = (4+r.nextInt(2));
	}

	@Override
	public void tick() {
		x += velX;
		y += velY;
		
		if(y > Game.HEIGHT+32)
			handler.removeObject(this);
		handler.addObject(new Trail((int)x, (int)y, ID.Trail, c, 16, 16, 0.02f, handler));
	}

	@Override
	public void render(Graphics g) {
		if(HUD.score > 10430)
			c = new Color(0f, 0.8f, 0f, 0.07f);
		g.setColor(c);
		g.fillRect((int)x, (int)y, 16, 16);
	}

	public Rectangle getBounds() {
		return new Rectangle((int)x, (int)y, 16, 16);
	}
	
	public boolean getSafe() {
		return true;
	}
}
