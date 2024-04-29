import tkinter as tk
import ttkbootstrap as ttk
import pickle
import locale
from sklearn import tree

# Flight Status Predictor, based on https://www.kaggle.com/datasets/robikscube/flight-delay-dataset-20182022/data
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
        ## 11 questions/inputs, 11 variables
        self.input_data = [tk.StringVar() for i in range(11)]
        self.prediction = tk.StringVar()
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
        # Load all intermediate pages (not the mainFrame or predictionFrame)
        for i in range(0, len(self.questions)):
            self.pages.append(PageFrame(self, self.questions[i]))
        # Load the prediction frame
        self.pages.append(PredictionFrame(self))

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    # Render the previous page in the pages list
    def previousPage(self):
        if self.currentPage != 0:
            self.pages[self.currentPage].grid_forget()
            self.currentPage -= 1
            self.pages[self.currentPage].grid(sticky="nswe")

    # Render the next page in the pages list
    def nextPage(self):
        if self.currentPage == len(self.pages) - 1:
            self.pages[self.currentPage].grid_forget()
            self.currentPage = 0
            self.pages[0].grid(sticky="nswe")
        else:
            self.pages[self.currentPage].grid_forget()
            self.currentPage += 1
            self.pages[self.currentPage].grid(sticky="nswe")

    # Load the pickle file given a name (either data dicts or the model)
    def loadPickle(self, pickle_name : str):
        return pickle.load(open(f"./pickles/{pickle_name}_unique.pickle", "rb"))

    # Loadl the model and call the prediction with the input data given
    def predict(self):
        locale.setlocale(locale.LC_ALL, "en_US.utf8")

        # Decision Tree Clasification
        model = pickle.load(open("./pickles/flight_predictor_model.pickle", "rb"))
        model_input = []

        model_input.append(self.loadPickle("Airline")[self.input_data[0].get()])
        model_input.append(self.loadPickle("Origin")[self.input_data[1].get()])
        model_input.append(self.loadPickle("Dest")[self.input_data[2].get()])
        model_input.append(float(self.input_data[3].get()))
        model_input.append(self.loadPickle("Month")[self.input_data[4].get()])
        model_input.append(int(self.input_data[5].get()))
        model_input.append(self.loadPickle("OriginCityName")[self.input_data[6].get()])
        model_input.append(self.loadPickle("OriginStateName")[self.input_data[7].get()])
        model_input.append(self.loadPickle("DestCityName")[self.input_data[8].get()])
        model_input.append(self.loadPickle("DestStateName")[self.input_data[9].get()]) 
        model_input.append(locale.atof(self.input_data[10].get()))

        model_input = [model_input]
        prediction = model.predict(model_input)

        if prediction == 1:
            self.prediction.set("Delayed")
        elif prediction == 2:
            self.prediction.set("On Time")
        elif prediction == 3:
            self.prediction.set("Cancelled")
        # Move to the final page when done
        self.nextPage()

