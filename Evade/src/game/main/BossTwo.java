package game.main;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Rectangle;
import java.util.Random;


// Handles Boss #2, which is when walls and missiles spawn
public class BossTwo extends GameObject {

	private Handler handler;
	Random r= new Random();
	public static boolean bossTwo = true;
	
	public BossTwo(int x, int y, ID id, Handler handler) {
		super(x, y, id);
		this.handler = handler;
		handler.addObject(new Wall(Game.WIDTH/2 -32, 100, ID.Wall, handler));
		handler.addObject(new Wall(Game.WIDTH/2 -32, 300, ID.Wall, handler));
	}

	@Override
	public void tick() {
		if(HUD.score < 10430) {
			if(HUD.score % 30 == 0 && HUD.score % 60 != 0)
				handler.addObject(new Missile(0, r.nextInt(Game.HEIGHT -32), ID.Projectile, handler));
			if(HUD.score % 60 == 0)
				handler.addObject(new Missile(Game.WIDTH + 32, r.nextInt(Game.HEIGHT -32), ID.Projectile, handler));
			if(HUD.score == 1100) {
				bossTwo = false;
				handler.removeObject(this);
			}
		}
		else{
			if(HUD.score % 60 == 0 && HUD.score % 120 != 0) {
				handler.addObject(new Missile(0, r.nextInt(Game.HEIGHT -32), ID.Projectile, handler));
				handler.addObject(new Missile(0, r.nextInt(Game.HEIGHT -32), ID.Projectile, handler));
				handler.addObject(new Missile(0, r.nextInt(Game.HEIGHT -32), ID.Projectile, handler));
			}
			if(HUD.score % 120 == 0) {
				handler.addObject(new Missile(Game.WIDTH + 32, r.nextInt(Game.HEIGHT -32), ID.Projectile, handler));
				handler.addObject(new Missile(Game.WIDTH + 32, r.nextInt(Game.HEIGHT -32), ID.Projectile, handler));
				handler.addObject(new Missile(Game.WIDTH + 32, r.nextInt(Game.HEIGHT -32), ID.Projectile, handler));
			}
		}
		
		if(HUD.score > 11430) {
			bossTwo = false;
			handler.removeObject(this);
		}
	}

	@Override
	public void render(Graphics g) {

	}

	public Rectangle getBounds() {
		return new Rectangle(0, 0, 0, 0);
	}
	
	public boolean getSafe() {
		return true;
	}

}
