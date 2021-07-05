package game.main;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Rectangle;


// Projectile that is fast and homing towards the player but can't turn around
public class Missile extends GameObject {

	private Handler handler;
	private GameObject player;
	private int safe = 0;
	private boolean right;
	private boolean dead;
	public static float hard = 0;
	public static Color c, c2;
	
	public Missile(float x, float y, ID id, Handler handler) {
		super(x, y, id);
		this.handler = handler;
		if(x <= Game.WIDTH/2) right = false;
		if(x > Game.WIDTH/2) right = true;
		for(int i = 0; i < handler.object.size(); i++) {
			if(handler.object.get(i).getID() == ID.Player) player = handler.object.get(i);
		}
		c = Color.red;
		c2 = Color.white;
	}

	@Override
	public void tick() {
		x += velX;
		y += velY;
		
		if(safe != 0)
			safe--;
		
		float diffX = x - player.getX() - 8;
		float diffY = y - player.getY() - 8;
		float distance = (float)Math.sqrt((x-player.getX()) * (x-player.getX()) + (y-player.getY()) * (y-player.getY()));
		
		velX = (7f+hard) * ((-1/distance) * diffX);
		velY = (4f+hard) * ((-1/distance) * diffY);
		
		if(!right) velX = Game.clamp(velX, 5, 30);
		if(right) velX = Game.clamp(velX, -30, -5);
		
		handler.addObject(new Trail((int)x, (int)y+5, ID.Trail, c2, 6, 6, 0.03f, handler, this));
		
		if(x < -50 || x > Game.WIDTH + 70) {
			handler.removeObject(this);
			dead = true;
		}
		if(HUD.score > 10430) {
			c = new Color(255, 187, 0);
			c2 = Color.red;
		}
	}

	@Override
	public void render(Graphics g) {
		if(!dead) {
				g.setColor(c);
			g.fillRoundRect((int)x, (int)y, 20, 20, 30, 5);
		}
	}

	public Rectangle getBounds() {
		return new Rectangle((int)x, (int)y, 18, 18);
	}

	public boolean getSafe() {
		return false;
	}
	
	public void kill() {
		dead = true;
	}
}//10430
