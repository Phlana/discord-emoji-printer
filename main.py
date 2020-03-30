"""
discord large emoji shit
"""

import tkinter as tk
import tkinter.ttk as ttk


class Window:
    def __init__(self):
        self.emoji = None
        self.window = tk.Tk()
        self.window.title('big emoji')
        self.window.iconbitmap('app.ico')

        # parent input frame
        parent_frame = tk.Frame(self.window)
        # frame for text output
        self.output_frame = tk.Frame(self.window)
        self.textbox = None

        # label frame
        label_frame = tk.Frame(parent_frame)
        self.tk_labels = list()

        self.tk_labels.append(tk.Label(label_frame, text='prefix'))
        self.tk_labels.append(tk.Label(label_frame, text='rows'))
        self.tk_labels.append(tk.Label(label_frame, text='columns'))
        self.tk_labels.append(tk.Label(label_frame, text='padding'))

        # adding elements to label frame
        for i in range(len(self.tk_labels)):
            label_frame.grid_rowconfigure(i, minsize=25)
            self.tk_labels[i].grid(row=i, sticky='e')

        # input frame
        input_frame = tk.Frame(parent_frame)
        self.tk_inputs = list()
        
        self.tk_inputs.append(tk.Entry(input_frame))
        self.tk_inputs.append(tk.Spinbox(input_frame, from_=1, to=20))      # row count
        self.tk_inputs.append(tk.Spinbox(input_frame, from_=1, to=20))      # column count
        self.tk_inputs.append(tk.Spinbox(input_frame, values=(0, 2, 3)))    # padding amount
        self.zi = tk.BooleanVar()                                           # zero indexed
        self.tk_inputs.append(tk.Checkbutton(input_frame, text='zero indexed', variable=self.zi))

        # adding elements to input frame
        for i in range(len(self.tk_inputs)):
            input_frame.grid_rowconfigure(i, minsize=25)
            self.tk_inputs[i].grid(row=i, sticky='w')

        # adding elements to parent frame
        label_frame.grid(row=0, column=0, padx=6, sticky='n')
        ttk.Separator(parent_frame, orient='vertical').grid(row=0, column=1, sticky='ns')
        input_frame.grid(row=0, column=2, padx=6, sticky='n')
        ttk.Separator(parent_frame, orient='horizontal').grid(row=6, column=0, columnspan=3, sticky='ew', pady=(0, 15))
        tk.Button(parent_frame, text='generate', command=self.generate, width=7).grid(row=7, column=2)
        tk.Button(parent_frame, text='clear', command=self.clear, width=7).grid(row=8, column=2)

        # display panel
        parent_frame.pack(anchor='n', padx=10, pady=15, side='left')

    def start(self):
        self.window.mainloop()

    def generate(self):
        prefix = self.tk_inputs[0].get()
        row = int(self.tk_inputs[1].get())
        col = int(self.tk_inputs[2].get())
        zero_index = self.zi.get()
        padding = int(self.tk_inputs[3].get())

        self.emoji = Emoji(prefix, row, col, zero_index, padding)
        self.emoji.make()
        # self.emoji.print()
        self.display_emoji()

    def clear(self):
        if self.output_frame.winfo_exists():
            self.output_frame.destroy()
            self.output_frame = tk.Frame(self.window)

    def display_emoji(self):
        self.clear()
        self.textbox = tk.Text(self.output_frame)

        for i in range(len(self.emoji.contents)):
            for el in self.emoji.contents[i]:
                self.textbox.insert('insert', el)
            if i != len(self.emoji.contents) - 1:
                self.textbox.insert('insert', '\n')
        self.textbox.insert('end', '')

        ttk.Separator(self.output_frame, orient='vertical').pack(fill='y', expand=True, side='left')
        self.textbox.pack(side='left')

        self.output_frame.pack(fill='y', expand=True, anchor='n', side='left')

        self.update_text_size()

    def update_text_size(self):
        width = 0
        height = float(self.textbox.index('end'))

        for line in self.textbox.get('1.0', 'end').split('\n'):
            if len(line) > width:
                width = len(line)

        self.textbox.config(width=width, height=height)


class Emoji:
    def __init__(self, p, r, c, index, padding):
        self.prefix = p
        self.rows = r
        self.cols = c
        self.index = index
        self.padding = padding

        self.contents = list()

    def make(self):
        i = 0
        for row in range(self.rows):
            row_list = list()
            for col in range(self.cols):
                if self.index:
                    row_list.append(':' + self.prefix + str(i).zfill(self.padding) + ':')
                else:
                    row_list.append(':' + self.prefix + str(i + 1).zfill(self.padding) + ':')
                i += 1
            self.contents.append(row_list)

    def print(self):
        for row in self.contents:
            for el in row:
                print(el, end='')
            print()


if __name__ == '__main__':
    window = Window()
    window.start()
