from __future__ import annotations
# Vectors adding and subtracting program
# Learned:
# - Turtle
# - More complex ui
# - Magic math methods for the Vector2D class
# - Typing Callable
# pyinstaller --onefile --noconsole main.py
import tkinter as tk
from tkinter import ttk
import widgets
import support
import equations
from tkinter.messagebox import showinfo

# Constants
TEXT_BUTTON_BACK_TO_MENU = 'Back to Menu'
TEXT_VERSION = 'Version 1.1.0'


class BaseWindow(ttk.Frame):
    def __init__(self, master, title: str, *, rows_num=0, columns_num=0, pad_x=0, pad_y=0):
        """
        Base Window from which all windows in the program inherit from

        :param master: Root tk object
        :param title: Title of window
        :param rows_num: Number of rows. Default is 0
        :param columns_num: Number of columns. Default is 0
        :param pad_x: Padding on the x or rows. Default is 0
        :param pad_y: Padding on the y or columns. Default is 0
        """
        super().__init__(master)
        self.master.title(title)
        ttk.Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 10')
        self.__configure_rows_columns(rows_num=rows_num, columns_num=columns_num, pad_x=pad_x, pad_y=pad_y)

    def init_ui(self):
        """Abstract method that must be called on initialization. This method initialization the ui"""
        ...

    def __configure_rows_columns(self, rows_num=0, columns_num=0, pad_x=0, pad_y=0):
        """
        Creates rows_num number of rows with padding pad_x and columns_num number of columns with padding pad_y. Called
        on initialization of the object.

        :param rows_num: Number of rows
        :param columns_num: Number of columns
        :param pad_x: Padding in the x
        :param pad_y: Padding in the y
        :return:
        """
        for i in range(rows_num):
            self.rowconfigure(i, pad=pad_x)

        for i in range(columns_num):
            self.columnconfigure(i, pad=pad_y)


class MenuWindow(BaseWindow):
    COURSE_MATH = 0
    COURSE_PHYSICS = 1

    def __init__(self, master):
        """
        Menu window. This is the entry to the program. The user selects what option they would like to use.

        :param master: Master tkinter object
        """
        super().__init__(master, 'Menu', rows_num=5, pad_x=20)
        self.info_buttons = ((f"What's new in {TEXT_VERSION}?", self.launch_whats_new),
                             ('Math Vectors', lambda: self.launch_window(MenuWindow.COURSE_MATH)),
                             ('Physics Vectors', lambda: self.launch_window(MenuWindow.COURSE_PHYSICS)),
                             ('Kinematics Problems', self.launch_kinematics)
                             )
        self.info_buttons_length = [len(i[0]) for i in self.info_buttons]
        self.buttons = [ttk.Button(self, text=i[0], command=i[1], width=max(self.info_buttons_length))
                        for i in self.info_buttons]

        # Labels
        self.label_title = tk.Label(self, text='Vectors', font='serif 30')
        self.label_version = tk.Label(self, text=TEXT_VERSION, pady=50)

        # Other
        self.init_ui()

    def init_ui(self):
        # Title label
        self.label_title.grid(row=0, pady=50)

        # Buttons
        for i, val in enumerate(self.buttons):
            val.grid(row=i+1)

        # Label version
        self.label_version.grid(row=5)
        self.pack()

    def launch_window(self, course):
        """
        Launches the math or physics vector window depending on the parameter.

        :param course: COURSE_MATH = 0 or COURSE_PHYSICS = 1
        """
        VectorsWindow(self.master, course)
        self.destroy()

    def launch_kinematics(self):
        """Launches the kinematics window"""
        KinematicsWindow(self.master)
        self.destroy()

    def launch_whats_new(self):
        WhatsNewWindow(self.master)
        self.destroy()


