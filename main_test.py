import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk

class DragDropTreeview(ttk.Treeview):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self["show"] = "tree headings"  # Remove hidden root row
        self.bind("<ButtonPress-1>", self.on_item_pressed)
        self.bind("<B1-Motion>", self.on_item_dragged)
        self.bind("<ButtonRelease-1>", self.on_item_released)

        self.dragging_item = None

    def on_item_pressed(self, event):
        item = self.identify_row(event.y)
        if item:
            self.dragging_item = item

    def on_item_dragged(self, event):
        if self.dragging_item:
            self.configure(cursor="hand2")

    def on_item_released(self, event):
        if not self.dragging_item:
            return

        target_item = self.identify_row(event.y)
        if not target_item or target_item == self.dragging_item:
            return

        dragging_parent = self.parent(self.dragging_item)
        target_parent = self.parent(target_item)

        if target_parent == "":
            new_parent = target_item
            new_index = "end"
        else:
            new_parent = target_parent
            new_index = self.index(target_item) + 1

        self.move(self.dragging_item, new_parent, new_index)
        self.configure(cursor="")
        self.dragging_item = None

class ListManagerApp:
    def __init__(self, root:tk.Tk):
        self.root = root
        self.root.title("Drag & Drop List Manager")
        self.root.geometry("600x400")
        
        # Container Frame for Treeview
        self.tree_frame = tk.Frame(root, borderwidth=2, relief="sunken") # width = 400
        self.tree_frame.place(x=10,y=10)

        self.tree = DragDropTreeview(self.tree_frame, self, columns=("lnColor","lnTextColor","stnCode","plus"))
        
        # Define Column Headers
        self.tree.heading("#0", text="Line Name")  # Main tree column
        self.tree.heading("lnColor", text="Line Color")
        self.tree.heading("lnTextColor", text="Line Text Color")
        self.tree.heading("stnCode", text="Stn. Num.")
        self.tree.heading("plus", text="[+]")
        
        # Column Config
        self.tree.column("#0", width=100, stretch=True,anchor="w")
        self.tree.column("lnColor", width=100, anchor="w")
        self.tree.column("lnTextColor", width=100, anchor="w")
        self.tree.column("stnCode", width=60, anchor="w")
        self.tree.column("plus", width=40,anchor="center") #tba: default height 20
        
        # Click Binds
        self.tree.bind("<Button-1>", self.on_header_click) # add group
        self.tree.bind("<Button-1>", self.on_group_click,add="+") # add item
        self.tree.bind("<Double-1>", self.on_cell_double_click) # edit item/properties
        self.tree.bind("<<TreeviewSelect>>", self.on_select) #select
        
        # Scrollbar
        self.tree_scroll = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scroll.set)

        # Layout inside the frame
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Item Properties
        self.item_properties = {}
        self.color_images = {}
        self.default_properties = ("#ffffff","black","01")

        self.populate_tree()

    def populate_tree(self):
        #self.tree.delete(*self.tree.get_children())

        for i in range(1, 4):
            group_id = self.tree.insert("", "end", text=f" Group {i}", values=("","","","[+]"), open=True)
            for j in range(2):
                new_item = self.tree.insert(group_id, "end", text=f"Item {chr(64+j+2*i-1)}", values=("#ffffff","black","01"),tags=("color"))
                new_bgColor = str(self.tree.set(new_item,self.tree["columns"][0]))
                new_fgColor = str(self.tree.set(new_item,self.tree["columns"][1]))
                self.apply_color(new_item,new_bgColor,new_fgColor)
                #img = self.color_image(new_bgColor)  # Generate color block

        
        self.style = ttk.Style()
        self.style.theme_use("vista")

        self.style.map(
            "Treeview",
            background=[("disabled", "SystemButtonFace"),("selected", "#99ccff")],  # Keep the background unchanged when selected
            foreground=[("disabled", "SystemGrayText"),("selected", "black")],  # Keep text color normal
        )
        
        self.style.configure("Treeview.Item", padding=0)

    ## Color Functions

    def apply_color(self, item_id, bgColor, fgColor):
        """Apply background color to a treeview row using tags."""
        colorTag = f"color_{bgColor}_{fgColor}"  # Create a unique tag for the color
        
        self.tree.tag_configure(colorTag, background=bgColor, foreground=fgColor)
        self.tree.item(item_id, tags=(colorTag))

    ## Click Functions

    def on_header_click(self, event):
        """Detects clicks on the 'Add Group' text inside the header."""
        region = self.tree.identify("region", event.x, event.y)
        col = self.tree.identify_column(event.x)
        if region == "heading" and col == "#5":  # If clicked in the first column header
            self.add_group()
            
    def on_group_click(self, event):
        item = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)
        if item and col == "#5" and self.tree.parent(item) == "":
            self.add_line(item)
            
    def on_cell_double_click(self, event):
        """Open an Entry widget when double-clicking a cell."""
        item_id = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)

        if col == "#0":
            self.tree.after(0, lambda: self.tree.item(item_id, open=True))  # Keep group open

        if (not item_id) or col == ("#2" or "#5"):  # Don't edit the first column
            return
        
        # Check if the item is a group (i.e., its parent is "")
        if (self.tree.parent(item_id) == "" and not col == "#0"):
            return  # Stop execution, so groups are not editable

        if col == "#0":
            current_value = self.tree.item(item_id, "text")  # Get item name
        else:
            col_name = self.tree["columns"][int(col[1:]) - 1]  # Get column name(columns is a dict key)
            current_value = self.tree.set(item_id, col_name)  # Get current cell value
        x, y, width, height = self.tree.bbox(item_id, col)  # Get cell position

        entry = tk.Entry(self.tree)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, current_value)  # Insert current value
        entry.focus()
        
        def save_value(event=None):
            """Save the new value back into the Treeview."""
            new_value = entry.get()
            if col == "#0":
                self.tree.item(item_id, text=new_value)  # Update item name properly
            else:
                self.tree.set(item_id, col_name, new_value)  # Update property value
            new_bgColor = self.tree.set(item_id,self.tree["columns"][0])
            new_fgColor = self.tree.set(item_id,self.tree["columns"][1])
            self.apply_color(item_id, new_bgColor,new_fgColor)
            
            entry.destroy()
            
        entry.bind("<Return>", save_value)
        entry.bind("<FocusOut>", save_value)

    def on_select(self, event):
        """Draw the outline around the selected item."""
        # Get the selected item and create a rectangle around it
        for item in self.tree.selection():
            bgColor = self.tree.set(item,self.tree["columns"][0])
            fgColor = self.tree.set(item,self.tree["columns"][1])
            self.apply_color(item,bgColor,fgColor)  
                
    ## Add Object Functions

    def add_group(self):
        """Adds a new group to the treeview."""
        group_count = len(self.tree.get_children()) + 1
        group_id = self.tree.insert("", "end", text=f" Group {group_count}", values=("","","","[+]"), open=True)

    def add_line(self, group_id, color):
        if group_id:
            line_count = len(self.tree.get_children(group_id))
            new_name = f"Line {line_count}"
            
            new_item = self.tree.insert(group_id, "end", text=new_name, values=("#ffffff","black","01"))
            new_bgColor = self.tree.set(new_item,self.tree["columns"][0])
            new_fgColor = self.tree.set(new_item,self.tree["columns"][1])
            self.apply_color(new_item, new_bgColor, new_fgColor)

if __name__ == "__main__":
    root = tk.Tk()
    app = ListManagerApp(root)
    root.mainloop()