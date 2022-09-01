import datetime
import os.path
import tkinter
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.font import Font
import random


class HighLightText(ScrolledText):
    def __init__(self, parent, **kwargs):
        super(HighLightText, self).__init__(parent, **kwargs)
        self.widget = parent
        self.dict_data = {}
        self.colorHex = lambda rgb: "#%02x%02x%02x" % rgb
        self.words_coord = {}
        self.words_widget = {}
        self.words_widget_func = {}
        self.words_widget_sequence = {}
        self.words_config = {}
        self.current_tag = None
        self.bind("<Motion>", self.__track)

    def command(self, tag, sequence=None, func=None, config: dict = None):
        self.words_widget_func[tag] = func
        self.words_widget_sequence[tag] = sequence
        self.words_config[tag] = config

    def __items(self, item="=", config: dict = None):
        import re
        data = self.get(0.0, "end")
        self.dict_data = {k + 1: v for k, v in enumerate(str(data).split("\n"))}
        for k, v in self.dict_data.items():
            for i in re.finditer(re.escape(item), v):
                coord_ = f"{k}.{i.start()}", f"{k}.{i.end()}"
                self.words_coord[coord_] = item
                if item not in self.words_widget:
                    self.words_widget[item] = Button()
                self.tag_add(item, f"{k}.{i.start()}", f"{k}.{i.end()}")
                self.tag_config(item, **config)

    def __capsule(self):
        self.words_coord.clear()
        for k in self.words_widget_func:
            __config = self.words_config.get(k)
            if __config and isinstance(__config, dict):
                cnf = __config
            else:
                cnf = {}
            self.__items(k, config=cnf)

    def __track(self, event):
        self.__capsule()
        index = event.widget.index(f"@{event.x},{event.y}")
        for k, v in self.words_coord.items():
            self.unbind(self.words_widget_sequence.get(v))
            cursor_ = cursor_row_, cursor_col = str(index).split(".")
            tag_start = tag_start_row, tag_start_col = str(k[0]).split(".")
            tag_end = tag_end_row, tag_end_col = str(k[1]).split(".")
            if cursor_row_ == tag_start_row == tag_end_row and int(tag_start_col) < int(cursor_col) < int(
                    tag_end_col):
                self.current_tag = v
                self.bind(self.words_widget_sequence.get(v), self.words_widget_func.get(v))
                return
            else:
                pass


if __name__ == '__main__':
    root = Tk()


    def change(event):
        top.state("normal")
        tag = event.widget.current_tag
        top.title(tag)
        label.config(image="")
        r, g, b = [random.randint(1, 255) for i in range(3)]
        label["bg"] = highlight_text.colorHex((r, g, b))
        label["text"] = f"{tag} = {datetime.datetime.now()}"


    def date(event):
        top.state("normal")
        tag = event.widget.current_tag
        top.title(tag)
        r, g, b = [random.randint(1, 255) for i in range(3)]
        label.config(image="")
        label["bg"] = highlight_text.colorHex((r, g, b))
        label["text"] = f"{tag} = {datetime.date.today()}"


    try:
        img_ = PhotoImage(file=os.path.join(os.getcwd(), "python_img.png"))
    except tkinter.TclError:
        img_ = None


    def open_python(event):
        tag = event.widget.current_tag
        top.title(tag)
        top.state("normal")
        label.config(image=img_,text="image not found")


    def my_widget(event):
        top.state("normal")

        tag = event.widget.current_tag
        top.title(tag)

        label.config(image="")
        label.config(text=f"{tag} : {type(event.widget).__name__=}")


    highlight_text = HighLightText(root)
    highlight_text.pack(fill="both", expand=1)

    top = Toplevel(root)
    top.state("withdraw")
    top.protocol("WM_DELETE_WINDOW", lambda: top.state("withdraw"))
    top.wm_attributes("-topmost", 1)

    label = Label(top, text="info")
    label.pack(fill="both", expand=1)

    highlight_text.command("today", "<Button-1>", func=change, config=dict(font=Font(underline=1), background="gray"))

    highlight_text.command("date", "<Button-1>", func=date, config=dict(font=Font(underline=1), foreground="green"))

    highlight_text.command("python", "<Button-1>", func=open_python,
                           config=dict(font=Font(underline=1, family="Arial", weight="bold")))

    highlight_text.command("widget", "<Button-1>", func=my_widget, config={"background": "red"})

    highlight_text.insert(0.0, "date? today ? \nthis is a python image \nwhat is widget name?")

    root.mainloop()
