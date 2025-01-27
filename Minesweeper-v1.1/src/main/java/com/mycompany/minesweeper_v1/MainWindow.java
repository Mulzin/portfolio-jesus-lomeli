package com.mycompany.minesweeper_v1;

import javax.swing.*;
import java.awt.*;

/**
 * Main window for the game.
 * This class is responsible for initializing and managing the primary UI components,
 * including the setup panel and the play panel.
 */
public class MainWindow extends JFrame{
    // Constants for frame configuration
    private final String FRAME_TITLE = "Minesweeper v1";
    private final int FRAME_WIDTH = 600;
    private final int FRAME_HEIGHT = 400;
    
    // Panels for different stages of the game
    public final SetupPanel setupPanel; //Panel for the game setup UI
    public final PlayPanel playPanel; //Panel for the gameplay UI
    
    /**
     * Constructor to initialize the main window and its panels.
     */
    MainWindow() {
        setupPanel = new SetupPanel();
        playPanel = new PlayPanel();
    }
    
    /**
     * Initializes the user interface by configuring the frame and adding panels.
     */
    public void initializeUI() {
        configFrame();
        
        setupPanel.initializeUI();
        add(setupPanel, BorderLayout.NORTH);
        
        playPanel.initializeUI();
        add(playPanel, BorderLayout.CENTER);
        
        setVisible(true);
    }
    
    /**
     * Configures the frame's basic properties, such as size, title, and default behavior.
     */
    private void configFrame() {
        setTitle(FRAME_TITLE);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(new Dimension(FRAME_HEIGHT, FRAME_WIDTH));
        setResizable(false);
        setLocationRelativeTo(null);
    }   
    
    /**
     * Toggles visibility between the setup panel and the play panel.
     * Adjusts the frame size as needed.
     */
    public void swapPanels() {
        boolean isPanel1Visible = setupPanel.isVisible();
        
        setupPanel.setVisible(!isPanel1Visible);
        playPanel.setVisible(isPanel1Visible);
        
        if(isPanel1Visible) {
            pack();
        }else {
            setSize(new Dimension(FRAME_HEIGHT, FRAME_WIDTH));
        }
        
    }
}
