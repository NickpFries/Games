package game.main;

import java.awt.Canvas;
import java.awt.Dimension;

import javax.swing.JFrame;


// Creates a window
public class Window extends Canvas {
	
	private static final long serialVersionUID = 1L;
	
	public Window(int width, int height, String title, Game game) {
		JFrame frame = new JFrame(title);
		
		Dimension d = new Dimension(width, height);
		frame.setPreferredSize(d);
		frame.setMaximumSize(d);
		frame.setMinimumSize(d);
		
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setResizable(false);
		frame.setLocationRelativeTo(null);
		frame.add(game);
		frame.setVisible(true);
		game.start();
	}
	
	
	
}
