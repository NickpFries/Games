package game.main;


// Handles all game audio and stores files in HashMaps
import java.util.HashMap;
import java.util.Map;

import org.newdawn.slick.Music;
import org.newdawn.slick.SlickException;
import org.newdawn.slick.Sound;
public class AudioPlayer {

	
	public static Map<String, Sound> soundMap = new HashMap<String, Sound>();
	public static Map<String, Music> musicMap = new HashMap<String, Music>();
	
	public static void load() {
		
		try {
			
			musicMap.put("game", new Music("Res/dp.ogg"));
			musicMap.put("end", new Music("Res/ussr.ogg"));
			musicMap.put("menu", new Music("Res/menu.ogg"));
			soundMap.put("Click", new Sound("Res/click.ogg"));
		}
		catch(SlickException e) {
			e.printStackTrace();
		}
	}
	
	public static Music getMusic(String key) {
		return musicMap.get(key);
	}
	
	public static Sound getSound(String key) {
		return soundMap.get(key);
	}
	
}
