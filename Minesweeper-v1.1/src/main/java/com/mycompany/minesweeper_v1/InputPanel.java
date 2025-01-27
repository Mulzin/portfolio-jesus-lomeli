package com.mycompany.minesweeper_v1;

import javax.swing.*;
import java.awt.*;

public class InputPanel extends JPanel {
    private final int PANEL_WIDTH = 300;
    private final int PANEL_HEIGHT = 30;
    
    private final int TEXTFIELD_LEN = 3;
    
    private final JLabel title;
    public final JTextField input;
    
    InputPanel(String titleStr) {
        title = new JLabel(titleStr);
        input = new JTextField(TEXTFIELD_LEN);
    }
    
    public void initializePanel() {
        setAlignmentX(Component.CENTER_ALIGNMENT);
        setMaximumSize(new Dimension(PANEL_WIDTH, PANEL_HEIGHT));
        
        add(title);
        add(input);
    }
    
    public String getInput() {
        return input.getText();
    }
}
