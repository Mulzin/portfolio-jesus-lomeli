import customtkinter as ctk
import random
            
COLORS = ["A","B","C","D"] #13 cards:1-13, 4 colors:A B C D
CARDS = [COLORS[i]+"\n"+str(j) for i in range(4) for j in range(1,13)]
PLAYER_COUNT = 2
PLAYER_COLOR = ["red","yellow","green","white"]
HAND_SIZE = 5
CORNER_SYMBOL = "0"
CELL_WIDTH = 60
CELL_HEIGHT = 80

class player:
    def __init__(self,initial_hand,color):
        self.hand = [i for i in initial_hand]
        self.color = color
    
class grid_cell:
    def __init__(self,value,x,y):
        self.value = value
        self.coord = (x,y)
        self.player_color = ""
        self.button = ctk.CTkButton(
            master=root,text=self.value,
            state="disabled",
            text_color_disabled="black",
            width=CELL_WIDTH,
            height=CELL_HEIGHT,
            border_color="black",
            border_width=3,
            font=("arial",25)
        )
        self.button.grid(row=self.coord[0],column=self.coord[1])
        return
    
    def update_cell(self,color,pos_moves,turn,deck):
        self.button.configure(state="normal",command=lambda:self.recolor(color,pos_moves,turn,deck))                 
        return

    def recolor(self,color,pos_moves,turn,deck):   
        self.button.configure(fg_color=color)  
        self.player_color = color
        for cell in pos_moves:
            grid[cell].disable()  
        player_grant_card(turn,self.value,deck)        
        if turn == (PLAYER_COUNT-1): turn = 0
        else: turn += 1
        highlight_options(turn,deck)
        return
    
    def disable(self):
        self.button.configure(state="disabled")  
        return

def gen_grid():
    available_cards = [j for i in range(2) for j in CARDS]
    for x in range(1,11):
        for y in range(10):
            if (x == 1 or x == 10) and (y == 0 or y == 9):
                grid.append(grid_cell(CORNER_SYMBOL,x,y))
            else:
                ran_num = random.randrange(len(available_cards))
                grid.append(grid_cell(available_cards[ran_num],x,y))
                available_cards.pop(ran_num)
    return

def game_start():
    available_cards = [j for i in range(3) for j in CARDS]    
    for i in range(PLAYER_COUNT):        
        inital_hand = [random.choice(available_cards) for j in range(HAND_SIZE)]
        player_list.append(player(inital_hand,PLAYER_COLOR[i]))
        for card in inital_hand: available_cards.remove(card)
    turn = 0
    highlight_options(turn,available_cards)
    return
            
def highlight_options(turn,deck):    
    player_title = ctk.CTkLabel(root,text="Jugador "+str(turn+1),bg_color=player_list[turn].color)
    player_title.grid(row=0,column=1)   
    posible_moves_i = [grid_i for card in player_list[turn].hand for grid_i in range(len(grid)) if card == grid[grid_i].value and grid[grid_i].player_color == ""]
    posible_moves_value = [grid[i].value for i in posible_moves_i]   
    print(posible_moves_value)          
    for cell in posible_moves_i:
        grid[cell].update_cell(player_list[turn].color,posible_moves_i,turn,deck)    
    for card in range(HAND_SIZE): 
        if not player_list[turn].hand[card] in posible_moves_value:
            player_hand_label[card].configure(text=player_list[turn].hand[card],state="normal",command=lambda:player_discard_card(turn,player_list[turn].hand[card]))
        else:
            player_hand_label[card].configure(text=player_list[turn].hand[card],state="disabled")    
    return     
            
def player_grant_card(turn,card,deck):
    new_card = random.choice(deck)  
    player_list[turn].hand.remove(card)
    player_list[turn].hand.append(new_card)
    deck.remove(new_card)
    return    

def player_discard_card(turn,card):
    print(card)
    return

root = ctk.CTk()

grid = []
shuffle_cards = [j for i in range(3) for j in CARDS]
player_list = [] 
player_hand_label = [ctk.CTkButton(root,
                                   text="",
                                   state="disabled",
                                   text_color_disabled="black",
                                   width=CELL_WIDTH,
                                   height=CELL_HEIGHT,
                                   border_color="black",
                                   border_width=3,
                                   font=("arial",25)) for i in range(HAND_SIZE)]
for card in range(len(player_hand_label)): player_hand_label[card].grid(row=0,column=card+2)

gen_grid()

game_start()

root.mainloop()