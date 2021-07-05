package game.main;

import java.awt.Graphics;
import java.util.LinkedList;
import java.util.Objects;

import game.main.Game.STATE;


// Handles all game objects
public class Handler {
	LinkedList<GameObject> object = new LinkedList<GameObject>();
	
	public void tick() {
		for(int i = object.size() -1; i >= 0; i--) {
			try {
				GameObject tempObject = object.get(i);
				tempObject.tick();}
			catch(Exception e) {
				//Object was deleted while this thread was in process
				//No need to do anything here
			}
			
		}
	}
	
	public void render(Graphics g) {
		for(int i = object.size()-1; i >= 0; i--) {
			try {
				GameObject tempObject = object.get(i);
				tempObject.render(g);}
			catch(Exception e) {
				//Object was deleted while this thread was in process
				//No need to do anything here
			}
		}
	}
	
	public void addObject(GameObject object) {
		this.object.add(object);
	}
	
	public void removeObject(GameObject object) {
		this.object.remove(object);
	}
	
	public void clearEnemies() {
		if(Game.gameState == STATE.End) object.clear();
		for(int i = object.size() - 1; i >= 0; i--) {
			if(object.get(i).getID() != ID.Player)
				object.remove(i);
		}
	}
	
	
}
