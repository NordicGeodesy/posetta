"""Posetta, The Universal Translator of Geodetic Coordinate File Formats

Posetta can convert input in one format to output with a different
format. Input and output can be either files, or stdin and stdout streams.
"""

# Standard library imports
import pathlib
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import ttk
from typing import Callable


# Posetta imports
import posetta
from posetta import readers
from posetta import writers


class CallWrapperReportingException(tk.CallWrapper):
    """Overrides the built-in CallWrapper, so that exceptions happening inside tkinter are reported."""

    def __call__(self, *args):
        """Apply first function SUBST to arguments, then FUNC."""
        try:
            if self.subst:
                args = self.subst(*args)
            return self.func(*args)
        except SystemExit:
            raise
        except:  # noqa
            import traceback
            from tkinter import messagebox

            err = traceback.format_exc()
            print(err)
            messagebox.showerror("Oops ...", err)


tk.CallWrapper = CallWrapperReportingException


class PosettaGui(tk.Tk):
    """A simple GUI frontend to the Posetta command line"""

    def __init__(self, translator: Callable, *args, **kwargs):
        # Set up window
        super().__init__(*args, **kwargs)
        super().wm_title("Posetta")

        # Make sure to keep references to icons
        # TODO: How should we handle setting the gui_dir properly
        gui_dir = pathlib.Path(__file__).parent
        self._posetta_icon = tk.PhotoImage(file=gui_dir / "icon.png")
        self.iconphoto(True, self._posetta_icon)

        self._banner = tk.PhotoImage(file=gui_dir / "banner.png")
        self._satellite_icon = tk.PhotoImage(file=gui_dir / "satellite.png")
        self._stone_icon = tk.PhotoImage(file=gui_dir / "stone.png")

        # Callback function for doing translation between files
        self.translator = translator

        # Variables
        self.vars = dict()

        # Layout: Banner image
        banner_line = ttk.Frame(self)
        banner = tk.Label(banner_line, image=self._banner)
        banner.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
        banner_line.pack(side=tk.TOP, fill=tk.X, expand=False)

        # Layout: From file
        from_file = FileAndFormat(
            self,
            text="Input format and file name:",
            fmt_list=readers.names(),
            var_prefix="reader",
            vars=self.vars,
            ask_overwrite=False,
        )
        from_file.pack(side=tk.TOP, fill=tk.X, expand=True)

        # Layout: To file
        to_file = FileAndFormat(
            self,
            text="Output format and file name:",
            fmt_list=writers.names(),
            var_prefix="writer",
            vars=self.vars,
            ask_overwrite=True,
        )
        to_file.pack(side=tk.TOP, fill=tk.X, expand=True)

        # Layout: Controls
        control_line = ttk.Frame(self)
        convert = ttk.Button(
            control_line,
            image=self._satellite_icon,
            text="Convert",
            command=self.translate,
            compound=tk.LEFT,
        )
        convert.pack(side=tk.RIGHT, padx=5, pady=5)
        control_line.pack(side=tk.TOP, fill=tk.X, expand=False)

        # Layout: Status frame
        self.status = Status(self)
        self.status.pack(side=tk.TOP, fill=tk.X, expand=False)

    def translate(self):
        # Gather necessary info
        file_from = self.vars["reader_file"].get()
        if not file_from:
            self.status.write("Please choose input file")
            return

        file_to = self.vars["writer_file"].get()
        if not file_to:
            self.status.write("Please choose output file")
            return

        fmt_from = self.vars["reader_fmt"].get()
        if fmt_from == "detect":
            fmt_from = None

        fmt_to = self.vars["writer_fmt"].get()
        if fmt_to == "detect":
            fmt_to = None

        options = dict(overwrite=True)

        # Call translator
        name_from = pathlib.Path(file_from).name
        name_to = pathlib.Path(file_to).name
        self.status.write(f"Converting {name_from} to {name_to}")
        try:
            self.translator(file_from, file_to, fmt_from, fmt_to, options)
        except Exception as err:
            self.status.write(f"The conversion failed:\n  {err}")
        else:
            self.status.write(f"Done. Output stored in {file_to}\n")


class FileAndFormat(ttk.Frame):

    def __init__(self, master, text, fmt_list, var_prefix, vars, ask_overwrite=False):
        super().__init__(master)
        self.vars = vars
        self.ask_overwrite = ask_overwrite

        # Add autodetection of format
        # fmt_list = ("detect", ) + fmt_list

        # Label
        label_line = ttk.Frame(self)
        tk.Label(label_line, text=text).pack(side=tk.LEFT, padx=5, pady=5)
        label_line.pack(side=tk.TOP, fill=tk.X, expand=False)

        # Format Dropdown
        file_line = ttk.Frame(self)
        fmt_var = self.vars[f"{var_prefix}_fmt"] = tk.StringVar()
        fmt_var.set(fmt_list[0])
        fmt_dropdown = ttk.Combobox(
            file_line, width=12, textvariable=fmt_var, values=fmt_list, state="readonly"
        )
        fmt_dropdown.pack(side=tk.LEFT, padx=20)

        # File Chooser
        self.file_var = self.vars[f"{var_prefix}_file"] = tk.StringVar()
        file_entry = tk.Entry(file_line, width=80, textvariable=self.file_var)
        file_entry.pack(side=tk.LEFT, padx=20)
        file_button = ttk.Button(
            file_line,
            image=self.master._stone_icon,
            text="Choose File",
            command=self._choose_file,
            compound=tk.LEFT,
        )
        file_button.pack(side=tk.LEFT, padx=10)
        file_line.pack(side=tk.BOTTOM, expand=False)

    def _choose_file(self):
        if self.ask_overwrite:
            self.file_var.set(filedialog.asksaveasfilename())
        else:
            self.file_var.set(filedialog.askopenfilename())


class Status(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)

        # Lay out widgets
        self._text = scrolledtext.ScrolledText(self, height=8, wrap=tk.WORD)
        self._text.pack(fill=tk.X, expand=False)

        # Initialize widgets
        startup_text = (
            f"Posetta, v{posetta.__version__}, MIT License {posetta.__copyright__}\n"
            f"See {posetta.__url__} for more information\n"
        )
        self._text.insert(1.0, startup_text)
        self._text.config(state=tk.DISABLED)

    def clear(self):
        self._text.config(state=tk.NORMAL)
        self._text.delete(1.0, tk.END)
        self._text.config(state=tk.DISABLED)

    def write(self, text):
        self._text.config(state=tk.NORMAL)
        self._text.insert(
            tk.END, f"\n{text}"
        )  # New-line in front to avoid blank line at end
        self._text.yview(tk.END)  # Move scrollbar to bottom
        self._text.config(state=tk.DISABLED)
