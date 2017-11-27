"""
Author: Nicholas Neill
Date: 11/25/2017
Interpreter: 3.6.3
IDE: PyCharm
Description: Maintains a fully-featured library of Regular Expressions
Version: EXLIB 0.9.1
"""
import os
import time
import xml.etree.cElementTree as et
import sys
import re
ex = None  # Creates global variable so our Library path need only be defined once.


def clear(wait=0, close=0):
    """
        Clears console to simplify user experience as well as perform simple task as prompted by arg

       the default action (with no args) is to immediately clear console and resume program

        Parameters
        ----------
        wait : int(seconds)
            uses builtin time method to allow users to read output before clearing screen
        close : int
            defines what to do before, during and after clearing console
    """
    # optional parameter to allow a message some time to be read before clearing console.
    time.sleep(wait)
    # statement to issue os command to proper OS
    if close == 0:  # Used in exceptions, Continues from the  EX point.
        if os.name == "nt":  # Handle Windows NT consoles
            os.system("cls")
        else:  # should work for *NIX OS's
            os.system("clear")
    elif close == 1:  # restarts the application.
        if os.name == "nt":  # Handle Windows NT consoles
            os.system("cls")
        else:  # should work for *NIX OS's
            os.system("clear")
        main_menu()
    elif close == 2:  # quits the application.
        quit()


def select_lib():
    # Accept input to select library location:
    change_xml = input("Use Default Library? \n 1. Yes\n 2. No \n Choose:")
    # loop selection process:
    global ex
    while True:
        try:    # add method for Excepting incorrect library paths, and non existing libraries:
            if change_xml == "2":  # Custom library location
                file_path = input("Enter Library Location: ")
                if not os.path.exists(file_path):  # test user input for validity using builtin function
                    raise ValueError("Library Not Found!")  # raise exception from incorrect input
                else:
                    ex = Expression(None, file_path)  # intiates the class Expression with the file_path argument
                    main_menu()  # passes the Expression instance to main_menu()
                    break  # Breaks loop now that selection of library is complete
            elif change_xml == "1":  # Default library location which is stored in the Expression class
                ex = Expression()  # Library is located at %cd%\data\EXLIB.xml
                main_menu()  # Passes Expression instance with default library to main_menu()
                clear(0, 0)
                break  # Breaks loop now that selection of library is complete
            else:  # input was incorrect and is now Excepted
                clear(wait=0, close=0)
                raise ValueError("Invalid Selection!")

        except ValueError as e:  # expcepts error's raised ValueErrors and restarts the selection
            print(e, "Try again!")
            clear(wait=0, close=1)


def main_menu():  # List Library commands
    print("Welcome to Expression Library Choose from the following options:")
    selection = input("1. Read - - - - - - - - - - : Read item(s) in EXLIB\n"
                      "2. New  - - - - - - - - - - : Adds new entry to EXLIB\n"
                      "3. Edit - - - - - - - - - - : Edits an existing entry in EXLIB\n"
                      "4. Delete - - - - - - - - - : Deletes an entry in EXLIB\n"
                      "SELECTION: ")
    try:  # process valid menu selections or except erroneous selections
        if selection == '1':
            re_menu()
        elif selection == '2':
            re_menu2()
        elif selection == '3':
            re_menu3()
        elif selection == "4":
            re_menu4()
        else:
            raise ValueError("Invalid Selection")
    except ValueError as e:
        print(e, "Try again please!")
        clear(2, 1)


def re_menu():
    library = 0
    print("Select All for to read all Expressions.")
    for item in ex.lib_list():
        library += 1
        print("{}. {}".format(library, item))
    re_select = input("Name of REGEX: ")

    if re_select == 'all':
        for item in ex.lib_list():
            print(ex.lib_read(item))
    else:
        print(ex.lib_read(re_select))
    time.sleep(4)
    main_menu()


def re_menu2():
    r = input('Input Regular Expression: ')
    n = input('Name of new expression: ')
    m = input('What does the expression match: ')
    d = input('Description of %s: ' % n)
    ex.lib_write(n, m, d, r)
    time.sleep(5)
    main_menu()


def re_menu3():
    print("Select Expression to modify: ")
    print(ex.lib_list())
    ex_name = input("Selection: ")
    ex_key = input("Select Value to change:\n match \n regex \n description \n Selection:")
    ex_val = input('Change Value: ')
    ex.lib_edit(ex_name, ex_key, ex_val)
    time.sleep(5)
    main_menu()


def re_menu4():
    library = 0
    for item in ex.lib_list():
        library += 1
        print("{}. {}".format(library, item))
    re_select = input("Name of REGEX: ")
    print(ex.lib_delete(re_select))
    main_menu()


