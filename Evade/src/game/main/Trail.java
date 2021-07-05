package game.main;

import java.awt.AlphaComposite;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Rectangle;


// Trail that follows enemies, player, and missiles. Purely for looks, can't collide with anything
public class Trail extends GameObject {

	private float alpha = 1;
	private Handler handler;
	private Color color;
	private int width, height;
	private float life;
	private boolean gor = false;
	private GameObject go;
	
	public Trail(int x, int y, ID id, Color color, int width, int height, float life, Handler handler) {
		super(x, y, id);
		this.color = color;
		this.width = width;
		this.height = height;
		this.life = life;
		this.handler = handler;
	}
	
	public Trail(int x, int y, ID id, Color color, int width, int height, float life, Handler handler, GameObject go) {
		super(x, y, id);
		this.color = color;
		this.width = width;
		this.height = height;
		this.life = life;
		this.handler = handler;
		gor = true;
		this.go = go;
	}

	@Override
	public void tick() {
		if(alpha > life) {
			alpha -= life-0.001f;
		}
		else
			handler.removeObject(this);
	}

	@Override
	public void render(Graphics g) {
		Graphics2D g2d = (Graphics2D) g;
		g2d.setComposite(makeTransparent(alpha));
		if(gor) g.setColor(Missile.c2);
		else g.setColor(color);
		g.fillRect((int)x, (int)y, width, height);
		
		g2d.setComposite(makeTransparent(1));
		if(gor) go.render(g);
	}

	private AlphaComposite makeTransparent(float alpha) {
		int type = AlphaComposite.SRC_OVER;
		return AlphaComposite.getInstance(type, alpha);
	}
	
	@Override
	public Rectangle getBounds() {
		return null;
	}
	
	public boolean getSafe() {
		return true;
	}
}
