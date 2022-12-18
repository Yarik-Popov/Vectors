from __future__ import annotations
import tkinter as tk
import typing
from tkinter import ttk
import support
from tkinter.messagebox import showinfo


class BooleanButton(ttk.Button):
    def __init__(self, master, *, value=True, name='Button', next_true_message='Yes', next_false_message='No', pad_y=10,
                 pack_button=True, special_command: typing.Callable = None):
        """
        This class creates a button that represents a boolean value. It shows the next message. Meaning if the current
        value is True, it will display next_false_message='No' or if the current value is False, it will display
        next_true_message='Yes'. It always shows what the next value will be on the button.

        :param master: The master object or frame
        :param value: Default value (True)
        :param name: The name of the button
        :param next_true_message: The next message to be displayed when the button is true
        :param next_false_message: The next message to be displayed when the button is false
        :param pad_y: The padding in the y direction
        :param pack_button: Packs the button by default
        """
        if not isinstance(value, bool):
            raise TypeError(f'{type(value) = }. value must be of type bool')

        # Set string variables
        self.text_button_variable = tk.StringVar()
        self.text_output_variable = tk.StringVar()

        # Super and other variables
        super().__init__(master, command=self.run_special_command, textvariable=self.text_button_variable)
        self.value = value
        self.name = name
        self.label = tk.Label(master, textvariable=self.text_output_variable)
        self.special_command = special_command

        # Sets the next message outputs
        self.next_true_message = next_true_message
        self.next_false_message = next_false_message

        # Set the text variables
        self.set_text_button_variable()
        self.set_text_output_variable()

        # Pack if indicated
        if pack_button:
            self.pack(pady=pad_y)

    def run_special_command(self):
        """Runs the special command that was inserted on initialization"""
        if isinstance(self.special_command, typing.Callable):
            self.special_command()
        self.change_value()

    def place(self, row, *, col_label=0, col_self=1, place_label=True):
        """
        Places the button on the master grid.
        :param row: Row where the button and text label is to be placed
        :param col_label: The column to place the label
        :param col_self: The column to place the button
        :param place_label: Places the label on the grid by default
        """
        self.grid(column=col_self, row=row)
        if place_label:
            self.label.grid(column=col_label, row=row)

    def set_text_output_variable(self):
        """Sets the text output to the button repr"""
        self.text_output_variable.set(str(self))

    def set_text_button_variable(self):
        """Sets the text button to the next message"""
        self.text_button_variable.set(self.get_next_message())

    def get_next_message(self):
        """Gets the next message to be used on the button"""
        if self.value:
            return self.next_false_message
        return self.next_true_message

    def get_current_text(self):
        """Gets the current text message"""
        if self.value:
            return self.next_true_message
        return self.next_false_message

    def change_value(self):
        """Changes the value of the button, from on to off and vice versa"""
        if self.value:
            self.value = False
        else:
            self.value = True

        # Sets the text variables to the appropriate output
        self.set_text_button_variable()
        self.set_text_output_variable()

    def __str__(self):
        return f'{self.name}: {self.get_current_text()}'


class PhysicsVariableRow:
    def __init__(self, master, *, text='', values=None, row=0):
        """
        This class handles the getting of the values from the user related to the physics vector variables.

        :param master: Root tk object
        :param text: The text to be displayed in the label
        :param values: The values of the list-boxes
        :param row: The row on which this object will be placed on
        """
        self.label = tk.Label(master, text=text)
        self.float_entry_length = FloatEntry(master)
        self.float_entry_angle = FloatEntry(master)
        self.listbox_cardinal0 = OptionListbox(master, values=values, default=0)
        self.listbox_cardinal1 = OptionListbox(master, values=values, default=1)
        self.row = row

    def place(self):
        """Places this object on the master tk frame at the row indicated on initialization"""
        self.label.grid(row=self.row)
        self.float_entry_length.grid(row=self.row, column=1)
        self.float_entry_angle.grid(row=self.row, column=2)
        self.listbox_cardinal0.grid(row=self.row, column=3)
        self.listbox_cardinal1.grid(row=self.row, column=4)

    def remove(self):
        """Removes the object from the master frame"""
        self.label.grid_forget()
        self.float_entry_length.grid_forget()
        self.float_entry_angle.grid_forget()
        self.listbox_cardinal0.grid_forget()
        self.listbox_cardinal1.grid_forget()

    def get_safe(self) -> support.Vector2D:
        """Gets the information from the object as a Vector2D object"""
        return create_cardinal_angles(self.listbox_cardinal0,
                                      self.listbox_cardinal1,
                                      self.float_entry_length.get_safe(),
                                      self.float_entry_angle.get_safe())

    def get_safe_raw(self):
        """
        Gets the data from the object.

        :return: self.listbox_cardinal0.get_safe(), self.listbox_cardinal1.get_safe(),
               self.float_entry_length.get_safe(), self.float_entry_angle.get_safe()
        """
        return self.listbox_cardinal0.get_safe(), self.listbox_cardinal1.get_safe(), \
               self.float_entry_length.get_safe(), self.float_entry_angle.get_safe()


