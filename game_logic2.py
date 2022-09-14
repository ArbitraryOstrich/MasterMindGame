import random
from prettytable import PrettyTable
import MM_tests

colours = ["Red", "Blue", "Green", "Yellow", "Brown", "Orange", "White", "Black"]

colour_pool = []

## this is not the number of dup sets, but the multiple of element in a set
# multiples_of_element = 2


class single_element(object):
    """
    This is a single colour in the mastermind line
    """

    def __init__(self, colour):
        super(single_element, self).__init__()
        self.colour = colour

    def getColour(self):
        return self.colour


class model(object):
    """
    The Games base level, stores element_list, colour_pool and guess_list

    Model exists as a dict containing multiple of the subclass single_element
    required inputs are 3 ints and a bool:
    number_of_elements, number_of_colours, multiples_of_element, allow_Emptys
    populates a colour_pool using multiples_of_element, number_of_colours and allow_Emptys
    then pops from the pool as it makes random choices allowing us to meet constraints
    regenerates the colour_pool after choice is made
    """

    def __init__(
        self, number_of_elements, number_of_colours, multiples_of_element, allow_Emptys
    ):
        super(model, self).__init__()
        self.number_of_colours = number_of_colours
        self.number_of_elements = number_of_elements
        self.multiples_of_element = multiples_of_element
        self.allow_Emptys = allow_Emptys
        self.element_list = {}
        self.colour_pool = []
        self.guess_list = [[], []]

    def return_colour_pool(self):
        list = []
        for a in range(0, self.number_of_colours):
            list.append(colours[a])
        if self.allow_Emptys:
            list.append("Empty")
        return list

    def return_guess_list(self):
        return self.guess_list

    def return_line(self):
        line = []
        for a in range(0, self.number_of_elements):
            line.append(self.element_list[a].getColour())
        return line

    def gen_colour_pool(self):
        """ """
        self.colour_pool = []
        for a in range(0, self.number_of_colours):
            if self.multiples_of_element == 1:
                self.colour_pool.append(colours[a])
            else:
                for b in range(0, self.multiples_of_element):
                    self.colour_pool.append(colours[a])

        if self.allow_Emptys:
            self.colour_pool.append("Empty")

    def choose_colours(self):
        """
        generates a colour_pool using self.gen_colour_pool() and populates it using
        multiples_of_element and number_of_elements then pops from the pool as selected
        """
        self.element_list = {}
        self.gen_colour_pool()

        for a in range(0, self.number_of_elements):
            temp_number = random.choice(range(0, len(self.colour_pool)))
            choice = self.colour_pool[temp_number]
            # Eat up the colour pool as I go
            self.colour_pool.pop(temp_number)
            ## Set chance of empty
            ## Should be 20% but its closer to 13%
            if choice == "Empty":
                if random.uniform(0, 1) * 10 <= 8:
                    temp_number = random.choice(range(0, len(self.colour_pool)))
                    choice = self.colour_pool[temp_number]
                    self.colour_pool.pop(temp_number)

            self.element_list[a] = single_element(choice)

        self.gen_colour_pool()


