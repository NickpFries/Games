package game.main;

import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;

import game.main.Game.STATE;


// Handles all keyboard inputs
public class KeyInput extends KeyAdapter{
	public static int speed = 5;
	private Handler handler;
	private static boolean w=false,a=false,s=false,d=false,space=false;
	private static GameObject player;
	
	public KeyInput(Handler handler) {
		this.handler = handler;
	}
	
	public void keyPressed(KeyEvent e) {
		int key = e.getKeyCode();
		
		for(int i = 0; i < handler.object.size(); i++) {
			
			if(key == KeyEvent.VK_W) w=true;
			if(key == KeyEvent.VK_S) s=true;
			if(key == KeyEvent.VK_D) d=true;
			if(key == KeyEvent.VK_A) a=true;
			if(key == KeyEvent.VK_SPACE) space=true;
		
			if(w && !s)player.setVelY(-speed);
			if(!w && s)player.setVelY(speed);
			if(w && s)player.setVelY(0);
			if(a && !d)player.setVelX(-speed);
			if(!a && d)player.setVelX(speed);
			if(a && d)player.setVelX(0);
		}
		
		//Pausing the game
		if(key == KeyEvent.VK_ESCAPE && Game.gameState == STATE.Game) {
			if(Game.paused) {
				Game.paused = false;
				AudioPlayer.getMusic("game").resume();
			}
			else{
				Game.paused = true;
				AudioPlayer.getMusic("game").pause();
			}
			
		}
	}
	
	public void keyReleased(KeyEvent e) {
		int key = e.getKeyCode();
		for(int i = 0; i < handler.object.size(); i++) {
				//Key Events for the player
				
			if(key == KeyEvent.VK_W) w=false;
			if(key == KeyEvent.VK_S) s=false;
			if(key == KeyEvent.VK_D) d=false;
			if(key == KeyEvent.VK_A) a=false;
			if(key == KeyEvent.VK_SPACE) space=false;
				
			if(!w && !s)player.setVelY(0);
			if(!a && !d)player.setVelX(0);
			if(w && !s)player.setVelY(-speed);
			if(!w && s)player.setVelY(speed);
			if(a && !d)player.setVelX(-speed);
			if(!a && d)player.setVelX(speed);
		}
	}
	
	public static void resetKeys(Player p) {
		a = false;
		w = false;
		s = false;
		d = false;
		player = p;
	}
	
	public static boolean getShield() {
		return space;
	}
}
