package game.main;

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Rectangle;
import java.awt.image.BufferedImage;
import java.util.Random;


// First boss of the game, moves up and down while spawning bullets randomly
public class BossOne extends GameObject {

	private Handler handler;
	private int delay = 30;
	private boolean fight = false, dead = false;
	Random r= new Random();
	private int bulletNum = 0;
	private int fireRate = 10;
	private int deathTimer = 85;
	public static boolean bossOne = true;
	private BufferedImage player_image;
	
	public BossOne(int x, int y, ID id, Handler handler) {
		super(x, y, id);
		this.handler = handler;
		
		velX = -6;
		velY = 0;
		
		SpriteSheet ss = new SpriteSheet(Game.sprite_sheet);
		player_image = ss.grabImage(2, 1, 95, 95);
	}

	@Override
	public void tick() {
		x += velX;
		y += velY;
		//Movement
		if(y <= 0 || y >= Game.HEIGHT - 133) velY *= -1;
		if(x < 600 && !dead) {
			x = 600;
			velX = 0;
			fight = true;
		}
		//Pausing after coming on screen
		if(fight) {
			delay--;
			if(delay == 0) {
				velY = 2;
				fight = false;
				for(int i = 0; i < 20; i++)
					handler.addObject(new Bullet((int)(x+48), (int)(y+48), ID.Projectile, handler));
			}
		}
		//Shoot bullets
		if(fight == false && x == 600 && !dead) {
			
			if(HUD.score == 5295 || HUD.score == 2980 || HUD.score == 3300 || HUD.score == 3640 || HUD.score == 3970 || HUD.score == 5620 || HUD.score == 5960 || HUD.score == 6290)
				for(int i = 0; i < 17; i++) handler.addObject(new Bullet((int)(x+48), (int)(y+48), ID.Projectile, handler));
			
			int spawn = r.nextInt(fireRate);
			if(spawn == 0) {
				handler.addObject(new Bullet((int)(x+48), (int)(y+48), ID.Projectile, handler));
				bulletNum++;
				if(bulletNum == (int)2*(20 + 10*(12-fireRate))) {
					if(fireRate > 6) {
						fireRate--;
						bulletNum = 0;
						velY = velY*1.3f;
					}
					else {
						bulletNum = 0;
					}
				}
			}
		}
		if(HUD.score == 3970 || HUD.score == 5295) HUD.HEALTH++;
		if(HUD.score == 6600) dead = true;
		//Despawn off screen
		if(dead) {
			deathTimer--;
			if(deathTimer < 0)
				velX = -8;
			if(x < -100)
				HUD.HEALTH = HUD.setHealth;
			if(x < -1200) {
				handler.removeObject(this);
				bossOne = false;
			}
		}
	}

	@Override
	public void render(Graphics g) {
		//g.setColor(Color.red);
		//g.fillRect((int)x, (int)y, 96, 96);
		g.drawImage(player_image, (int)x, (int)y, null);
		
		//Display "Lives Refilled!" Once boss is off the screen
		if(x < -100) {
			g.setColor(Color.white);
			g.setFont(new Font("arial", 1, 20));
			g.drawString("Lives Refilled!", Game.WIDTH/2 - 60, 50);
		}
		
	}

	public Rectangle getBounds() {
		return new Rectangle((int)x, (int)y, 96, 96);
	}
	
	public boolean getSafe() {
		return false;
	}

}
