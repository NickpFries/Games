package game.main;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Rectangle;
import java.awt.image.BufferedImage;


// Handles the user controlled player object
public class Player extends GameObject{
	Graphics g;
	Handler handler;
	private boolean immunity = false;
	private int immunityTimer = 100;
	private int red[] = {255,255,255};
	private BufferedImage player_image;
	
	public Player(int x, int y, ID id, Handler handler) {
		super(x, y, id);
		this.handler = handler;
		KeyInput.resetKeys(this);
		
		SpriteSheet ss = new SpriteSheet(Game.sprite_sheet);
		player_image = ss.grabImage(1, 1, 32, 32);
	}
	
	public Rectangle getBounds() {
		return new Rectangle((int)x, (int)y, 32, 32);
	}
	
	public void tick() {
		x += velX;
		y += velY;
		
		x = Game.clamp(x, 0, Game.WIDTH-48);
		y = Game.clamp(y, 0, Game.HEIGHT-68);
		
		if(HUD.shielded()) {
			red[0] = 75; red[1] = 153; red[2] = 141;
		}else{
			red[0] = 255; red[1] = 255; red[2] = 255;
		}
		handler.addObject(new Trail((int)x, (int)y, ID.Trail, new Color(red[0], red[1], red[2]), 32, 32, 0.1f, handler));
		
		if(immunity) {
			immunityTimer--;
			if(immunityTimer == 0) {
				immunityTimer = 50;
				immunity = false;
				red[0] = 255; red[1] = 255; red[2] = 255;
			}
			if(immunity && (immunityTimer/10 + 1) % 2 == 0) {red[0] = 255; red[1] = 255; red[2] = 255;}
			else if(immunity){red[0] = 100; red[1] = 12; red[2] = 12;}
		}
		collision();
	}
	
	private void collision() {
		for(int i = 0; i < handler.object.size(); i++) {
			
			GameObject tempObject = handler.object.get(i);
			if(tempObject.getID() == ID.BasicEnemy || tempObject.getID() == ID.FastEnemy || tempObject.getID() == ID.SmartEnemy ||
					tempObject.getID() == ID.CrazyEnemy || tempObject.getID() == ID.BossOne || tempObject.getID() == ID.Projectile) {
				if(getBounds().intersects(tempObject.getBounds()) && !immunity && !HUD.shielded() && !tempObject.getSafe()) {
					//collision code
					HUD.HEALTH = HUD.HEALTH - 1;
					immunity = true;
					red[0] = 100; red[1] = 12; red[2] = 12;
					if(tempObject.getID() == ID.Projectile) {
						handler.object.remove(tempObject);
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
			else if(tempObject.getID() == ID.Wall) {
				if(getBounds().intersects(tempObject.getBounds())) {
					//We hit a wall, the wall is currently tempObject
					Wall wall = (Wall)tempObject;
					if(wall.xRange((int)x) && !wall.xRange((int)x + 32))
						x += KeyInput.speed;
					if(!wall.xRange((int)x) && wall.xRange((int)x + 32))
						x -= KeyInput.speed;
					if(wall.yRange((int)y) && !wall.yRange((int)y + 32))
						y += KeyInput.speed;
					if(!wall.yRange((int)y) && wall.yRange((int)y + 32))
						y -= KeyInput.speed;
				}
			}
		}
	}
	
	public void render(Graphics g) {
		if(!immunity && !HUD.shielded())
			g.drawImage(player_image, (int)x, (int)y, null);
		else {
			g.setColor(new Color(red[0], red[1], red[2]));
			g.fillRect((int)x, (int)y, 32, 32);
		}
	}
	
	public boolean getSafe() {
		return true;
	}
}
