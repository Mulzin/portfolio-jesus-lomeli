package com.mycompany.minesweeper_v1;

import javax.swing.*;
import java.awt.*;

/**
 * Represents a single cell in the grid.
 * Each cell has a unique ID, coordinates, and various states that
 * determine its behavior in the game.
 */
public class Cell { 
    // Constants for different cell background colors
    private final Color UNCLEARED_COLOR = Color.GRAY;
    private final Color DANGER_COLOR = Color.RED;
    private final Color CLEARED_COLOR = Color.WHITE;   
    
    private final String id;
    
    public final int[] coordinates;
    
    public final JButton button;
    
    // Multiple states for the cell
    public boolean isMine;    
    public boolean isSafe;     
    public boolean isClear;    
    public boolean isMineAdjacent;
    
    public boolean mineAdjacentMinesVisible; //If the cell displays the number of adjacent mines
    
    private boolean mineFlag; //Indicates whether the cell is flagged by the player
    
    public int adjacentMines; //Number of mines directly next to the cell
    
    /**
     * Constructor to initialize a Cell.
     *
     * @param column the column index of the cell
     * @param row the row index of the cell
     */
    Cell(int column,int row) {
        id = (column+" "+row);
        
        coordinates = new int[2];
        coordinates[0] = column;
        coordinates[1] = row;
        
        button = new JButton();        
        
        isMine = false;
        
        isSafe = false;
        
        isClear = false;
        
        isMineAdjacent = false;  
        
        mineAdjacentMinesVisible = false;
        
        mineFlag = false;
        
        adjacentMines = 0;
        
    } 
    
    /**
     * Toggles the flagged state of the cell and updates its appearance.
     */
    public void cycleState() {
        if (isClear || mineAdjacentMinesVisible) { //Do nothing if the cell is clear or adjacentMines is visible
            return;
        }
        if(mineFlag) {
            button.setBackground(UNCLEARED_COLOR);
        }else {
            button.setBackground(DANGER_COLOR);            
        }
        mineFlag = !mineFlag;
    }
    
    /**
     * Increases the count of adjacent mines and marks the cell as mine-adjacent.
     */
    public void increaseMineCount() {
        adjacentMines ++;
        isMineAdjacent = true;
    }
    
    /**
     * Marks the cell as containing a mine.
     */
    public void setToMine() {
        isMine = true;
    }
    
    /**
     * Marks the cell as safe.
     */
    public void setToSafe() {
        isSafe = true;
    }    
    
    /**
     * Marks the cell as cleared and updates its appearance.
     */
    public void setToClear() {
        isClear = true;
        button.setBackground(CLEARED_COLOR);
    }
    
    /**
     * Displays the number of adjacent mines on the cell's button.
     */
    public void displayMinesNearText() {
        button.setText(adjacentMines+"");
        mineAdjacentMinesVisible = true;
    }
}
