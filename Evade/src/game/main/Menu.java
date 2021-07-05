package game.main;

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.Random;

import game.main.Game.STATE;

// Handles the main menu and its buttons, as well as the seperate difficulties and the "game over" menu
public class Menu extends MouseAdapter{
	
	private Game game; 
	private Handler handler;
	Random r = new Random();
	private HUD hud;
	public boolean loading = true;
	
	public Menu(Game game, Handler handler, HUD hud) {
		this.game = game;
		this.handler = handler;
		this.hud = hud;
		for(int i = 0; i < 10 ; i++)
			handler.addObject(new MenuParticle(r.nextInt(Game.WIDTH-50), r.nextInt(Game.HEIGHT-50), ID.Particle, handler));
	}
	
	
	public void mousePressed(MouseEvent e) {
		int mx = e.getX();
		int my = e.getY();

		if(Game.gameState == STATE.Select) {
			if(mouseOver(mx, my, 220, 180, 273, 70)){
				//"Easy" button was hit
				HUD.setHealth = 8;
				HUD.HEALTH = HUD.setHealth;
				BasicEnemy.speed = 4;
				FastEnemy.speed = 3;
				SmartEnemy.speed = 1f;
				KeyInput.speed = 5;
				HUD.setShield = 5f; HUD.shield = HUD.setShield;
				Game.gameState = STATE.Game;
				handler.clearEnemies();
				handler.addObject(new Player(Game.WIDTH/2-32, Game.HEIGHT/2-32, ID.Player, handler));
				handler.addObject(new BasicEnemy(r.nextInt(Game.WIDTH-50), r.nextInt(Game.HEIGHT-50), ID.BasicEnemy, handler));
				handler.addObject(new BasicEnemy(r.nextInt(Game.WIDTH-50), r.nextInt(Game.HEIGHT-50), ID.BasicEnemy, handler));
				AudioPlayer.getMusic("menu").stop();
				AudioPlayer.getMusic("game").loop();
				AudioPlayer.getSound("Click").play();
			}
			
			if(mouseOver(mx, my, 260, 280, 200, 70)) {
				//"Medium" Button was hit
				HUD.setHealth = 5;
				HUD.HEALTH = HUD.setHealth;
				BasicEnemy.speed = 5;
				FastEnemy.speed = 3;
				SmartEnemy.speed = 1.5f;
				KeyInput.speed = 6;
				HUD.setShield = 3.8f; HUD.shield = HUD.setShield;
				Game.gameState = STATE.Game;
				handler.clearEnemies();
				handler.addObject(new Player(Game.WIDTH/2-32, Game.HEIGHT/2-32, ID.Player, handler));
				handler.addObject(new BasicEnemy(r.nextInt(Game.WIDTH-50), r.nextInt(Game.HEIGHT-50), ID.BasicEnemy, handler));
				handler.addObject(new BasicEnemy(r.nextInt(Game.WIDTH-50), r.nextInt(Game.HEIGHT-50), ID.BasicEnemy, handler));
				AudioPlayer.getMusic("menu").stop();
				AudioPlayer.getMusic("game").loop();
				AudioPlayer.getSound("Click").play();
			}
			
			if(mouseOver(mx, my, 205, 380, 300, 70)) {
				//"Hard" button was hit
				HUD.setHealth = 5;
				HUD.HEALTH = HUD.setHealth;
				BasicEnemy.speed = 7;
				FastEnemy.speed = 5;
				SmartEnemy.speed = 2f;
				Missile.hard = 3; Bullet.hard = 1.5f;
				KeyInput.speed = 8;
				HUD.setShield = 1f; HUD.shield = HUD.setShield;
				Game.gameState = STATE.Game;
				handler.clearEnemies();
				handler.addObject(new Player(Game.WIDTH/2-32, Game.HEIGHT/2-32, ID.Player, handler));
				handler.addObject(new BasicEnemy(r.nextInt(Game.WIDTH-50), r.nextInt(Game.HEIGHT-50), ID.BasicEnemy, handler));
				handler.addObject(new BasicEnemy(r.nextInt(Game.WIDTH-50), r.nextInt(Game.HEIGHT-50), ID.BasicEnemy, handler));
				AudioPlayer.getMusic("menu").stop();
				AudioPlayer.getMusic("game").loop();
				AudioPlayer.getSound("Click").play();
			}
		}
		
		if(Game.gameState == STATE.Menu) {
			if(mouseOver(mx, my, 250, 180, 200, 70)){
				//"Play" button was hit
				Game.gameState = STATE.Select;
				AudioPlayer.getSound("Click").play();
			}
			
			if(mouseOver(mx, my, 250, 280, 200, 70)) {
				//"Help" Button was hit
				AudioPlayer.getSound("Click").play();
				Game.gameState = STATE.Help;
			}
			
			if(mouseOver(mx, my, 250, 380, 200, 70)) {
				//"Exit" button was hit
				System.exit(0);
			}
		}
		
		if(Game.gameState == STATE.Help) {
			if(mouseOver(mx, my, 100, 430, 140, 60)) {
				//"Back" button was hit
				AudioPlayer.getSound("Click").play();
				Game.gameState = STATE.Menu;
			}
		}
		
		if(Game.gameState == STATE.End) {

			if(mouseOver(mx, my, 130, 330, 240, 130)) {
				//Playing again...
				Game.gameState = STATE.Game;
				AudioPlayer.getMusic("end").stop();
				AudioPlayer.getSound("Click").play();
				AudioPlayer.getMusic("game").loop();
				hud.score(0);
				hud.setLevel(1);
				HUD.HEALTH = 10;
				HUD.shield = 10f;
				handler.clearEnemies();
				handler.addObject(new Player(Game.WIDTH/2-32, Game.HEIGHT/2-32, ID.Player, handler));
				handler.addObject(new BasicEnemy(r.nextInt(Game.WIDTH-50), r.nextInt(Game.HEIGHT-50), ID.BasicEnemy, handler));
				handler.addObject(new BasicEnemy(r.nextInt(Game.WIDTH-50), r.nextInt(Game.HEIGHT-50), ID.BasicEnemy, handler));
			}
			
			if(mouseOver(mx, my, 430, 330, 150, 60)) {
				//Going to menu...
				hud.score(0);
				hud.setLevel(1);
				AudioPlayer.getMusic("end").stop();
				AudioPlayer.getSound("Click").play();
				AudioPlayer.getMusic("menu").loop();
				handler.clearEnemies();
				Game.gameState = STATE.Menu;
				for(int i = 0; i < 10 ; i++)
					handler.addObject(new MenuParticle(r.nextInt(Game.WIDTH-50), r.nextInt(Game.HEIGHT-50), ID.Particle, handler));
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
		if(Game.gameState == STATE.Menu) {
			g.setColor(Color.black);
			g.fillRect(165, 50, 370, 104); //Name
			g.fillRect(250, 180, 200, 70); //Play
			g.fillRect(250, 280, 200, 70); //Help
			g.fillRect(250, 380, 200, 70); //Exit
			g.setColor(Color.WHITE);
			Font f = new Font("arial", 1, 85);
			Font f2 = new Font("arial", 1, 40);
			g.setFont(f);
			g.drawString("EVADE", 205, 130);
			g.setFont(f2);
			g.drawString("Play", 310, 227);
			g.drawString("Help", 307, 327);
			g.drawString("Quit",  309, 427);
			
			g.setColor(Color.WHITE);
			g.drawRect(165, 50, 370, 104); //Name
			g.drawRect(250, 180, 200, 70); //Play
			g.drawRect(250, 280, 200, 70); //Help
			g.drawRect(250, 380, 200, 70); //Exit
		}
		if(Game.gameState == STATE.Select) {
			g.setColor(Color.black);
			g.fillRect(165, 50, 370, 104); //Name
			g.fillRect(220, 180, 273, 70); //Easy
			g.fillRect(260, 280, 200, 70); //Medium
			g.fillRect(205, 380, 300, 70); //Hard
			g.setColor(Color.WHITE);
			Font f = new Font("arial", 0, 75);
			Font f2 = new Font("arial", 1, 40);
			g.setFont(f);
			g.drawString("Difficulty:", 200, 130);
			g.setFont(f2);
			g.drawString("Weenie Mode", 230, 227);
			g.drawString("Average", 285, 327);
			g.drawString("Built Differrent",  215, 427);
			
			g.setColor(Color.WHITE);
			g.drawRect(165, 50, 370, 104); //"Difficulty
			g.drawRect(220, 180, 273, 70); //Easy
			g.drawRect(260, 280, 200, 70); //Medium
			g.drawRect(205, 380, 300, 70); //Hard
		}
		if(Game.gameState == STATE.End) {
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
		if(Game.gameState == STATE.Help) {
			g.setColor(Color.black);
			g.fillRect(260, 32, 200, 90); //Help
			g.fillRect(100, 122, 530, 208); //Directions	
			g.fillRect(100, 430, 140, 60); //Back
			g.setColor(Color.WHITE);
			Font f = new Font("arial", 1, 75);
			Font f2 = new Font("arial", 1, 30);
			g.setFont(f);
			g.setColor(Color.white);
			g.drawString("Help", 280, 100);
			g.setColor(Color.white);
			g.setFont(f2);
			g.drawString("Avoid The Enemies!", 110, 200);
			g.drawString("Use the WASD keys to move.", 110, 250);
			g.drawString("Use your shield by holding SPACE.", 110, 300);
			g.drawString("Back", 132, 467);
			
			g.setColor(Color.WHITE);
			g.drawRect(100, 430, 140, 60); //Back

		}
		if(loading) {
			g.setColor(Color.BLACK);
			g.fillRect(0, 0, Game.WIDTH, Game.HEIGHT);
			Font f = new Font("arial", 1, 35);
			g.setColor(Color.white);
			g.setFont(f);
			g.drawString("loading...", 285, Game.HEIGHT/2-32);
			f = new Font("arial", 1, 20);
			g.setFont(f);
			g.drawString("Now is a good time to give an epilepsy warning.", 135, Game.HEIGHT/2 + 32);
		}
	}
	
	
}