class Expression(object):
    """
    Creates the Expression object with in the XML library.

    Parsing the XML Library using ElementTree, The Expression object can be Read, Written, Edited and Deleted.

    Defines:

    lib_read() : reads Expression in Library.
    lib_list() : list all Expression in Library useful for enumerating menus.
    lib_write() : Writes a new Expression to the Library.
    lib_edit() : Edits existing Expression in Library.
    lib_delete() : Deletes Expression from Library.


    """

    def __init__(self, data_file=os.path.join(os.getcwd(), 'EXLIB.xml')):
        """
           Initiates Expression object and defines Library to use.


           Parameters
           ----------
           data_file : str
               Default value is %cd%\EXLIB.xml

        """
        self.name = []
        self.data_file = data_file
        self.xmld = et.parse(data_file)
        self.root = self.xmld.getroot()

    def lib_read(self, r_name, generate=False):
        """
        Uses ElementTree to parse XML Library for r_name

        Because lib_read() parses the XML Library in a For-Loop, 'if;' logic will return False until value is found
        it became necessary to use a sentinel value (r_sentinel) to allow ElementTree to parse the entire library
        before raising a ValueError

        Parameters
        ----------
        r_name : str
           String to search library for
        generate : bool
            False by default, Does not Compile Regular Expression
            If true Returns a Compiled regular expression.

        Returns
        -------
        str
           match, description and expression in formatted string.

        """
        r_sentinel = False
        match = ''
        regex = ''
        desc = ''
        if not generate:
            try:
                for child in self.root:
                    if child.tag == "expression":
                        for attr in child:
                            if child.get('name') == r_name:
                                r_sentinel = True
                                if attr.tag == 'match':
                                    match = attr.text
                                if attr.tag == 'description':
                                    desc = attr.text
                                if attr.tag == 'regex':
                                    regex = attr.text
                if r_sentinel:
                    return "{}: [{}]-----('{}')".format(match, desc, regex)

                else:
                    raise ValueError("Expression not found!")
            except ValueError as e:
                print(e, "Try Again")
                clear(1,0)
        if generate:
            try:
                for child in self.root:
                    if child.tag == "expression":
                        for attr in child:
                            if child.get('name') == r_name:
                                r_sentinel = True
                                if attr.tag == 'match':
                                    match = attr.text
                                if attr.tag == 'description':
                                    desc = attr.text
                                if attr.tag == 'regex':
                                    regex = attr.text
                if r_sentinel:
                    r_expression = re.compile(regex)
                    return r_expression

                else:
                    raise ValueError("Expression not found!")
            except ValueError as e:
                return e

    def lib_list(self):
        """
        Appends all expressions from the XML Library to a list.

        Parses attribute 'name' within 'expression' Elements to a list object.

        Returns
        -------
        list
           List which contains all Expression within the XML Library

        """
        lib_list = []
        for child in self.root:
            if child.tag == 'expression':
                lib_list.append(child.get('name'))
        return lib_list

    def lib_write(self, w_name, w_match, w_description, w_regex):
        """
        Writes a full expression to the XML Library.

        Using user input adds the Element and SubElement with Attributes to XML Library

        Parameters
        ----------
        w_name : str
            Name of expression to be writen to XML Library.
        w_match : str
            Match value of expression to be writen to XML Library.
        w_description : str
            Description of expression to be writen to XML Library.
        w_regex : str
            Regular Expression to be writen to XML Library.

        Returns
        -------
        str
           Formatted confirming Expression was written to library.

        """
        temp_root = et.SubElement(self.root, "expression", name=w_name)
        for child in self.root:
            if child.tag == "expression":
                if child.get('name') == w_name:
                    et.SubElement(temp_root, "match").text = w_match
                    et.SubElement(temp_root, "description").text = w_description
                    et.SubElement(temp_root, "regex").text = w_regex

        tree = et.ElementTree(self.root)
        tree.write(self.data_file)

        return print("The expression ({}) has been written to the Library!".format(self.lib_read(w_name)))

    def lib_edit(self, e_name, e_key, e_val):
        """
        Edits an attribute of an expression.

        Using user input EDITS a single Element and SubElement within XML Library

        Parameters
        ----------
        e_name : str
           Name of expression to be edited in XML Library.
        e_key : str
           SubElement of expression to be to be edited in XML Library.
        e_val : str
           Value of SubElement to be edited in XML Library.

        Returns
        -------
        str
          Formatted with origin value and edited value.

        """
        origin = self.lib_read(e_name)
        temp_root = et.SubElement(self.root, "expression", name=e_name)
        for child in self.root:
            if child.tag == "expression":
                if child.get('name') == e_name:
                    et.SubElement(temp_root, e_key).text = e_val
        tree = et.ElementTree(self.root)
        tree.write(self.data_file)
        return print("The expression: {} Was changed to: \n{}".format(origin, self.lib_read(e_name)))

    def lib_delete(self, d_name):
        """
        Writes a full expression to the XML Library.

        Using user input adds the Element and SubElement with Attributes to XML Library

        Parameters
        ----------
        d_name : str
           Name of expression to be removed from XML Library.

        Returns
        -------
        str
          Formatted confirming Expression was REMOVED from library.

        """
        for child in self.root:
            if child.tag == "expression":
                if child.get('name') == d_name:
                    self.root.remove(child)
                    tree = et.ElementTree(self.root)
                    tree.write(self.data_file)
        return print(d_name, " has been removed from library!")


def main():
    select_lib()


main()
