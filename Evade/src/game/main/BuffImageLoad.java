package game.main;

import java.awt.image.BufferedImage;
import java.io.IOException;

import javax.imageio.ImageIO;


// Load image
public class BuffImageLoad {

	BufferedImage image;
	
	public BufferedImage loadImage(String path) {
			try {
				image = ImageIO.read(getClass().getResource(path));
			} catch (IOException e) {
				e.printStackTrace();
			}
			return image;
	}
}
