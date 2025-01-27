package com.mycompany.minesweeper_v1;

import javax.swing.*;
import java.awt.*;
import javax.swing.border.Border;

/**
 * Game area where the Minesweeper grid is displayed and interacted with.
 * It handles the visualization and styling of the game cells.
 */
public class PlayPanel extends JPanel {
    // Panel constants
    private final Color NORMAL_COLOR = Color.GRAY;
    
    // Dimensions for each game cell button
    private final int BUTTON_HEIGHT = 30;            
    private final int BUTTON_WIDTH = 30;
    
    // Padding for cell buttons
    private final int BUTTON_PADDING = 0;
    
    // Border styling for the cell buttons
    private final Color MARGIN_COLOR = Color.BLACK;
    private final int MARGIN_THICKNESS = 1;
    
    /**
     * Constructor for PlayPanel.
     * Initializes the panel without any specific configuration.
     */
    PlayPanel(){
    }
    
    /**
     * Initializes the user interface of the PlayPanel.
     * Currently sets the panel to be invisible by default.
     */
    public void initializeUI() {   
        setVisible(false);
    }
    
    /**
     * Paints the Minesweeper grid on the panel using the provided cell grid.
     * 
     * @param cellGrid A 2D array of Cell objects representing the Minesweeper grid
     * @param gridWidth The width of the grid in cells
     * @param gridHeight The height of the grid in cells
     */
    public void paintCellGrid(Cell[][] cellGrid,int gridWidth,int gridHeight) {
        removeAll();
        
        setLayout(new GridLayout(gridHeight,gridWidth));
        
        // Loop through each cell in the grid. Configure its button
        // then add it to the panel
        for(Cell[] row: cellGrid) {
            for(Cell cell:row) {
                configButtonStyle(cell.button);
                add(cell.button);
            }
        }        
    }
    
     /**
     * Configures the visual style of a cell button.
     * 
     * @param cellButton The JButton representing a cell
     */
    private void configButtonStyle(JButton cellButton) {
        cellButton.setBackground(NORMAL_COLOR);
        cellButton.setPreferredSize(new Dimension(BUTTON_HEIGHT, BUTTON_WIDTH));
        cellButton.setMargin(new Insets(BUTTON_PADDING, BUTTON_PADDING, BUTTON_PADDING, BUTTON_PADDING));
        Border marginBorder = BorderFactory.createLineBorder(MARGIN_COLOR, MARGIN_THICKNESS); // Color and thickness
        cellButton.setBorder(marginBorder);
    }
}