# First page, introduction/starting page
class MainFrame(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        
        ttk.Label(self, text = "Flight Status Predictor", anchor="s", 
                  bootstyle="inverse-primary", font=("Arial", 24, "bold")).grid(row=0, column=0, sticky="nswe")
        
        ttk.Label(self, text = 
                """Input information about your flight and we will predict if it will be on time, 
                delayed, or cancelled.""", anchor="s", justify="center", font=("Arial", 14)).grid(row=1, column=0, sticky="nswe")
        
        tk.Button(self, text="Start", command=root.nextPage).grid(row=2, column=0, padx="50", pady="50", sticky="nswe")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

# Each page corresponds to one question
class PageFrame(tk.Frame):
    def __init__(self, root, question: str):
        tk.Frame.__init__(self, root)
        
        ttk.Label(self, text = "Flight Status Predictor", anchor="s", 
                  bootstyle="inverse-primary", font=("Arial", 24, "bold")) \
        .grid(row=0, column=0, columnspan=2, sticky="nswe")
        
        ttk.Label(self, text = question, anchor="s", justify="center", font=("Arial", 14, "bold")).grid(row=1, columnspan=2)
        
        if "time" in question:
                        ttk.Entry(self, textvariable=root.input_data[3], validate="focusout") \
            .grid(row=2, columnspan=2, sticky="nswe")
        elif "distance" in question:
                        ttk.Entry(self, textvariable=root.input_data[10], validate="focusout") \
            .grid(row=2, columnspan=2, sticky="nswe")

        else:
            if question == root.questions[0]:
                ttk.Combobox(self, values=sorted(list(root.loadPickle("Airline").keys())), \
                             textvariable=root.input_data[0], validate="focusout").grid(row=2, columnspan=2, sticky="nswe")        
            elif question == root.questions[1]:
                ttk.Combobox(self, values=sorted(list(root.loadPickle("Origin").keys())), \
                             textvariable=root.input_data[1], validate="focusout").grid(row=2, columnspan=2, sticky="nswe")
            elif question == root.questions[2]:
                ttk.Combobox(self, values=sorted(list(root.loadPickle("Dest").keys())), \
                             textvariable=root.input_data[2], validate="focusout").grid(row=2, columnspan=2, sticky="nswe")
            elif question == root.questions[4]:
                ttk.Combobox(self, values=sorted(list(root.loadPickle("Month").keys()), key=int), \
                             textvariable=root.input_data[4], validate="focusout").grid(row=2, columnspan=2, sticky="nswe")
            elif question == root.questions[5]:
                ttk.Combobox(self, values=[1, 2, 3, 4, 5, 6, 7], \
                             textvariable=root.input_data[5], validate="focusout").grid(row=2, columnspan=2, sticky="nswe")
            elif question == root.questions[6]:
                ttk.Combobox(self, values=sorted(list(root.loadPickle("OriginCityName").keys())), \
                             textvariable=root.input_data[6], validate="focusout").grid(row=2, columnspan=2, sticky="nswe")
            elif question == root.questions[7]:
                ttk.Combobox(self, values=sorted(list(root.loadPickle("OriginStateName").keys())), \
                             textvariable=root.input_data[7], validate="focusout").grid(row=2, columnspan=2, sticky="nswe")
            elif question == root.questions[8]:
                ttk.Combobox(self, values=sorted(list(root.loadPickle("DestCityName").keys())), \
                             textvariable=root.input_data[8], validate="focusout").grid(row=2, columnspan=2, sticky="nswe")
            elif question == root.questions[9]:
                ttk.Combobox(self, values=sorted(list(root.loadPickle("DestStateName").keys())), \
                             textvariable=root.input_data[9], validate="focusout").grid(row=2, columnspan=2, sticky="nswe")
        ttk.Button(self, text="Back", command=root.previousPage, bootstyle="danger").grid(padx=10, pady=10, row=3, column=0, sticky="nswe")

        if question == "What is the distance?":
            ttk.Button(self, text="Predict", command=root.predict, bootstyle="warning").grid(padx=10, pady=10, row=3, column=1, sticky="nswe")
        else:
            ttk.Button(self, text="Next", command=root.nextPage, bootstyle="success").grid(padx=10, pady=10, row=3, column=1, sticky="nswe")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

# Last page containing the prediction
class PredictionFrame(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        ttk.Label(self, text = "Flight Status Predictor", bootstyle="inverse-primary", anchor="s", \
                  justify="center", font=("Arial", 24, "bold")).grid(row=0, column=0, sticky="nswe")
        
        ttk.Label(self, text = "Your flight is predicted to be...", anchor="s", \
                  justify="center", font=("Arial", 18, "bold")).grid(row=1, column=0, sticky="nswe")

        ttk.Label(self, textvariable=root.prediction, anchor="s", \
                  justify="center", font=("Arial", 24, "bold")).grid(row=2, column=0, sticky="nswe")

        root.currentPage = 0

        ttk.Button(self, text="New Prediction", command=root.nextPage).grid(row=3, column=0, padx="50", pady="50", sticky="nswe")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)