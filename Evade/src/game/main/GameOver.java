package game.main;

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.Random;

import game.main.Game.STATE;


// Handles the event of a game over
public class GameOver extends MouseAdapter{
	
	private Game game; 
	private Handler handler;
	Random r = new Random();
	private HUD hud;
	
	public GameOver(Game game, Handler handler, HUD hud) {
		this.game = game;
		this.handler = handler;
		this.hud = hud;
		for(int i = 0; i < 10 ; i++)
			handler.addObject(new MenuParticle(r.nextInt(Game.WIDTH-50), r.nextInt(Game.HEIGHT-50), ID.Particle, handler));
	}
	
	
	public void mousePressed(MouseEvent e) {
		int mx = e.getX();
		int my = e.getY();
		
		if(Game.gameState == STATE.End) {

			if(mouseOver(mx, my, 130, 330, 240, 130)) {
				//Playing again...
				Game.gameState = STATE.Game;
				hud.score(0);
				hud.setLevel(1);
				handler.addObject(new Player(Game.WIDTH/2-32, Game.HEIGHT/2-32, ID.Player, handler));
				handler.addObject(new BasicEnemy(r.nextInt(Game.WIDTH-50), r.nextInt(Game.HEIGHT-50), ID.BasicEnemy, handler));
			}
			
			if(mouseOver(mx, my, 430, 330, 150, 60)) {
				//Going to menu...
				handler.clearEnemies();
				Game.gameState = STATE.Menu;
			}
			
			if(mouseOver(mx, my, 430, 400, 150, 60)) {
				//Exit the game...
				System.exit(1);
			}
		}
	}
	
	public void mouseReleased(MouseEvent e) {
		
	}
	
	private boolean mouseOver(int mx, int my, int x, int y, int width, int height) {
		if(mx > x && mx < x+width) {
			if(my > y && my < y+height) {
				return true;
			}
		}
		return false;
	}
	
	public void tick() {
		
	}
	
	public void render(Graphics g) {
		g.setColor(Color.black);
		g.fillRect(130, 30, 460, 84); //Name
		g.fillRect(130, 160, 460, 100); //Score and level		
		g.fillRect(130, 330, 240, 130); //Play Again
		g.fillRect(430, 330, 150, 60); //Menu
		g.fillRect(430, 400, 150, 60); //Exit
		g.setColor(Color.WHITE);
		Font f = new Font("arial", 1, 75);
		Font f2 = new Font("arial", 1, 40);
		g.setFont(f);
		g.setColor(Color.red);
		g.drawString("GAME OVER", 130, 100);
		g.setColor(Color.white);
		g.setFont(f2);
		g.drawString("Score: " + hud.getScore(), 135, 200);
		g.drawString("Level Reached: " + hud.getLevel(), 135, 250);
		g.drawString("Play Again", 150, 405);
		g.drawString("Menu", 455, 372);
		g.drawString("Exit", 465, 442);
		
		g.setColor(Color.WHITE);
		g.drawRect(130, 330, 240, 130); //Play
		g.drawRect(430, 400, 150, 60); //Exit
		g.drawRect(430, 330, 150, 60); //Menu
	}
	
	
}
