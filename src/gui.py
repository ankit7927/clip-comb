import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox

class DataCollector:
    data:list = []
    backPath:str=None

    title_image:str = None
    text_image:str = None
    
    def __init__(self):

        window = tk.Tk()
        window.resizable(0, 0)
        window.title("Video Editor")

        frame1 = ttk.LabelFrame(window, text="Title")
        frame1.pack(pady=6, fill="both", padx=10)

        video_type_var = tk.StringVar()
        video_type_dropdown = ttk.Combobox(frame1, textvariable=video_type_var, values=["Vertical", "Horizontal"], width=20)
        video_type_dropdown.current(0)
        video_type_dropdown.grid(row=0, column=0, padx=5, pady=5)

        title_entry = ttk.Entry(frame1, width=40)
        title_entry.grid(row=0, column=2, padx=5, pady=5)

        def select_image():

            filetypes = (("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*"))
            self.title_image = filedialog.askopenfilename(title="Select Image", filetypes=filetypes)

        image_button = ttk.Button(frame1, text="Select Image", command=select_image)
        image_button.grid(row=0, column=3, padx=5, pady=5)

        def select_back():
            filetypes = (("Video file", "*.mp4"), ("All files", "*.*"))
            self.backPath = filedialog.askopenfilename(title="Select Background", filetypes=filetypes)


        back_button = ttk.Button(frame1, text="Select Background", command=select_back)
        back_button.grid(row=0, column=4, padx=5, pady=5)

        table = ttk.Treeview(window, columns=("text", "image"), show="headings", selectmode="browse")
        table.heading("text", text="Text")
        table.heading("image", text="Image")
        table.pack(padx=10, pady=5, fill="both")

        frame2 = ttk.LabelFrame(window, text="Add Text")
        frame2.pack(pady=6, fill="both", padx=10)

        text_entry = ttk.Entry(frame2, width=50)
        text_entry.grid(row=0, column=0, padx=5, pady=5)

        def select_image_frame2():
            filetypes = (("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*"))
            self.text_image = filedialog.askopenfilename(title="Select Image", filetypes=filetypes)

        image_button_frame2 = ttk.Button(frame2, text="Select Image", command=select_image_frame2)
        image_button_frame2.grid(row=0, column=1, padx=5, pady=5)

        def save_text():
            text = text_entry.get()

            if not text or not self.text_image:
                messagebox.showwarning("Alert", "both text and image is required")
                return
            table.insert("", tk.END, values=(text, self.text_image))
            self.text_image = None
            text_entry.delete(0, tk.END)

        save_button = ttk.Button(frame2, text="Save", command=save_text)
        save_button.grid(row=0, column=2, padx=5, pady=5)

        def delete_video():
            selected_item = table.selection()
            if selected_item:
                table.delete(selected_item)

        delete_button = ttk.Button(frame2, text="Delete", command=delete_video)
        delete_button.grid(row=0, column=4, padx=5, pady=5)

        def done():

            if len(table.get_children()) == 0:
                messagebox.showwarning("Alert", "No text is given")
                return

            title = title_entry.get()
            if title == "" or self.backPath == None or self.title_image == None:
                messagebox.showwarning("Alert", "title, image and backgroung are required")
                return
            self.data.insert(0, {"text":title, "image":self.title_image})
            
            for item in table.get_children():
                text = table.item(item, 'values')[0]
                image = table.item(item, 'values')[1]

                self.data.append({"text":text, "image":image})
            window.destroy()

        done_button = ttk.Button(window, text="Done", command=done)
        done_button.pack(pady=10, padx=10, fill="both")

        window.mainloop()
    
    def get(self):
        return (self.data, self.backPath)