class TextEntry(ttk.Entry):
    def __init__(self, master, *, default=None, validator: typing.Callable[[str], bool] = None):
        """
        This class handles the getting of data from the user via a text entry box. Also has a label inside the text
        entry object for ease of use.

        :param master: The main ui.
        :param default: The default value used in the self.get_safe() method if the validator fails
        :param validator: The function used to check if the given input from the user is valid and should be used when
        calling the self.get_safe() method. If the validator fails the self.get_safe() reverts to the default value
        specified.
        """

        # Text variables
        self.entry_text_variable = tk.StringVar()
        self.label_text_variable = tk.StringVar()

        # Super and other
        super().__init__(master, textvariable=self.entry_text_variable)
        self.label = ttk.Label(master, textvariable=self.label_text_variable)

        self.validator = validator
        self.default = default
        self.focus()

    def set_label_text(self, text: str):
        """Sets the text of the label"""
        self.label_text_variable.set(text)

    def place(self, row: int, *, col_label=0, col_entry=1, place_label=True):
        """
        This method places the text entry onto the grid

        :param row: The row to be used.
        :param col_label: Column of label
        :param col_entry: Column of the entry
        :param place_label: True means the label will be placed.
        """
        if place_label:
            self.label.grid(row=row, column=col_label)

        self.grid(row=row, column=col_entry)

    def get_safe(self):
        """
        This method gets the input from the user making sure it passes the validator function passed in when the text
        entry is initialized. This is the preferred option of getting from the text entry. Thought, self.get() is
        available.

        :return: self.get() or self.default.
        """

        result = self.get()
        if isinstance(self.validator, typing.Callable) and self.validator(result):
            return result
        return self.default

    def remove(self):
        """Removes the text entry from the frame"""
        self.label.grid_remove()
        self.grid_remove()


class FloatEntry(TextEntry):
    def __init__(self, master, *, default: int | float = 0.0):
        """
        This class handles the getting of data from the user via a text entry box. Also has a label inside the text
        entry object for ease of use. It allows the program to only get floating numbers from the user

        :param master: The main ui.
        :param default: The default value used in the self.get_safe() method if the validator fails
        """
        super().__init__(master, validator=support.is_float, default=default)

    def get_safe(self) -> float | int:
        """
        This method returns the entry of the user if it is a float or the default value. All are converted to float
        """
        result = self.get()
        if self.validator(result):
            return float(result)
        return self.default


class OptionListbox(tk.Listbox):
    def __init__(self, master, *, text='', values=None, default: int = None,
                 command: typing.Callable[[str, int], None] = None):
        """
        This class handles the values and logic behind an option's list-box.

        :param master: Root tk frame object
        :param text: The text to be displayed in the label
        :param values: The values in the list-box
        :param default: The default value to be returned when getting from the user
        :param command: The command to be run when the user selects an element from the list-box
        """
        super().__init__(master, height=len(values), selectmode=tk.SINGLE)
        # Variables
        self.background_color = 'yellow'
        self.label = tk.Label(master, text=text)
        self.default = default
        self.list_values = values
        self.value = None
        self.command = command
        self.text = text

        # Operations done on initialization
        self.bind('<<ListboxSelect>>', lambda _: self.select(_))
        for i in values:
            self.insert(tk.END, i)

        if isinstance(self.default, int):
            self.itemconfig(self.default, background=self.background_color)

    def select(self, _):
        """This method runs when the user selects an element. It updates the value stored in the object related to which
        element was selected."""

        # Gets the selected index from the user and sets all the rows to white
        index = self.curselection()
        for i in range(self.size()):
            self.itemconfig(i, background='white')

        # Makes sure the index exists and then updates the value accordingly
        if not index:
            if self.value is None:
                index = self.default
            else:
                index = self.value
        else:
            self.value = index[0]

        # Shows the user which element they selected and calls the command passing the text and the index
        self.itemconfig(index, background=self.background_color)
        if isinstance(self.command, typing.Callable):
            self.command(self.text, self.get_safe())

    def get_safe(self):
        """Gets the value if it exists or else the default value (index)"""
        if self.value is None:
            return self.default
        return self.value

    def remove(self):
        """Removes the object from the frame"""
        self.grid_remove()
        self.label.grid_remove()

    def place(self, row, *, col_label=0, col_self=1):
        """
        Places the object on the frame based on the row and column values

        :param row: The row on which the object will be placed on
        :param col_label: The column on which the label will be placed on
        :param col_self: The column on which the list-box will be placed on
        """
        self.label.grid(row=row, column=col_label)
        self.grid(row=row, column=col_self)


def create_cardinal_angles(listbox_cardinal0: OptionListbox, listbox_cardinal1: OptionListbox,
                           length: int | float, angle: int | float, *, show_message=True) -> support.Vector2D:
    """
    This function creates a Vector2D object based on the indexes from the list-box objects, length and angle. The
    indexes

    :param listbox_cardinal0: Main OptionListbox object used to generate the main axis
    :param listbox_cardinal1: Second OptionListbox object used to determine to which direction from the main axis the
    vector will point to
    :param length: Length inputted
    :param angle: Angle inputted
    :param show_message: Shows a pop-up message when the user has 2 cardinals equal or opposite
    :return: support.Vector2D() or support.Vector2D(length=length, angle=result_angle)
    """
    # Gets the cardinal indexes from the listbox objects
    cardinal0 = listbox_cardinal0.get_safe()
    cardinal1 = listbox_cardinal1.get_safe()

    # Makes sure that the cardinals aren't equal or opposites
    if cardinal0 % 2 == cardinal1 % 2:
        if show_message:
            showinfo('Error', 'You cannot have 2 cardinals be the same or opposite!')
        return support.Vector2D()

    # Calculate angle based on the cardinals inputted
    result_angle = cardinal0 * 90
    if cardinal0 == 0 and cardinal1 == 3:
        result_angle = 360 - angle
    elif cardinal0 == 3 and cardinal1 == 0:
        result_angle = 270 + angle
    elif cardinal0 > cardinal1:
        result_angle -= angle
    else:
        result_angle += angle
    return support.Vector2D(magnitude=length, angle=result_angle)
