package game.main;

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;


// Handles the hud and player attributes including health and shield
public class HUD {
	
	public static float setHealth = 1;
	public static float HEALTH = setHealth;
	private float greenValue = 255, blueValue = 255;
	public static float setShield = 1;
	public static float shield = setShield;
	private int level = 1;
	public static int score = 0;

	public void tick() {
		HEALTH = (int) Game.clamp(HEALTH, 0, setHealth);
		greenValue = (HEALTH/setHealth)*255;
		greenValue = (int) Game.clamp(greenValue, 0, 255);
		score++;
		
		shield+=0.002f;
		if(KeyInput.getShield()) shield -= 0.1f;
		shield = Game.clamp(shield, 0, setShield);
		blueValue = (shield/setShield)*255;
		blueValue = (int)Game.clamp(blueValue, 0, 210);
		
	}
	
	public void render(Graphics g) {
		//Health Bar
		g.setColor(Color.gray);
		g.fillRect(15,  15, 200, 32);
		g.setColor(new Color(75, (int)greenValue, 0));
		g.fillRect((int)15,  (int)15, (int)(200*(HEALTH/setHealth)), 32);
		g.setColor(Color.white);
		g.drawRect(15,  15, 200, 32);
		
		//Shield Bar
		g.setColor(Color.gray);
		g.fillRect(490,  15, 200, 32);
		g.setColor(new Color(0, (int)blueValue, (int)blueValue));
		g.fillRect((int)490,  (int)15, (int)(200*(shield/setShield)), 32);
		g.setColor(Color.white);
		g.drawRect(490,  15, 200, 32);
		
		//Score, Level, and Lives texts
		g.setFont(new Font("arial", 0, 15));
		g.drawString("Score: " + score, 20, 64);
		g.drawString("Level: " + level, 20, 80);
		g.setFont(new Font("TimesRoman", Font.PLAIN, 22));
		g.drawString("Shield", 495, 40);
		g.setColor(Color.black);
		g.drawString("Lives: " + (int)HEALTH, 20, 40);
	}
	
	public void score(int score) {
		HUD.score = score;
	}
	
	public int getScore() {
		return HUD.score;
	}
	
	public int getLevel() {
		return level;
	}
	
	public void setLevel(int l) {
		this.level = l;
	}
	
	public static boolean shielded() {
		if(KeyInput.getShield() && shield > 0) {
			return true;
		}
		return false;
	}
}
