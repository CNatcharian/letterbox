# Heya! This is an experiment by Chris Natcharian.
# A very simple programming language of this form:
# Pa (print var a) Sa3 (set a to 3)

# This file is a GUI-based Letterbox Editor.

import tkinter as tk
import tkinter.filedialog as fd
import letterbox as lb

class LBGUI(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master, padx=5, pady=5)
        self.grid()
        self.createWidgets()
        self.box = lb.Letterbox()

    def createWidgets(self):
        # Quit button
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(row=0, column=3)
        # Save button
        self.saveButton = tk.Button(self, text='Save', command=self.filesave)
        self.saveButton.grid(row=0, column=1)
        # Run button
        self.runButton = tk.Button(self, text='Run', command=self.filerun)
        self.runButton.grid(row=0, column=2)
        # Load button
        self.openButton = tk.Button(self, text='Open', command=self.fileload)
        self.openButton.grid(row=0, column=0)

        # Code window
        self.codew = tk.Text(self,
                             height=20, width=80,
                             wrap=tk.WORD,
                             padx=2, pady=2)
        self.codew.grid(row=1, column=0, columnspan=4)

        # Output window
        self.outw = tk.Text(self,
                            height=10, width=80,
                            wrap=tk.WORD,
                            padx=2, pady=2)
        self.outw.grid(row=2, column=0, columnspan=4)

    # Saves the contents of the code window to a file.
    def filesave(self):
        t = self.codew.get("1.0","end")
        savelocation = fd.asksaveasfilename(filetypes=(("Letterbox file","*.lb"),
                                                       ("All files", "*.*")))
        file1 = open(savelocation, "w+")
        file1.write(t)
        file1.close()

    # Opens a file in the code window.
    def fileload(self):
        floc = fd.askopenfile(filetypes=(("Letterbox file","*.lb"),
                                         ("All files", "*.*")))
        f1 = open(floc, "r")
        t = f1.read()
        self.codew.delete("1.0", "end")
        self.codew.insert(t, "end")

    # Runs the code in codew and puts the output into outw.
    def filerun(self):
        t = self.codew.get("1.0", "end-1c")
        lines = t.split("\n")
        self.box.reset_data()
        self.outw.delete("1.0", "end")
        for line in lines:
            self.box.set_input(line)
            self.box.clear_output()
            self.box.parse_exec()
            out = self.box.get_output()
            if out != "":
                self.outw.insert("end", out + "\n")

app = LBGUI()
app.master.title('Letterbox Editor')
app.mainloop()