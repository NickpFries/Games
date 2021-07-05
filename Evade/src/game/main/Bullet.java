package game.main;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Rectangle;
import java.awt.image.BufferedImage;
import java.util.Random;


// Projectile that doesn't change direction
public class Bullet extends GameObject {

	private Handler handler;
	Random r = new Random();
	public static float hard = 0;
	private BufferedImage grey, red;
	
	public Bullet(int x, int y, ID id, Handler handler) {
		super(x, y, id);
		this.handler = handler;
		
		velX = -8;
		velY = r.nextInt(12)-6;
		
		SpriteSheet ss = new SpriteSheet(Game.sprite_sheet);
		grey = ss.grabImage(2, 4, 16, 16);
		red = ss.grabImage(3, 4, 16, 16);
	}

	@Override
	public void tick() {
		x += velX - hard;
		y += velY;
		
		if(y >= Game.HEIGHT || y <= 0 || x < 0) handler.removeObject(this);
		
		//handler.addObject(new Trail((int)x, (int)y, ID.Trail, Color.LIGHT_GRAY, 16, 16, 0.05f, handler));
	}

	@Override
	public void render(Graphics g) {
	/*	if(HUD.score > 3980 ) {
			g.setColor(new Color(166, 0, 0));
			if(HUD.score > 4220 && HUD.score < 4280 && HUD.score/10 % 2 == 0) {
				g.setColor(Color.LIGHT_GRAY);
			}
			else if(HUD.score > 4560 && HUD.score < 4620 && HUD.score/10 % 2 == 0) {
				g.setColor(Color.LIGHT_GRAY);
			}
			else if(HUD.score > 4885 && HUD.score < 4945 && HUD.score/10 % 2 == 0) {
				g.setColor(Color.LIGHT_GRAY);
			}
			else if(HUD.score > 5300)
				g.setColor(Color.LIGHT_GRAY);
		}
		else
			g.setColor(Color.LIGHT_GRAY);
		g.fillRect((int)x, (int)y, 16, 16);*/
		
		if(HUD.score > 3980 && HUD.score < 5300) {
			g.drawImage(red, (int)x, (int)y, null);
			if(HUD.score > 4220 && HUD.score < 4280 && HUD.score/10 % 2 == 0) {
				g.drawImage(grey, (int)x, (int)y, null);
			}
			else if(HUD.score > 4560 && HUD.score < 4620 && HUD.score/10 % 2 == 0) {
				g.drawImage(grey, (int)x, (int)y, null);
			}
			else if(HUD.score > 4885 && HUD.score < 4945 && HUD.score/10 % 2 == 0) {
				g.drawImage(grey, (int)x, (int)y, null);
			}
		}
		else
			g.drawImage(grey, (int)x, (int)y, null);
	}

	public Rectangle getBounds() {
		return new Rectangle((int)x, (int)y, 16, 16);
	}

	public boolean getSafe() {
		return false;
	}
}
