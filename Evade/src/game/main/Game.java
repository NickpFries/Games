package game.main;
import java.awt.Canvas;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.image.BufferStrategy;
import java.awt.image.BufferedImage;
import java.util.Random;


// Game engine, handles ticking and rendering, tracks what state the game is in, initializes everything
public class Game extends Canvas implements Runnable {

	private static final long serialVersionUID = 1L;
	//Change size of the window on next line
	public static final int WIDTH = 720, HEIGHT = WIDTH / 12 * 9;
	
	private Thread thread;
	private boolean running = false;
	private Handler handler;
	private HUD hud;
	private Spawn spawner;
	private Menu menu;
	private Random r;
	public static boolean paused = false;
	public static BufferedImage sprite_sheet;
	
	public enum STATE{
		Select,
		Menu,
		Help,
		Game,
		End
	};
	
	public static STATE gameState = STATE.Menu;
	
	public Game() {
		handler = new Handler();
		this.addKeyListener(new KeyInput(handler));
		new Window(WIDTH, HEIGHT, "Evade", this);
		hud = new HUD();
		menu = new Menu(this, handler, hud);
		AudioPlayer.load();
		BuffImageLoad loader = new BuffImageLoad();
		sprite_sheet = loader.loadImage("/EVADE.png");
		AudioPlayer.getMusic("menu").loop();
		menu.loading = false;
		this.addMouseListener(menu);
		spawner = new Spawn(handler, hud);
		this.requestFocus();
		r = new Random();
		
}
	
	public synchronized void start() {
		thread = new Thread(this);
		thread.start();
		running = true;
	}
	
	public synchronized void stop() {
		try {
			thread.join();
			running = false;
		}
		catch(Exception e){
			e.printStackTrace();
		}
	}
	
	public void run() {
		this.requestFocus();
		long lastTime = System.nanoTime();
		double amountOfTicks = 60.0;
		double ns = 1000000000 / amountOfTicks;
		double delta = 0;
		long timer = System.currentTimeMillis();
		int frames = 0;
		while(running) {
			long now = System.nanoTime();
			delta += (now - lastTime) / ns;
			lastTime = now;
			while(delta >= 1) {
				tick();
				delta--;
			}
			if(running)
				render();
			frames++;
			
			if(System.currentTimeMillis() - timer > 1000) {
				timer += 1000;
				System.out.println("FPS: " + frames);
				frames = 0;
			}
		}
		stop();
	}
	
	private void tick() {
		if(!paused)
			handler.tick();
		if(HUD.HEALTH <= 0) {
			HUD.HEALTH = HUD.setHealth;
			gameState = STATE.End;
			handler.clearEnemies();
			AudioPlayer.getMusic("game").stop();
			AudioPlayer.getMusic("end").loop();
			for(int i = 0; i < 10 ; i++)
				handler.addObject(new MenuParticle(r.nextInt(Game.WIDTH-50), r.nextInt(Game.HEIGHT-50), ID.Particle, handler));
		}
		if(gameState == STATE.Game && !paused) {
			hud.tick();
			spawner.tick();
		}
		else if(gameState == STATE.Menu) {
			menu.tick();
		}
		else if(gameState == STATE.End) {
			menu.tick();
		}
		else if(gameState == STATE.Select) {
			menu.tick();
		}
	}
	
	private void render() {
		BufferStrategy bs = this.getBufferStrategy();
		if(bs == null) {
			this.createBufferStrategy(3);
			return;
		}
		
		Graphics g = bs.getDrawGraphics();
		
		g.setColor(Color.black);
		g.fillRect(0,  0,  WIDTH,  HEIGHT);
		
		handler.render(g);
		
		if(paused) {
			g.setColor(Color.white);
			g.drawString("PAUSED", 100, 100);
			
		}
		if(gameState == STATE.Game) {
			hud.render(g);
		}
		else if(gameState == STATE.Menu) {
			menu.render(g);
		}
		else if(gameState == STATE.Help) {
			menu.render(g);
		}
		else if(gameState == STATE.End) {
			menu.render(g);
		}
		else if(gameState== STATE.Select) {
			menu.render(g);
		}
		g.dispose();
		bs.show();
	}
		
	//Method to keep player inside a box
	public static float clamp(float var, float min, float max) {
		if(var >= max)
			return max;
		if(var <= min)
			return min;
		else
			return var;
	}
	
	public static void main(String[] args) {
		new Game();
		
	}

}
