package com.mycompany.minesweeper_v1;

/**
 * Entry point for the Minesweeper v1 application.
 * This class initializes and starts the application.
 */
public class MinesweeperGame { 
    
    /**
     * The main method is the entry point of the application.
     * It creates an instance of the MainApp class and starts the application.
     * 
     * @param args Command-line arguments (not used in this application)
     */
    public static void main(String[] args) {
        MainApp mainApp = new MainApp();
        mainApp.appStart();
    }
}
