import os
import tkinter as tk
import ttkbootstrap as ttk
import pickle
import sklearn

class App (tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Flight Status Predictor")
        self.geometry("800x400")
        self.resizable(False, False)
        self.pages = []
        self.currentPage = 0
        self.pages.append(MainFrame(self))
        self.pages[0].grid(sticky="nswe")
        self.input_data = []

        self.questions = [
                     "What airline are you flying with?", 
                     "What is your origin's airport name?",
                     "What is your destination's airport name?",
                     "What is your departure time (hhmm)?",
                     "What month is it?",
                     "What day of the week is it? (Sunday .. Saturday)",
                     "What is the origin's city name?",
                     "What is the origin's state name?",
                     "What is the destination's city name?",
                     "What is the destination's state name?",
                     "What is the distance?",
                     ]
        
        for i in range(0, len(self.questions)):
            self.pages.append(PageFrame(self, self.questions[i]))
        self.pages.append(PredictionFrame(self))

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def previousPage(self):
        if self.currentPage != 0:
            self.pages[self.currentPage].grid_forget()
            self.currentPage -= 1
            self.pages[self.currentPage].grid(sticky="nswe")

    def nextPage(self):
        if self.currentPage == len(self.pages) - 1:
            self.pages[self.currentPage].grid_forget()
            self.currentPage = 0
            self.pages[0].grid(sticky="nswe")
        else:
            self.pages[self.currentPage].grid_forget()
            self.currentPage += 1
            self.pages[self.currentPage].grid(sticky="nswe")

    def loadPickle(self, pickle_name : str):
        print("asd", os.listdir("./pickles/"))
        return pickle.load(open(f"./pickles/{pickle_name}_unique.pickle", "rb"))

class MainFrame(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        
        ttk.Label(self, text = "Flight Status Predictor", anchor="s", 
                  bootstyle="inverse-primary", font=("Arial", 24, "bold")).grid(row=0, column=0, sticky="nswe")
        
        ttk.Label(self, text = 
                """Input information about your flight and we will predict if it will be on time, 
                delayed, or cancelled.""", anchor="s", justify="center", font=("Arial", 14)).grid(row=1, column=0, sticky="nswe")
        
        tk.Button(self, text="Start", command=lambda: root.nextPage()).grid(row=2, column=0, padx="50", pady="50", sticky="nswe")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

class PageFrame(tk.Frame):
    def __init__(self, root, question: str):
        tk.Frame.__init__(self, root)
        
        ttk.Label(self, text = "Flight Status Predictor", anchor="s", 
                  bootstyle="inverse-primary", font=("Arial", 24, "bold")) \
        .grid(row=0, column=0, columnspan=2, sticky="nswe")
        
        ttk.Label(self, text = question, anchor="s", justify="center", font=("Arial", 14, "bold")).grid(row=1, columnspan=2)
        
        if "time" in question or "distance" in question:
            ttk.Entry(self).grid(row=2, columnspan=2, sticky="nswe")
        else:
            if question == root.questions[0]:
                ttk.Combobox(self, values=list(root.loadPickle("Airline").keys())).grid(row=2, columnspan=2, sticky="nswe")        
            elif question == root.questions[1]:
                ttk.Combobox(self, values=list(root.loadPickle("Origin").keys())).grid(row=2, columnspan=2, sticky="nswe")
            elif question == root.questions[2]:
                ttk.Combobox(self, values=list(root.loadPickle("Dest").keys())).grid(row=2, columnspan=2, sticky="nswe")
            elif question == root.questions[4]:
                ttk.Combobox(self, values=list(root.loadPickle("Month").keys())).grid(row=2, columnspan=2, sticky="nswe")
            elif question == root.questions[5]:
                ttk.Combobox(self, values=[1, 2, 3, 4, 5, 6, 7]).grid(row=2, columnspan=2, sticky="nswe")
            elif question == root.questions[6]:
                ttk.Combobox(self, values=list(root.loadPickle("OriginCityName").keys())).grid(row=2, columnspan=2, sticky="nswe")
            elif question == root.questions[7]:
                ttk.Combobox(self, values=list(root.loadPickle("OriginStateName").keys())).grid(row=2, columnspan=2, sticky="nswe")
            elif question == root.questions[8]:
                ttk.Combobox(self, values=list(root.loadPickle("DestCityName").keys())).grid(row=2, columnspan=2, sticky="nswe")
            elif question == root.questions[9]:
                ttk.Combobox(self, values=list(root.loadPickle("DestStateName").keys())).grid(row=2, columnspan=2, sticky="nswe")
        ttk.Button(self, text="Back", command=lambda: root.previousPage(), bootstyle="danger").grid(padx=10, pady=10, row=3, column=0, sticky="nswe")

        if question == "What is the distance?":
            ttk.Button(self, text="Predict", command=lambda: root.nextPage(), bootstyle="warning").grid(padx=10, pady=10, row=3, column=1, sticky="nswe")
        else:
            ttk.Button(self, text="Next", command=lambda: root.nextPage(), bootstyle="success").grid(padx=10, pady=10, row=3, column=1, sticky="nswe")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

class PredictionFrame(tk.Frame):
    def __init__(self, root: str):
        tk.Frame.__init__(self, root)

        ttk.Label(self, text = "Flight Status Predictor", bootstyle="inverse-primary", anchor="s", \
                  justify="center", font=("Arial", 24, "bold")).grid(row=0, column=0, sticky="nswe")
        
        ttk.Label(self, text = "Your flight is predicted to be...", anchor="s", \
                  justify="center", font=("Arial", 18, "bold")).grid(row=1, column=0, sticky="nswe")

        ttk.Label(self, text = "Cancelled", anchor="s", \
                  justify="center", font=("Arial", 24, "bold")).grid(row=2, column=0, sticky="nswe")

        root.currentPage = 0

        ttk.Button(self, text="New Prediction", command=lambda: root.nextPage()).grid(row=3, column=0, padx="50", pady="50", sticky="nswe")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)