class WhatsNewWindow(BaseWindow):
    def __init__(self, master):
        """
        Creates a window explaining what is new in the latest version of the Vectors program.

        :param master: Master tkinter object
        """
        super().__init__(master, "What's new?", rows_num=3, pad_x=20)
        self.label_version_info = tk.Label(self, text=f"What's new in {TEXT_VERSION}?", font='serif 20')
        self.label_info = tk.Label(self, text='''
- Added the "What's new" button and window explaining the new features
- Added the kinematics problem solve feature
        ''', justify=tk.LEFT, font='serif 12')
        self.button_back = ttk.Button(self, text=TEXT_BUTTON_BACK_TO_MENU, command=self.back_to_menu)
        self.init_ui()

    def init_ui(self):
        self.label_version_info.grid(row=0)
        self.label_info.grid(row=1)
        self.button_back.grid(row=2)
        self.pack()

    def back_to_menu(self):
        """Returns to the menu"""
        MenuWindow(self.master)
        self.destroy()


class VectorsWindow(BaseWindow):
    DEFAULT_CARDINAL0 = 0
    DEFAULT_CARDINAL1 = 1
    PHYSICS_CARDINALS = ['East', 'North', 'West', 'South']

    def __init__(self, master, course):
        """
        Main window for the addition and subtraction of vectors

        :param master: Root tkinter object
        :param course: The course (math or physics)
        """
        super().__init__(master, 'Vector', rows_num=10, pad_x=20, columns_num=4, pad_y=20)
        # Buttons
        self.button_vector_type = widgets.BooleanButton(self, name='Vector Type', next_true_message='Algebraic',
                                                        next_false_message='Geometric', pack_button=False,
                                                        special_command=self.change_type)
        self.button_generate = ttk.Button(self, text="Generate", command=self.generate_vectors)
        self.button_add = ttk.Button(self, text='Add', command=self.add_vector)
        self.button_subtract = ttk.Button(self, text='Subtract', command=self.subtract_vector)
        self.button_back = ttk.Button(self, text=TEXT_BUTTON_BACK_TO_MENU, command=self.back_to_courses)

        # Text entry
        self.entry_x_length = widgets.TextEntry(self, default=0, validator=support.is_float)
        self.entry_x_length.set_label_text('X Distance:')
        self.entry_y_angle = widgets.TextEntry(self, default=0, validator=support.is_float)
        self.entry_y_angle.set_label_text('Y Distance:')
        self.entry_multiplier = widgets.TextEntry(self, default=1, validator=support.is_float)
        self.entry_multiplier.set_label_text('Multiplier: ')

        # Result label
        self.label_result = ttk.Label(self, text='Result Vector: ')
        self.text_variable_vector = tk.StringVar()
        self.text_variable_vector.set('Result Vector will appear here')
        self.label_vector = ttk.Label(self, textvariable=self.text_variable_vector)

        # Scroll bar and listbox
        self.display = tk.Listbox(self, width=100, height=10)
        # self.scrollbar = ttk.Scrollbar(self.display, orient='vertical')
        self.scrollbar = ttk.Scrollbar(self.display)
        self.display.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.display.yview)

        # Physics cardinal directions
        self.listbox_cardinal0 = widgets.OptionListbox(self, text='Initial Direction: ',
                                                       values=VectorsWindow.PHYSICS_CARDINALS,
                                                       default=VectorsWindow.DEFAULT_CARDINAL0)
        self.listbox_cardinal1 = widgets.OptionListbox(self, text='Vector Towards: ',
                                                       values=VectorsWindow.PHYSICS_CARDINALS,
                                                       default=VectorsWindow.DEFAULT_CARDINAL1)

        # Other variables and methods
        self.vectors = []
        self.course = course
        self.clear_vectors = False

        # Launch gui
        self.init_ui()

    def init_ui(self):
        # First (0th) row and second row
        self.button_vector_type.place(0, col_label=1, col_self=2)
        self.entry_x_length.place(1)
        self.entry_y_angle.place(1, col_label=2, col_entry=3)

        # Third row and fourth row
        self.entry_multiplier.place(2, col_label=1, col_entry=2)

        # Operation buttons
        self.button_add.grid(row=4, column=1)
        self.button_subtract.grid(row=4, column=2)

        # Fifth + sixth rows
        self.display.grid(row=5, columnspan=4)
        self.button_generate.grid(row=6, column=1, columnspan=2)

        # 7th and 8th rows and pack ui
        self.label_result.grid(row=7, column=1, columnspan=2)
        self.label_vector.grid(row=8, column=1, columnspan=2)
        self.button_back.grid(row=9, columnspan=2, column=1, pady=50)

        # Other
        self.pack()

    def place_physics_cardinals(self):
        """Places the physics cardinals on the screen"""
        self.listbox_cardinal0.place(3)
        self.listbox_cardinal1.place(3, col_label=2, col_self=3)

    def remove_physics_cardinals(self):
        """Removes the physics cardinals from the screen"""
        self.listbox_cardinal0.remove()
        self.listbox_cardinal1.remove()

    def back_to_courses(self):
        """Brings the user back to the course selection menu"""
        MenuWindow(self.master)
        self.destroy()

    def pull_input_data(self):
        """
        Gets the input from the users. Creates a vector and returns it. This is called by the add_vectors() method.
        """

        # Gets the x or length and y or angle from user
        x_length = float(self.entry_x_length.get_safe())
        y_angle = float(self.entry_y_angle.get_safe())

        # Returns the appropriate vector based on the type of vector needed
        if self.button_vector_type.value:
            return support.Vector2D(x_length, y_angle)

        # Creates a vector based on the cardinal directions if in physics mode
        if self.course == MenuWindow.COURSE_PHYSICS:
            return widgets.create_cardinal_angles(self.listbox_cardinal0, self.listbox_cardinal1, x_length, y_angle)
        return support.Vector2D(magnitude=x_length, angle=y_angle)

    def add_vector(self, _multiplier=1):
        """
        Adds the vectors to the list and listbox of vectors.

        :param _multiplier: This parameter is used internally and should not be modified. Probably is not the best way
        of doing this. This is adjusted to add or subtract the vectors from the list of vectors.
        """
        # Get vector and multiplier from user and adjust vector
        vector = self.pull_input_data()
        vector *= _multiplier * float(self.entry_multiplier.get_safe())

        # Make sure that the vector created is not a 0 vector
        if vector:
            # Delete past data
            if self.clear_vectors:
                self.vectors = []
                self.display.delete(0, tk.END)
                self.clear_vectors = False

            # Add vector to the list and listbox
            self.display.insert(tk.END, vector)
            self.vectors.append(vector)

            # Remove the 2 last vector from listbox and list if they are opposites
            if len(self.vectors) > 1 and vector.is_opposite(self.vectors[-2]):
                self.display.delete(len(self.vectors) - 2, tk.END)
                self.vectors = self.vectors[:-2]

    def subtract_vector(self):
        """
        Subtracts or makes the vectors negative and adds it to the list and listbox by calling add_vectors() and passing
        in a negative multiplier
        """
        self.add_vector(_multiplier=-1)

    def change_type(self):
        """Changes the type of vector input"""
        if not self.button_vector_type.value:
            self.entry_x_length.set_label_text('X Distance:')
            self.entry_y_angle.set_label_text('Y Distance:')
            self.remove_physics_cardinals()
        else:
            self.entry_x_length.set_label_text('Length: ')
            self.entry_y_angle.set_label_text('Angle:')
            if self.course == MenuWindow.COURSE_PHYSICS:
                self.place_physics_cardinals()

    def generate_vectors(self):
        """
        Generates the vectors that the user added. Scales the vectors so that they are not too small or too big.
        """
        vector_result = support.draw_vectors(self.vectors)
        if vector_result is not None:
            self.text_variable_vector.set(str(vector_result))
            self.clear_vectors = True


