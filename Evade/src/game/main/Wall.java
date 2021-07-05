package game.main;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Rectangle;
import java.util.Random;

// Creates a wall that the player can't go through and missiles will despawn when hitting it
public class Wall extends GameObject {

	private Handler handler;
	Random r= new Random();
	public static boolean bossTwo = true;
	
	public Wall(int x, int y, ID id, Handler handler) {
		super(x, y, id);
		this.handler = handler;
	}

	@Override
	public void tick() {
		if(!bossTwo)
			handler.removeObject(this);
		collision();
	}

	@Override
	public void render(Graphics g) {
		if(HUD.score > 10430) g.setColor(new Color(30, 0, 70));
		else g.setColor(Color.gray);
		g.fillRect((int)x, (int)y, 16, 96);
	}

	public Rectangle getBounds() {
		return new Rectangle((int)x, (int)y, 16, 96);
	}
	
	public boolean xRange(int x) {
		if(x > this.x && x < this.x + 16)
			return true;
		return false;
	}
	
	public boolean yRange(int y) {
		if(y > this.y && y < this.y + 96)
			return true;
		return false;
	}
	
	public boolean getSafe() {
		return true;
	}
	
	//Delete projectiles when they hit a wall
	private void collision() {
		for(int i = 0; i < handler.object.size(); i++) {
			GameObject tempObject = handler.object.get(i);
			if(tempObject.getID() == ID.Projectile)
				if(getBounds().intersects(tempObject.getBounds())) {
					handler.removeObject(tempObject);
					try {
						Missile m = (Missile)tempObject;
						m.kill();
					} catch(Exception e) {
						//Projectile was not a missile, cannot kill
						//No need to do anything
					}
				}
		}
	}
}
