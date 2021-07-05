package game.main;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Rectangle;
import java.awt.image.BufferedImage;


// Bullet that travels across screen and curves towards the player
public class SmartBullet extends GameObject {

	private Handler handler;
	private GameObject player;
	private int safe = 0;
	private Color c;
	private BufferedImage player_image;
	
	public SmartBullet(float x, float y, ID id, Handler handler) {
		super(x, y, id);
		this.handler = handler;
		
		for(int i = 0; i < handler.object.size(); i++) {
			if(handler.object.get(i).getID() == ID.Player) player = handler.object.get(i);
		}
		c = Color.magenta;
		
		SpriteSheet ss = new SpriteSheet(Game.sprite_sheet);
		player_image = ss.grabImage(1, 4, 16, 16);
	}

	@Override
	public void tick() {
		x += velX;
		y += velY;
		
		if(safe != 0)
			safe--;

		float diffY = y - player.getY() - 8;
		float distance = (float)Math.sqrt((x-player.getX()) * (x-player.getX()) + (y-player.getY()) * (y-player.getY()));
		
		velX = -6;
		velY = 5f * ((-1/distance) * diffY);
		
		//handler.addObject(new Trail((int)x, (int)y, ID.Trail, c, 16, 16, 0.06f, handler));
		if(x < -30)
			handler.removeObject(this);
	}

	@Override
	public void render(Graphics g) {
		//g.setColor(c);
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
