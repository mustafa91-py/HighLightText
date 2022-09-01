import datetime
import random

from high_light_text import HighLightText
from tkinter import *

TEXT = """Python is a programming language that lets you work more quickly and integrate your systems more 
effectively.Python is a clear and powerful object-oriented programming language, comparable to Perl, Ruby, Scheme, 
or Java The tkinter package (“Tk interface”) is the standard Python interface to the Tcl/Tk GUI toolkit. Both Tk and 
tkinter are available on most Unix platforms, including macOS, as well as on Windows systems.\nwhat time is it? """

URL = {"tkinter": "https://docs.python.org/3/library/tkinter.html",
       "python": "https://www.python.org/"}


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()

        self.label = Label(self, text="info")
        self.label.pack(side="top", fill="x")

        self.text = HighLightText(self)
        self.text.pack(fill="both", expand=1)
        self.text.insert(0.0, TEXT)

        for i in URL:
            self.text.command(i, "<Button-1>", self.info, config={"foreground": "red"}, ignore_case=True)

        self.text.command("time",
                          "<Button-1>",
                          lambda e: self.label.config(text=str(datetime.datetime.now())),
                          config=dict(background="green"))

    def info(self, event):
        tag = event.widget.current_tag
        url = URL.get(str(tag).lower())
        r, g, b = [random.randint(20, 255) for i in range(3)]
        self.label.config(text=f"{url=}", bg=self.text.colorHex((r, g, b)))


r = Root()
r.mainloop()
