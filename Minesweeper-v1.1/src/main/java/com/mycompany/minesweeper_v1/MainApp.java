package com.mycompany.minesweeper_v1;

import java.awt.event.*;
import java.util.ArrayList;
import java.util.Collections;
import javax.swing.SwingUtilities;
import javax.swing.JDialog;
import javax.swing.JOptionPane;

/**
 * Core logic and controller for the game.
 * It manages game initialization, grid setup, mine placement, and gameplay.
 */
public class MainApp {
    // Directions for checking adjacent cells
    private final int[][] CROOS_SIDES = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};
    private final int[][] VERTICAL_SIDE = {{-1,0},{1,0}};
    private final int[][] HORIZONTAL_SIDES = {{0,1},{0,1}};
        
    // Messages and titles for game-over and victory dialogs
    private final String GAME_OVER_TITLE = "Game Over";
    private final String VICTORY_TITLE = "Victory Royale";            
    private final String GAME_OVER_MESSAGE = "Boom! You hit a mine.";
    private final String VICTORY_MESSAGE = "Cleared the board!";
                    
    private final MainWindow frame;
    
    // Game settings
    private int gridWidth;
    private int gridHeight;    
    private int mineNum;
    private Cell[][] cellGrid;
    
    private boolean firstMove; // Indicates if the next move is the first one
    private int hidenNodesRemaining; // Number of non-mine cells yet to be revealed
    
    /**
     * Constructor initializes the MainApp.
     * Sets up the main window and initializes default game state.
     */
    MainApp() {
        frame = new MainWindow();
        
        firstMove = true;
        
        hidenNodesRemaining = 0;
    }
    
    /**
     * Starts the Minesweeper application.
     * Initializes the main window and sets up the start button's functionality.
     */
    public void appStart() {
        frame.initializeUI();
        
        frame.setupPanel.startButton.addActionListener(e -> {
            gameStart();
        });
    }
    
    /**
     * Starts a new game by validating input, setting up the game grid, 
     * and configuring the user interface for gameplay.
     */
    private void gameStart() {
        if(frame.setupPanel.validateInput()) { // Check if the input is correct
            setupGameSettings();
            
            frame.playPanel.paintCellGrid(cellGrid,gridWidth,gridHeight);
            
            frame.swapPanels();
        
            configCellGridCallback();
        }
    }
    
    /**
     * Sets up the game grid and initializes the cells based on user input.
     */
    private void setupGameSettings() {
        int[] gameSetting = frame.setupPanel.getGameSetting();
        
        gridHeight = gameSetting[0];
        gridWidth = gameSetting[1];        
        mineNum = gameSetting[2];
        
        cellGrid = new Cell[gridHeight][gridWidth];
        
        for(int x = 0;x < gridHeight;x++) {
            for(int y = 0;y < gridWidth;y++) {
                cellGrid[x][y] = new Cell(x,y);
            }
        }
        
        firstMove = true; // Reset firstMove for new game
        
        hidenNodesRemaining = (gridWidth*gridHeight) - mineNum;
    }
    
    /**
     * Configures click listeners for each cell in the grid to handle left and right clicks.
     */
    private void configCellGridCallback() {
        for(Cell[] row: cellGrid) {
            for(Cell cell: row) {
                cell.button.addMouseListener(new MouseAdapter() {
                    @Override
                    public void mouseClicked(MouseEvent e) {
                        if (SwingUtilities.isLeftMouseButton(e)) {
                            handleLeftClick(cell); // Handle left click behavior                      
                        } else if (SwingUtilities.isRightMouseButton(e)) {
                            cell.cycleState(); // Cycle through cell states (e.g., flagging)
                        }
                    }
                });
            }
        }
    }
    
    /**
     * Handles the logic for a left click on a cell.
     * 
     * @param cell The cell that was clicked
     */
    private void handleLeftClick(Cell cell) {
        if(firstMove) {            
            initializeMines(cell.coordinates);
            firstMove = false;
        }
        if(cell.isMine) {
            resetGame(false);
            return;
        }        
        if(!cell.isClear && !cell.isMineAdjacent) {
            hidenNodesRemaining --;
            cell.setToClear();
            revealCrossCells(cell,true); 
        }
        if(!cell.mineAdjacentMinesVisible && cell.isMineAdjacent) {
                hidenNodesRemaining --;
                cell.displayMinesNearText();
                revealCrossCells(cell,false);                                
        }
        checkWinCondition();
    }
    
    /**
     * Initializes the minefield by placing mines and updating adjacent cell counts.
     * Ensures the initial click area is safe.
     * 
     * @param startCoordinates The coordinates of the first clicked cell
     */
    private void initializeMines(int[] startCoordinates) {   
        int[][] safeZone = getCellNeighborhood(startCoordinates);          
        
        setupSafeCells(safeZone);
        
        int[][] mineCoordinates = genRandomMines();
        
        setupMines(mineCoordinates);
        
        initializeMineAdjacentCells(mineCoordinates);
    }
    
    /**
     * Marks a safe zone (non-mine) around the initial click.
     */
    private void setupSafeCells(int[][] neighborhood) {
        for(int[] coordinate: neighborhood) {
            if(isCoordinateInBounds(coordinate)) {
                cellGrid[coordinate[0]][coordinate[1]].setToSafe();
            }            
        }
    }
    
    /**
     * Generates random mine locations by shuffling the cells.
     * 
     * @return An array of mine coordinates
     */
    private int[][] genRandomMines() {
        ArrayList<Cell> shuffledCells = shuffleCells();
        
        int[][] mineCoordinates = selectMineCoordinates(shuffledCells);
        	
        return mineCoordinates;
    }
    
    /**
     * Randomly shuffles the cells to prepare for mine placement.
     */
    private ArrayList<Cell> shuffleCells() {
        ArrayList<Cell> newList = new ArrayList<>();
        
        for(Cell[] row: cellGrid) {
            for(Cell node: row) {
                newList.add(node);
            }             
        }
        
        Collections.shuffle(newList);
        
        return newList;
    }
    
    /**
     * Selects coordinates for the mines from the shuffled cells.
     */
    private int[][] selectMineCoordinates(ArrayList<Cell> shuffledCells) {
        int[][] mineCoordinates = new int[mineNum][2];
        
        Cell auxCell;
        
        int j = 0;
        
        for(int i = 0;i < mineNum;i++) { // Iterate the number of mines
            while(true) {    
                auxCell = shuffledCells.get(j);
                j++;
                if(!auxCell.isSafe) { // If cell is available 
                    mineCoordinates[i] = auxCell.coordinates;
                    break;
                }
            }            
        }
        
        return mineCoordinates;
    }
    
    /**
     * Sets up mines in the grid by marking cells as mines.
     * 
     * @param mineCoordinates The coordinates of the mines
     */
    private void setupMines(int[][] mineCoordinates) {
        for(int[] coordinate: mineCoordinates) {
            cellGrid[coordinate[0]][coordinate[1]].setToMine();
        }
    }
    
    /**
     * Initializes the neighboring cells around each mine by incrementing the mine counter.
     * This counts how many mines are adjacent to each cell.
     * 
     * @param mineCoordinates The coordinates of the mines
     */
    private  void initializeMineAdjacentCells(int[][] mineCoordinates) {
       for(int[] coordinate: mineCoordinates) {
           increaseMineCounter(coordinate);
       }
    }
    
    /**
     * Increases the mine count for each adjacent cell of a mine.
     * 
     * @param mineCoordinate The coordinates of the mine
     */
    private void increaseMineCounter(int[] mineCoordinate) {
       int[][] mineNeighborhood; 
       Cell updatedNode;
       
       mineNeighborhood = getCellNeighborhood(mineCoordinate);
       
       // Loop through all the neighbors of the current mine
       for(int[] coordinate: mineNeighborhood) {
            if(!isCoordinateInBounds(coordinate)){     
                continue;
            }
            updatedNode = cellGrid[coordinate[0]][coordinate[1]];
            // If the adjacent cell isn't a mine, increment its mine counter
            if(!updatedNode.isMine) {
                updatedNode.increaseMineCount();
            }
        }
    }
    
    /**
     * Reveals the adjacent cells of a given cell.
     * If the adjacent cells are safe (non-mine), they will be cleared.
     * If the adjacent cells are mine-adjacent, their mine count will be displayed.
     * Non adjacent are cleared recursively
     * Mine-adjacent cells follow a diferent method
     * 
     * @param targetNode The current cell whose neighbors will be revealed
     * @param checkMineAdjacentSides If true, the method will also reveal adjacent mine counts
     */
    private void revealCrossCells(Cell targetNode,boolean checkMineAdjacentSides) {
        int[] checkCoordinate = new int[2];
        Cell sideCell;
        
        // Loop through the cross (up, right, down, left) adjacent cells
        for (int[] crossCoordinate : CROOS_SIDES) { 
            checkCoordinate[0] = targetNode.coordinates[0] + crossCoordinate[0];
            checkCoordinate[1] = targetNode.coordinates[1] + crossCoordinate[1];

            if (!isCoordinateInBounds(checkCoordinate)) {
                continue;
            }

            sideCell = cellGrid[checkCoordinate[0]][checkCoordinate[1]];
            
            // If the cell is adjacent to a mine but not yet displayed, show the mine count
            if (sideCell.isMineAdjacent) {
                if(sideCell.mineAdjacentMinesVisible) {
                    continue;
                }
                if(!checkMineAdjacentSides) {
                    continue;
                }                
                hidenNodesRemaining --;
                sideCell.displayMinesNearText();
                filterOrientation(sideCell.coordinates, crossCoordinate);          
                continue;
            }
            
            // If the cell is not yet cleared, clear it and reveal its neighbors recursively
            if (!sideCell.isClear) {
                hidenNodesRemaining --;
                sideCell.setToClear();  
                revealCrossCells(sideCell, true); 
            }        
        }
    }
    
    /**
     * Filters the adjacent cells' orientation (either horizontal or vertical) to correctly reveal them.
     * This ensures that cells on the edges of the grid are handled properly.
     * 
     * @param targetCellCoordinates The coordinates of the target cell
     * @param incomingSide The direction from which the cell is being checked (either vertical or horizontal)
     */
    private void filterOrientation(int[] targetCellCoordinates,int[] incomingSide) {
        if(incomingSide[0] > 0 || incomingSide[0] < 0) {
            // If moving horizontally, reveal horizontal neighbors
            setupSideCells(HORIZONTAL_SIDES,targetCellCoordinates);
        }else {
            // Else if moving vertically, reveal vertical neighbors
            setupSideCells(VERTICAL_SIDE,targetCellCoordinates);
        }
    }    
    
    /**
     * Sets up the side cells based on a direction (horizontal or vertical).
     * This ensures that adjacent cells in the proper direction are checked.
     * 
     * @param sideSteps The directional steps (horizontal or vertical)
     * @param targetCellCoordinates The coordinates of the target cell
     */
    private void setupSideCells(int[][] sideSteps,int[] targetCellCoordinates) {
        int[] sideCoordinates = new int[2];
        Cell sideNode;
        
        // Loop through the filtered sides ({left,right} or {up,down})
        for(int[] stepCoordinates: sideSteps) {
            sideCoordinates[0] = targetCellCoordinates[0] + stepCoordinates[0];
            sideCoordinates[1] = targetCellCoordinates[1] + stepCoordinates[1];
            
            if(!isCoordinateInBounds(sideCoordinates)){
                continue;                     
            }
            sideNode = cellGrid[sideCoordinates[0]][sideCoordinates[1]];
            
            // If the side node is mine-adjacent and hasn't been revealed, display its mine count
            if(sideNode.isMineAdjacent && !sideNode.mineAdjacentMinesVisible) {
                hidenNodesRemaining --;
                sideNode.displayMinesNearText();
            }  
        }
    }
    
    /**
     * Checks if the player has won the game by revealing all non-mine cells.
     */
    private void checkWinCondition() {
        if(hidenNodesRemaining == 0){
            resetGame(true);
        }
    }
    
    /**
     * Resets the game, showing a dialog with either a win or lose message.
     * 
     * @param win Indicates if the player won or lost the game
     */
    private void resetGame(boolean win) {
        if(win) {
            JOptionPane.showMessageDialog(
                   frame,
                   VICTORY_MESSAGE,
                   VICTORY_TITLE,
                   JOptionPane.PLAIN_MESSAGE
           );
        }else {
           JOptionPane.showMessageDialog(
                   frame,
                   GAME_OVER_MESSAGE,
                   GAME_OVER_TITLE,
                   JOptionPane.ERROR_MESSAGE
           ); 
        }
        // Swap panels to restart or exit the game
        frame.swapPanels();        
    }
    
    /**
     * Gets the neighborhood of a given cell, including all surrounding cells (8 directions).
     * 
     * @param nodeCoordinates The coordinates of the cell
     * @return A 2D array of the neighboring cell coordinates
     */
    private static int[][] getCellNeighborhood(int[] nodeCoordinates) {
        int[][] adjacentNodes = new int[9][2];        
        int i = 0; 
        
        // Loop through the surrounding 8 cells plus the cell itself
        for(int x = -1;x < 2;x++) {
            for(int y = -1;y < 2;y++){
                adjacentNodes[i][0] = nodeCoordinates[0] + x;
                adjacentNodes[i][1] = nodeCoordinates[1] + y;
                i++;
            }
        }
        return adjacentNodes;
    }
    
    /**
     * Checks if a coordinate is within the bounds of the game grid.
     * 
     * @param coordinate The coordinates to check
     * @return True if the coordinate is within bounds, false otherwise
     */
    private boolean isCoordinateInBounds(int[] coordinate) {
        if(coordinate[0] >= gridWidth || coordinate[0] < 0) {
            return false;
        }
        return !(coordinate[1] >= gridHeight || coordinate[1] < 0);
    }
}