class controler(object):
    def __init__(
        self, number_of_elements, number_of_colours, multiples_of_element, allow_Emptys
    ):
        super(controler, self).__init__()
        self.model = model(
            number_of_elements, number_of_colours, multiples_of_element, allow_Emptys
        )

    def start_board(self):
        self.model.choose_colours()
        return True

    def numeric_conversion(self, guess):
        """
        Converts numeric str answer into list of colours
        """
        stringified_list = []
        for number in guess:
            number = int(number)
            ## Check if number is in bounds of colours
            if len(self.model.return_colour_pool()) > number:
                stringified_list.append(self.model.return_colour_pool()[number])
            else:
                return False, number
        return stringified_list

    ## This feels like it should be in viewer and not controler as it returns error messages?
    def validate_guess(self, guess):
        """
        returns true if guess passes various sanity checks.
        if false returns an array [False, "error message"]
        Note numeric_conversion checks if number is in bounds of colours
        """
        ### Mutate guess into list of colours if its digits
        if type(guess) is str and guess.isdigit():
            converted_guess = self.numeric_conversion(guess)
            if not converted_guess[0]:
                error = f"{converted_guess[1]} is greater then the possible selection"
                return [False, error]
            else:
                guess = converted_guess
        # ### Check its a list (shouldnt be needed as no but me is playing as text)
        if type(guess) is not list:
            error = f"Your Guess must be passed as a list."
            return [False, error]
        ### Check for multiple Emptys
        if guess.count("Empty") > 1:
            error = f"Only one Empty is allowed at a time."
            return [False, error]
        ### Check for correct number of elements
        if len(guess) != self.model.number_of_elements:
            error = f"Your guess needs to be {self.model.number_of_elements} long."
            return [False, error]
        ### Checks on each input
        for element in guess:
            ### Actually in colour list
            if element not in self.model.colour_pool:
                error = f"{element} is not in the list of possible colours."
                return [False, error]
            ### Higher number of dupes then allowed
            if guess.count(element) > self.model.multiples_of_element:
                error = f"Only allowed {self.model.multiples_of_element} of any given element. {element} has {guess.count(element)}"
                return [False, error]
            ### Emptys
            if not self.model.allow_Emptys and element == "Empty":
                error = f"Emptys are set to not be allowed."
                return [False, error]

        return [True, guess]

    def check_guess(self, guess):
        """
        validates guess
        find black pegs replacing that element of our guess
        find white pegs also replacing
        Sort the Peglist to obscure position info
        valid returns a list of peglist and guess
        invalid returns list of False, the guess and an error
        """
        validated = self.validate_guess(guess)
        if not guess or not validated[0]:
            print("Started at the bottom now im here")
            return [False, guess, validated[1]]
        else:
            guess = validated[1]
            temp_model = self.model.return_line()
            peg_list = []
            # check for black pegs
            for current_index in range(0, self.model.number_of_elements):
                if guess[current_index] == temp_model[current_index]:
                    temp_model[current_index] = "replaced"
                    peg_list.append("Black")
                # check for white pegs
                else:
                    # If not a black peg
                    if guess[current_index] is not temp_model[current_index]:
                        # but it is a white peg
                        if guess[current_index] in temp_model:
                            # find it it in list
                            for a in range(0, self.model.number_of_elements):
                                if temp_model[a] is guess[current_index]:
                                    # Replace first found instance
                                    temp_model[a] = "replaced"
                                    break
                            peg_list.append("White")

            while len(peg_list) != self.model.number_of_elements:
                peg_list.append("Empty")
            ## obfuscate positional info from peglist
            # peg_list = sorted(peg_list)
            self.model.guess_list[0].append(guess)
            self.model.guess_list[1].append(peg_list)
            return [peg_list, guess]


class viewer(object):
    def __init__(
        self,
        number_of_colours=4,
        number_of_elements=6,
        multiples_of_element=2,
        allow_Emptys=False,
    ):
        super(viewer, self).__init__()
        ###### Controler
        self.controler = controler(
            number_of_elements, number_of_colours, multiples_of_element, allow_Emptys
        )
        self.controler.start_board()
        ## Guesses
        self.table1 = PrettyTable()
        self.table1.field_names = range(
            1, (self.controler.model.number_of_elements) + 1
        )
        ## Responses
        self.table2 = PrettyTable()
        self.table2.field_names = range(
            1, (self.controler.model.number_of_elements) + 1
        )
        ## Guess vs Response
        self.table3 = PrettyTable()
        self.table3.field_names = ["Guess", "Response"]

        ## Full table
        self.table4 = PrettyTable()
        self.table4.field_names = ["Hidden answer"]

        ## Should be better way to do this but this check is dependent on number_of_elements
        self.correct_response = []
        for number in range(0, self.controler.model.number_of_elements):
            self.correct_response.append("Black")

    def show_game(self):
        while True:
            print(self.controler.model.return_line())
            print(self.table4)

            print("Your possible choices are")
            colour_pool = self.controler.model.return_colour_pool()
            for a in range(0, len(colour_pool)):
                print(f"{a}: {colour_pool[a]}")
                # print(f"{a}: {colour_pool[a]}", end=" ")
            print("\n")
            answer = input("Input list of numbers corasponding to the colours:")

            response = self.controler.check_guess(str(answer))

            if not response[0]:
                print("\x1bc")
                print(response[2])
                continue
            else:
                self.response = response[0]
                self.stringified_answer = response[1]

            print(self.response, "\n")

            self.table3 = PrettyTable()
            self.table3.field_names = ["Guess", "Response"]
            self.table4 = PrettyTable()
            self.table4.field_names = ["Hidden answer"]

            self.table1.add_row(self.stringified_answer)
            self.table2.add_row(self.response)

            self.table3.add_row([self.table1, self.table2])
            self.table4.add_row([self.table3])
            print("\x1bc")

            if self.response == self.correct_response:
                print("You won congrats!")
                print("Your guess list was:")
                self.table4.field_names = [str(self.controler.model.return_line())]
                print(self.table4)
                break


if __name__ == "__main__":

    vwr = viewer(
        number_of_colours=8,
        number_of_elements=4,
        multiples_of_element=2,
        allow_Emptys=True,
    )
    vwr.show_game()