class KinematicsWindow(BaseWindow):
    PHYSICS_VARIABLES = ['Initial Velocity (Vi)', 'Final Velocity (Vf)', 'Acceleration (A)', 'Displacement (d)',
                         'Time (t)']
    OPTIONS = ['Variable: ', 'Length: ', 'Angle: ', 'Starting: ', 'Ending: ']
    CARDINAL_TEXT = ['Required Variable: ', 'Not Used Variable: ']

    def __init__(self, master):
        """
        Creates the window for the user to use kinematics variables and equations

        :param master: Master tkinter object
        """
        super().__init__(master, 'Kinematics', columns_num=4, pad_y=20, rows_num=10, pad_x=20)
        # Cardinals and physics variable list
        self.physics_variables = []
        self.cardinal_required = widgets.OptionListbox(self,
                                                       text=KinematicsWindow.CARDINAL_TEXT[0],
                                                       values=KinematicsWindow.PHYSICS_VARIABLES,
                                                       command=self.remove_not_used)
        self.cardinal_not_used = widgets.OptionListbox(self,
                                                       text=KinematicsWindow.CARDINAL_TEXT[1],
                                                       values=KinematicsWindow.PHYSICS_VARIABLES,
                                                       command=self.remove_not_used)
        self.index_required = None
        self.index_not_used = None

        # Physics variable entries
        for i in range(len(KinematicsWindow.PHYSICS_VARIABLES) - 1):
            self.physics_variables.append(widgets.PhysicsVariableRow(self,
                                                                     text=f'{KinematicsWindow.PHYSICS_VARIABLES[i]}:',
                                                                     values=VectorsWindow.PHYSICS_CARDINALS,
                                                                     row=i + 2))

        # Buttons
        self.button_solve_problem = tk.Button(self, text='Solve Problem', command=self.solve_problem)
        self.button_back_to_courses = tk.Button(self, text=TEXT_BUTTON_BACK_TO_MENU, command=self.back_to_courses)

        # Time text entry and launch gui
        self.float_entry_time = widgets.FloatEntry(self)
        self.float_entry_time.set_label_text(f'{KinematicsWindow.PHYSICS_VARIABLES[-1]}:')

        # Label equation
        self.text_variable_equation = tk.StringVar()
        self.label_equation = tk.Label(self, textvariable=self.text_variable_equation)

        # Label result
        self.text_variable_result = tk.StringVar()
        self.label_result = tk.Label(self, textvariable=self.text_variable_result)

        # Other variables and initialize ui
        self.calculator_functions = (self.calculate_initial_velocity,
                                     self.calculate_final_velocity,
                                     self.calculate_acceleration,
                                     self.calculate_displacement,
                                     self.calculate_time)
        self.init_ui()

    def init_ui(self):
        # Cardinals for the required and not used variables
        self.cardinal_required.place(0)
        self.cardinal_not_used.place(0, col_label=2, col_self=3)

        # Menu
        for i, val in enumerate(KinematicsWindow.OPTIONS):
            tk.Label(self, text=val).grid(row=1, column=i)

        # Variables
        for i in self.physics_variables:
            i.place()

        # Time and pack
        self.float_entry_time.place(6, col_label=1, col_entry=2)
        self.button_solve_problem.grid(row=7, column=2)
        self.label_equation.grid(row=8, column=2)
        self.label_result.grid(row=9, columnspan=5)
        self.button_back_to_courses.grid(row=10, column=2, pady=20)
        self.pack()

    def remove_not_used(self, text, index):
        """
        This method removes the physics variable that is not used from the view

        :param text: Text of physics variable
        :param index: The index
        """
        # Places the hidden row
        if text == KinematicsWindow.CARDINAL_TEXT[0]:
            self.place_time_or_other(self.index_required)
            self.index_required = index
        elif text == KinematicsWindow.CARDINAL_TEXT[1]:
            self.place_time_or_other(self.index_not_used)
            self.index_not_used = index

        # Removes the appropriate row
        if index == len(KinematicsWindow.OPTIONS) - 1:
            self.float_entry_time.remove()
        else:
            self.physics_variables[index].remove()

        # Modifies the equation shown or displays a warning message
        if self.index_required is not None and self.index_not_used is not None:
            if self.index_required == self.index_not_used:
                showinfo('Warning', 'You cannot have the same variables for both the Required and Not Used sections')
            elif self.index_required < self.index_not_used:
                self.text_variable_equation.set(equations.EQUATIONS[self.index_required][self.index_not_used - 1])
            else:
                self.text_variable_equation.set(equations.EQUATIONS[self.index_required][self.index_not_used])

    def place_time_or_other(self, index):
        """
        Places the time or other physics variable made on the index.

        :param index:
        """
        if index == len(KinematicsWindow.OPTIONS) - 1:
            self.float_entry_time.place(6)
        elif index is not None:
            self.physics_variables[index].place()

    def solve_problem(self):
        """Solves the problem"""
        # Makes sure that both the required and not used variables exist
        if self.index_required is None:
            showinfo('Warning', 'Must select a required variable to solve problem')
            return
        if self.index_not_used is None:
            showinfo('Warning', 'Must select a not used variable to solve problem')
            return

        # Solves the problem
        self.text_variable_result.set(f'''Result: 
{self.calculator_functions[self.index_required]([i.get_safe() for i in self.physics_variables],
                                                self.float_entry_time.get_safe())}''')

    def back_to_courses(self):
        """Brings the user back to the course selection menu"""
        MenuWindow(self.master)
        self.destroy()

    def calculate_initial_velocity(self, values, time):
        """
        Calculates the initial velocity

        :param values: The values found in the physics variables
        :param time: Time
        :return: Initial velocity as Vector2D object or ''
        """
        if self.index_not_used == 1:
            return equations.calculate_vi_no_vf(values[2], values[3], time)
        elif self.index_not_used == 2:
            return equations.calculate_vi_no_a(values[1], values[3], time)
        elif self.index_not_used == 3:
            return equations.calculate_vi_no_d(values[1], values[2], time)
        elif self.index_not_used == 4:
            return f'Magnitude: {equations.calculate_vi_no_t(*values[1:])}'
        return ''

    def calculate_final_velocity(self, values, time):
        """
        Calculates the final velocity

        :param values: The values found in the physics variables
        :param time: Time of object in motion
        :return: Initial final as Vector2D object or ''
        """
        if self.index_not_used == 0:
            return equations.calculate_vf_no_vi(*values[2:], time)
        elif self.index_not_used == 2:
            return equations.calculate_vf_no_a(values[0], values[3], time)
        elif self.index_not_used == 3:
            return equations.calculate_vf_no_d(values[0], values[2], time)
        elif self.index_not_used == 4:
            return f'Magnitude: {equations.calculate_vf_no_t(values[0], *values[2:])}'
        return ''

    def calculate_acceleration(self, values, time):
        """
        Calculates the acceleration

        :param values: The values found in the physics variables
        :param time: Time of object in motion
        :return: Acceleration as Vector2D object or ''
        """
        if self.index_not_used == 0:
            return equations.calculate_a_no_vi(values[1], values[3], time)
        elif self.index_not_used == 1:
            return equations.calculate_a_no_vf(values[0], values[3], time)
        elif self.index_not_used == 3:
            return equations.calculate_a_no_d(*values[0:2], time)
        elif self.index_not_used == 4:
            return equations.calculate_a_no_t(*values[:2], values[3])
        return ''

    def calculate_displacement(self, values, time):
        """
        Calculates the displacement

        :param values: The values found in the physics variables
        :param time: Time of object in motion
        :return: Displacement as Vector2D object or ''
        """
        if self.index_not_used == 0:
            return equations.calculate_d_no_vi(*values[1:3], time)
        elif self.index_not_used == 1:
            return equations.calculate_d_no_vf(values[0], values[2], time)
        elif self.index_not_used == 2:
            return equations.calculate_d_no_a(*values[:2], time)
        elif self.index_not_used == 4:
            return equations.calculate_d_no_t(*values[:3])
        return ''

    def calculate_time(self, values, _):
        """
        Calculates the time

        :param values: The values found in the physics variables
        :param _: Would be time but since this method calculates for it, it is ignored
        :return: Time as float or tuple of floats or 'No Solution'
        """
        values_raw = [i.get_safe_raw()[2] for i in self.physics_variables]
        result = None
        if self.index_not_used == 0:
            result = equations.calculate_t_no_vi(*values_raw[1:])
        elif self.index_not_used == 1:
            result = equations.calculate_t_no_vf(values_raw[0], *values_raw[2:])
        elif self.index_not_used == 2:
            result = equations.calculate_t_no_a(*values[:2], values[3])
        elif self.index_not_used == 3:
            result = equations.calculate_t_no_d(*values[:3])

        if result is None or (isinstance(result, tuple) and not len(result)):
            return 'No Solution'
        return result


def main():
    root = tk.Tk()
    root.state('zoomed')
    MenuWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
