package game.main;

import java.awt.Color;
import java.util.Random;


// Handle spawning of enemies, generally spawns enemies on beat with the music
public class Spawn {

	private Handler handler;
	private HUD hud;
	private Random r = new Random();
	public Spawn(Handler handler, HUD hud) {
		this.handler = handler;
		this.hud = hud;
	}

	public void tick() {

		if(hud.getScore() >= 670 && hud.getLevel() < 2) {
			handler.addObject(new FastEnemy(r.nextInt(Game.WIDTH-50), r.nextInt(Game.HEIGHT-50), ID.FastEnemy, handler));
			hud.setLevel(2);
		}
		else if(hud.getScore() >= 1326 && hud.getLevel() < 3) {
			handler.addObject(new FastEnemy(r.nextInt(Game.WIDTH-50), r.nextInt(Game.HEIGHT-50), ID.FastEnemy, handler));
			hud.setLevel(3);
		}
		else if(hud.getScore() >= 2000 && hud.getLevel() < 4) {
			handler.addObject(new SmartEnemy(r.nextInt(Game.WIDTH-50), r.nextInt(Game.HEIGHT-50), ID.SmartEnemy, handler));
			hud.setLevel(4);
		}
		else if(hud.getScore() >= 2550 && hud.getLevel() < 5) {
			handler.clearEnemies();
			HUD.HEALTH += 1;
			handler.addObject(new BossOne(Game.WIDTH + 300, Game.HEIGHT/2 - 48, ID.BossOne, handler));
			hud.setLevel(5);
		}
		if (hud.getScore() >= 2650 && hud.getLevel() == 5 && hud.getScore() % 11 == 0 && BossOne.bossOne) {
			handler.addObject(new BossParticle(r.nextInt(Game.WIDTH-50), 0, ID.Particle, handler));

		}
		else if(hud.getScore() >= 7290 && hud.getLevel() < 6) {
			handler.addObject(new CrazyEnemy(r.nextInt(Game.WIDTH-50), r.nextInt(Game.HEIGHT-50), ID.CrazyEnemy, handler));
			handler.addObject(new CrazyEnemy(r.nextInt(Game.WIDTH-50), r.nextInt(Game.HEIGHT-50), ID.CrazyEnemy, handler));
			handler.addObject(new CrazyEnemy(r.nextInt(Game.WIDTH-50), r.nextInt(Game.HEIGHT-50), ID.CrazyEnemy, handler));
			hud.setLevel(6);
		}
		else if(hud.getScore() >= 7960 && hud.getLevel() < 7) {
			handler.addObject(new SmartEnemy(20, Game.HEIGHT-69, ID.SmartEnemy, handler));
			handler.addObject(new SmartEnemy(Game.WIDTH-69, 20, ID.SmartEnemy, handler));
			hud.setLevel(7);
		}
		else if(HUD.score >= 8600 && hud.getLevel() < 8) {
			for(int i = handler.object.size() - 1; i >= 0; i--) {
				if(handler.object.get(i).getID() != ID.Player)
					handler.object.remove(i);
			}
			hud.setLevel(8);
		}
		else if(hud.getScore() >= 8600 && HUD.score < 9100 && hud.getLevel() == 8 && HUD.score % 25 == 0) {
			handler.addObject(new SmartBullet(Game.WIDTH + 32, r.nextInt(Game.HEIGHT), ID.Projectile, handler));
		}
		else if(HUD.score >= 9165 && hud.getLevel() < 9) {
			hud.setLevel(9);
			HUD.HEALTH = HUD.setHealth;
			handler.addObject(new BossTwo(0, 0, ID.Particle, handler));
		}
		if (hud.getScore() >= 9225 && hud.getLevel() == 9 && hud.getScore() % 11 == 0 && BossTwo.bossTwo) {
			handler.addObject(new BossParticle(r.nextInt(Game.WIDTH-50), 0, ID.Particle, handler));
		}
		else if(HUD.score > 11430 && hud.getLevel() < 10) {
			hud.setLevel(10);
			handler.addObject(new FastEnemy(r.nextInt(Game.WIDTH-50), r.nextInt(Game.HEIGHT-50), ID.FastEnemy, handler));
			handler.addObject(new FastEnemy(r.nextInt(Game.WIDTH-50), r.nextInt(Game.HEIGHT-50), ID.FastEnemy, handler));
		}
		if(hud.getScore() >= 11430 && hud.getLevel() == 10 && HUD.score % 30 == 0) {
			handler.addObject(new SmartBullet(Game.WIDTH + 32, r.nextInt(Game.HEIGHT), ID.Projectile, handler));
		}
		if(HUD.score >= 13430 && hud.getLevel() == 10) {
			handler.clearEnemies();
		}
		if(HUD.score > 13430 && hud.getLevel() < 11) {hud.setLevel(11);}
		if(hud.getLevel() >= 11) {
			if(HUD.score % 1000 == 0)
				hud.setLevel(hud.getLevel()+1);
			if(HUD.score % (116-hud.getLevel()*5) == 0)
				handler.addObject(new Missile(-10, r.nextInt(Game.HEIGHT -32), ID.Projectile, handler));
			if(HUD.score % 28 == 0)
				handler.addObject(new SmartBullet(Game.WIDTH + 32, r.nextInt(Game.HEIGHT), ID.Projectile, handler));
			if(HUD.score == 17000 || HUD.score == 20000 || HUD.score == 23000)
				handler.addObject(new BasicEnemy(r.nextInt(Game.WIDTH-50), r.nextInt(Game.HEIGHT-50), ID.BasicEnemy, handler));
		}
	}

}
