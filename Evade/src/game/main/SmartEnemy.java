package game.main;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Rectangle;
import java.awt.image.BufferedImage;


// Enemy that follows the player but at a slow speed
public class SmartEnemy extends GameObject {

	private Handler handler;
	private GameObject player;
	private int safe = 70;
	public static float speed;
	private BufferedImage player_image;
	
	public SmartEnemy(float x, float y, ID id, Handler handler) {
		super(x, y, id);
		this.handler = handler;
		
		for(int i = 0; i < handler.object.size(); i++) {
			if(handler.object.get(i).getID() == ID.Player) player = handler.object.get(i);
		}
		
		SpriteSheet ss = new SpriteSheet(Game.sprite_sheet);
		player_image = ss.grabImage(1, 4, 16, 16);
		
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
		
		velX = speed * ((-1/distance) * diffX);
		velY = speed * ((-1/distance) * diffY);
		
		handler.addObject(new Trail((int)x, (int)y, ID.Trail, Color.MAGENTA, 16, 16, 0.03f, handler));
	}

	@Override
	public void render(Graphics g) {
		//g.setColor(Color.magenta);
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
