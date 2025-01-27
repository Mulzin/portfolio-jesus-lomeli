package com.mycompany.minesweeper_v1;

import javax.swing.*;
import java.awt.*;

/**
 * Handles the UI for configuring the game grid.
 * It includes input fields for the grid dimensions, mine count, and error messages.
 */
public class SetupPanel extends JPanel {
    // Panel constants
    private final String PANEL_TITLE = "Minesweeper v1";
    
    // Input field labels
    private final String WIDTH_TITLE = "Width:";
    private final String HEIGHT_TITLE = "Height:";
    private final String MINE_COUNT_TITLE = "Mines:";
    private final String START_STR = "Start";
    
    // Validation constants
    private final int SAFE_ZONE_AREA = 9;    
    private final int GRID_SIZE_FLOOR = 4;
    private final int GRID_SIZE_CEIL = 31;
    
    // Error messages
    private final String INT_ERROR = "Input must be full numbers";
    private final String MINE_ROOM_ERROR = "Not enough room for mines";
    private final String GRID_SIZE_ERROR = "Width or height out of range: ";
    
    private final JLabel title;
    
    // Custom input panels
    private final InputPanel heightInput;
    private final InputPanel widthInput;      
    private final InputPanel mineCountInput;
    
    private final JLabel warningIntError;
    private final JLabel warningMineRoom;
    private final JLabel warningSmallSizeError;
    
    public final JButton startButton;
    
    /**
     * Constructor to initialize the setup panel and its components.
     */
    SetupPanel() {
        title = new JLabel(PANEL_TITLE, SwingConstants.CENTER);
        
        widthInput = new InputPanel(WIDTH_TITLE);
        heightInput = new InputPanel(HEIGHT_TITLE);
        mineCountInput = new InputPanel(MINE_COUNT_TITLE);
        
        startButton = new JButton(START_STR);
        
        warningIntError = new JLabel(INT_ERROR);
        warningMineRoom = new JLabel(MINE_ROOM_ERROR);
        warningSmallSizeError = new JLabel(GRID_SIZE_ERROR);
    }
    
    /**
     * Initializes the panel's user interface.
     * Sets layout, aligns components, and adds them to the panel.
     */
    public void initializeUI() {
        setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
        setAlignmentX(Component.LEFT_ALIGNMENT);
        
        title.setAlignmentX(Component.CENTER_ALIGNMENT);
        add(title);
        
        heightInput.initializePanel();
        add(heightInput);
        
        widthInput.initializePanel();
        add(widthInput);
        
        mineCountInput.initializePanel();
        add(mineCountInput);
        
        startButton.setAlignmentX(Component.CENTER_ALIGNMENT);
        add(startButton);
        
        add(warningIntError);
        add(warningSmallSizeError);
        add(warningMineRoom);
        
        hideWarningLabels();
    }
    
    /**
     * Hides all warning labels.
     */
    private void hideWarningLabels() {
        warningIntError.setVisible(false);
        warningSmallSizeError.setVisible(false);
        warningMineRoom.setVisible(false);
    }
    
    /**
     * Validates the user input from the input fields.
     * 
     * @return true if the input is valid, false otherwise
     */
    public boolean validateInput() {
        hideWarningLabels();
        try {
            // Integer.parseInt will raise an error if any of the inputs are not integers
            int gridHeight = Integer.parseInt(heightInput.getInput());
            int gridWidth = Integer.parseInt(widthInput.getInput());            
            int mineNum = Integer.parseInt(mineCountInput.getInput());
            
            // Check if grid dimensions are within allowed range
            if(gridHeight > GRID_SIZE_CEIL || gridHeight < GRID_SIZE_FLOOR ||
               gridWidth > GRID_SIZE_CEIL || gridWidth < GRID_SIZE_FLOOR) {
                warningSmallSizeError.setVisible(true);
                return false;
            }
            
            // Check if the grid has enough space for mines
            if(mineNum+SAFE_ZONE_AREA > gridWidth*gridHeight) {
                warningMineRoom.setVisible(true);
                return false; 
            }
            
            return true;  // Input is valid          
        }catch(NumberFormatException integerError) { // Catch Integer.parseInt error
            warningIntError.setVisible(true);
            return false;
        }
    } 
    
    /**
     * Retrieves the game settings input by the user.
     * 
     * @return an array containing the height, width, and mine count
     */
    public int[] getGameSetting() {
        int[] gameSetting = new int[3];
        
        gameSetting[0] = Integer.parseInt(heightInput.getInput());
        gameSetting[1] = Integer.parseInt(widthInput.getInput());        
        gameSetting[2] = Integer.parseInt(mineCountInput.getInput());
        
        return gameSetting;
    }
}
