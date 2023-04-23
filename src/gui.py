import tkinter as tk
from tkinter import filedialog
import sys

class FactsData:
    data:dict = {}
    backPath:str=""
    
    def __init__(self):
        facts:list = []            

        root = tk.Tk()
        root.resizable(0,0)
        root.title("Shorts Maker with python by x64-tech")

        titleframe = tk.LabelFrame(root, text="Title")
        titleframe.pack(padx=10, pady=10, fill= "both")
        
        titleEntry = tk.Text(titleframe, width=30, height=2)
        titleEntry.grid(row=0, column=0, padx=5, pady=10)

        def select_file():
            self.data["title"] = {"text":titleEntry.get("1.0", "end-1c"), "image":filedialog.askopenfilename()}
            
        tk.Button(titleframe, text="Select Image", command=select_file).grid(row=0, column=1, padx=5, pady=5)


        def backSet():  self.backPath = filedialog.askopenfilename()

        selectBack= tk.Button(root, text="Select Background", 
                               command=backSet)
        selectBack.pack(fill="both", padx=10)

        factFrame = tk.LabelFrame(root, text="Add Facts")
        factFrame.pack(padx=10, pady=10, fill= "both") 
        

        f1 = tk.Text(factFrame, width=30, height=2)
        f1.grid(row=0, column=0)
        tk.Button(factFrame, text="select image", 
                  command=lambda : facts.append({"fact":f1.get("1.0", "end-1c"), "image":filedialog.askopenfilename()})).grid(row=0, column=1, padx=5, pady=5)

        f2 = tk.Text(factFrame, width=30, height=2)
        f2.grid(row=1, column=0)
        tk.Button(factFrame, text="select image", 
                  command=lambda : facts.append({"fact":f2.get("1.0", "end-1c"), "image":filedialog.askopenfilename()})).grid(row=1, column=1, padx=5, pady=5)

        f3 = tk.Text(factFrame, width=30, height=2)
        f3.grid(row=2, column=0)
        tk.Button(factFrame, text="select image", 
                  command=lambda : facts.append({"fact":f3.get("1.0", "end-1c"), "image":filedialog.askopenfilename()})).grid(row=2, column=1, padx=5, pady=5)

        f4 = tk.Text(factFrame, width=30, height=2)
        f4.grid(row=3, column=0)
        tk.Button(factFrame, text="select image", 
                  command=lambda : facts.append({"fact":f4.get("1.0", "end-1c"), "image":filedialog.askopenfilename()})).grid(row=3, column=1, padx=5, pady=5)

        f5 = tk.Text(factFrame, width=30, height=2)
        f5.grid(row=4, column=0)
        tk.Button(factFrame, text="select image", 
                  command=lambda : facts.append({"fact":f5.get("1.0", "end-1c"), "image":filedialog.askopenfilename()})).grid(row=4, column=1, padx=5, pady=5)

        def proc():
            self.data["facts"] = facts
            root.destroy()

        contFrame = tk.Frame(root)
        contFrame.pack(padx=10, pady=5, fill= "both")

        proceedAhed= tk.Button(contFrame, text="Create Video", command=proc)
        proceedAhed.grid(row=0, column=0, padx=5, pady=10)

        exitbtn =tk.Button(contFrame, text="Exit", command=lambda:sys.exit())
        exitbtn.grid(row=0, column=1, padx=5, pady=10)
        
        root.mainloop()
    
    def get(self):
        return (self.data, self.backPath)