from tkinter import *
from Game import *
from PIL import Image, ImageTk

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.game = Game(self)
        self.grid()
        self.create_widgets()
    
    def create_widgets(self):
        #design widgets
        title = Label(self, text="Pokemon Battle", font=("Ariel", 20))

        # Button Frame for initial actions
        self.button_frame = Frame(self)

        #Image Frame
        #img = ImageTk.PhotoImage(Image.open(""))
        self.image_frame = Frame(self)

        #Image Boxes for pokemon images
        self.txt_Box_1 = Text(self.image_frame, width=45,height=10)
        self.txt_Box_2 = Text(self.image_frame, width=45,height=10)
        self.txt_Box_3 = Text(self, width=90, height=10)

        self.health_Frame = Frame(self)

        self.attack_Frame = Frame(self)
        
        #Buttons from startup
        self.starter_pokemon = Button(self.button_frame, text="Choose Pokemon",height=2,width=15, command=self.choose_pokemon)
        self.stored_pokemon_list = Button(self.button_frame, text="Stored Pokemon",height=2,width=15, command=self.stored_pokemon)
        self.battle_button = Button(self.button_frame,text="Battle",height=2,width=15,command=lambda: self.game.start_battle())
        self.inventory_button = Button(self.button_frame,text="Inventory",height=2,width=15,command=lambda: self.use_item)

        # Draw Widgets on screen
        # Main Frame
        title.grid(row=0, column=0, sticky='we')
        self.button_frame.grid(row=1, column=0, padx=10, pady=10)
        self.image_frame.grid(row=2, column=0, padx=10, pady=10)
        self.health_Frame.grid(row=3, column=0, padx=10, pady=10)
        self.attack_Frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        self.txt_Box_1.grid(row=2, column=0, sticky='w')
        self.txt_Box_2.grid(row=2, column=1, sticky='e', padx=10)
        self.txt_Box_3.grid(row=4, column=0, sticky='e')

        #Button Frame
        self.starter_pokemon.grid(row=0, column=0, padx=5, pady=5)
        self.stored_pokemon_list.grid(row=0, column=1, padx=5, pady=5)
        self.battle_button.grid(row=0, column=2, padx=5, pady=5)
        self.inventory_button.grid(row=0, column=3, padx=5, pady=5)

        self.player_health = Label(self.health_Frame, text="Player Health:")
        self.player_health_canvas = Canvas(self.health_Frame, width=200, height=20, bg='Red')
        self.player_health.grid(row=0, column=0, padx=50, pady=5)
        self.player_health_canvas.grid(row=1, column=0, padx=50, pady=5)
        self.cpu_health = Label(self.health_Frame, text="Opponent Health:")
        self.cpu_health_canvas = Canvas(self.health_Frame, width=200, height=20, bg='Red')

        self.cpu_health.grid(row=0, column=1, padx=50, pady=5)
        self.cpu_health_canvas.grid(row=1, column=1, padx=50, pady=5)
        

    def use_item(self,selected_item):
        """Open a new window to display the player's inventory."""
        new_window = Toplevel(self)
        new_window.title("Inventory")
        new_window.geometry("300x300")

        labelname = Label(new_window, text="Inventory:")
        labelname.pack(pady=10)

        for items, count in self.game.inventory.items():
            Button(new_window, 
                   text=f"{items}: {count}",
                   height=2,
                   width=10,
                   command=lambda item=items: self.game.use_inventory_item(item)
                   ).pack(pady=5)
        return selected_item

    def choose_pokemon(self):
        """Open window for choosing a starter Pokémon."""
        if self.game.first_run:
            new_window = Toplevel(self)
            new_window.title("Choose Pokemon")
            new_window.geometry("300x300")

            labelname = Label(new_window, text="Choose your starter Pokemon")
            labelname.pack(pady=10)
        
            starter_pokemon = [pokemon for pokemon in self.game.pokemon_list if pokemon.name in ["Bulbasaur", "Charmander", "Squirtle"]]
            for pokemon in starter_pokemon:
                button = Button(new_window, text=pokemon.name, command=lambda p=pokemon: self.select_pokemon(p, new_window))
                button.pack(pady=5)

            # Disable button after first use
            self.game.first_run = False
            self.starter_pokemon.config(state=DISABLED)

    def stored_pokemon(self):
        """Display a list of stored Pokémon in a new window."""
        new_window = Toplevel(self)
        new_window.title("Stored Pokemon")
        new_window.geometry("300x300")

        labelname = Label(new_window, text="Stored Pokémon:")
        labelname.pack(pady=10)

        for pokemon in self.game.stored_pokemon:
            Label(new_window, text=pokemon.name).pack()

    def select_pokemon(self, pokemon, window):
        """Select a starter Pokémon and close the window."""
        self.game.selected_pokemon = pokemon
        self.game.stored_pokemon.append(pokemon)
        window.destroy()