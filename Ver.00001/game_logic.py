import random
from prettytable import PrettyTable

colours = ["Red", "Blue", "Green", "Yellow", "Brown", "Orange", "White", "Black"]
colour_pool = []
allow_blanks = True
## this is not the number of dup sets, but the multiple of a given element in a set
number_of_dupes = 2

#### SOMETHING IS BROKEN WITH ask_user
### checks in the class do not work
### checks return false abut keep going forward


#
# test_guess = ['Red',  'Blue', 'Green', 'Yellow', 'Brown', 'Orange']
# test_guess = ['White', 'Black', 'Green', 'Orange', 'Blue', 'Yellow']
#
class single_element(object):
    """This is a single colour in the mastermind line"""

    def __init__(self, colour):
        super(single_element, self).__init__()
        self.colour = colour

    def getColour(self):
        return self.colour


class answer_line(object):
    """
    answer_line is a dict of elements.
    it generates a colour_pool and populates it using
    number_of_dupes and number_of_elements then pops from the pool
    as it makes random choices

    """

    def __init__(self, number_of_elements=6, number_of_colours=8):
        super(answer_line, self).__init__()
        self.number_of_colours = number_of_colours
        self.number_of_elements = number_of_elements
        self.answer_line = {}
        self.colour_pool = []
        self.guess_list = []

    def return_colour_pool(self):
        list = []
        for a in range(0, self.number_of_colours):
            list.append(f"{a}: {colours[a]}")
        return list

    def return_guess_list(self):
        return self.guess_list

    def return_line(self):
        line = []
        for a in range(0, self.number_of_elements):
            line.append(self.answer_line[a].getColour())
        return line

    def choose_colours(self):

        """
        generates a colour_pool and populates it using
        number_of_dupes and number_of_elements then pops from the pool as selected
        """

        self.answer_line = {}

        for a in range(0, self.number_of_colours):
            for b in range(0, number_of_dupes):
                self.colour_pool.append(colours[a])

        if allow_blanks:
            self.colour_pool.append("Blank")

        for a in range(0, self.number_of_elements):
            ## choose random_num from range 0-len(colour_pool)
            ## then remove that element from our colour_pool
            temp_number = random.choice(range(0, len(self.colour_pool) - 1))
            choice = self.colour_pool[temp_number]
            self.colour_pool.pop(temp_number)
            self.answer_line[a] = single_element(choice)

    def validate_guess(self, guess):
        """
        Validate_guess returns true if guess passes various sanity checks.
        """
        ### Check its a list (shouldnt be needed as no but me is playing as text)
        if type(guess) is not list:
            print(f"Your Guess must be passed as a list.")
            return False
        ### Check for multiple blanks
        if guess.count("Blank") > 1:
            print(f"Only one blank is allowed at a time.")
            return False
        ### Check for correct number of elements
        if len(guess) != self.number_of_elements:
            print(f"Your guess needs to be at least {self.number_of_elements} long.")
            return False
        ### Checks on each input
        for element in guess:
            ### Actually in colour list
            if element not in colours:
                print(f"{element} is not in the list of possible colours.")
                return False
            ### higher number of dupes then allowed
            if guess.count(element) > number_of_dupes:
                print(f"Only allowed {number_of_dupes} of any given element.")
                print(f"{element} has {guess.count(element)}")
                return False
            ### blanks
            if not allow_blanks and element == "Blank":
                print(f"Blanks are set to not be allowed.")
                return False

        return True

    def check_answer(self, single_guess):
        """
        first validates single_guess
        then find black pegs replacing that element of our guess
        then find white pegs also replacing that element when found
        returns a list of pegs, will not contain any guess position information
        """
        print(f"Your Guess was {single_guess}")
        # for index in range(0,len(single_guess)):
        #     single_guess[index] = single_guess[index].capitalize()

        if not self.validate_guess(single_guess):
            # print(f"Your guess needs to be a list of colours {number_of_elements} long with max {number_of_dupes} dupes"  )
            # print("")
            return False
        else:
            # self.guess_list.append(single_guess)
            temp_answer_line = self.return_line()
            peg_list = []
            # check for black pegs
            for current_index in range(0, self.number_of_elements):
                if single_guess[current_index] == temp_answer_line[current_index]:
                    temp_answer_line[current_index] = "replaced"
                    peg_list.append("Black")
                # check for white pegs
                else:
                    # If not a black peg
                    if (
                        single_guess[current_index]
                        is not temp_answer_line[current_index]
                    ):
                        # but it is a white peg
                        if single_guess[current_index] in temp_answer_line:
                            # find it it in list
                            for a in range(0, self.number_of_elements):
                                if temp_answer_line[a] is single_guess[current_index]:
                                    # Replace first found instance
                                    temp_answer_line[a] = "replaced"
                                    break
                            peg_list.append("White")
            self.guess_list.append([single_guess, peg_list])
            return peg_list


def ask_user():
    answer = input("Input list of numbers corresponding to the colours:")
    stringified_answer = []
    for number in answer:
        try:
            stringified_answer.append(colours[int(number)])
        except ValueError:
            print(f"{number} is not a number or is not on the list")
            return ""

    response = answer_line.check_answer(stringified_answer)
    if response:
        return response, stringified_answer
    else:
        return False, False


if __name__ == "__main__":
    answer_line = answer_line()
    answer_line.choose_colours()

    # x = PrettyTable()
    # x.field_names =  [ "Guess","Response","1","2","3","4","5 6","Result" ]

    table1 = PrettyTable()
    table2 = PrettyTable()
    table3 = PrettyTable()
    table4 = PrettyTable()
    table1.field_names = range(1, (answer_line.number_of_elements) + 1)
    table2.field_names = range(1, (answer_line.number_of_elements) + 1)
    table3.field_names = ["Guess", "Response"]
    table4.field_names = ["Hidden answer"]

    while True:

        print(answer_line.return_line())
        print(table4)
        print("Your possible choices are")
        print(answer_line.return_colour_pool())

        response, stringified_answer = ask_user()
        if not response:
            print("\x1bc")
            print("Answer was not formated correctly")
            continue

        print(response, "\n")

        table3 = PrettyTable()
        table4 = PrettyTable()

        table1.add_row(stringified_answer)
        while len(response) != answer_line.number_of_elements:
            response.append("Empty")
        table2.add_row(response)

        table3.add_row([table1, table2])
        table4.add_row([table3])
        print("\x1bc")

        ## Should be better way to do this but this check is dependent on number_of_elements
        correct_response = []
        for number in range(0, answer_line.number_of_elements):
            correct_response.append("Black")

        if response == correct_response:
            print("You won congrats!")
            print("Your guess list was:")
            guess_list = answer_line.return_guess_list()
            # print(f"{guess_list}")

            table1 = PrettyTable()
            table2 = PrettyTable()
            table3 = PrettyTable()
            table4 = PrettyTable()

            # for a in range(1,answer_line.number_of_elements*2):
            # field_names.append
            table1.field_names = range(1, (answer_line.number_of_elements) + 1)
            table2.field_names = range(1, (answer_line.number_of_elements) + 1)
            table3.field_names = ["Guess", "Response"]
            table4.field_names = [answer_line.return_line()]

            for a in range(0, len(guess_list)):
                table1.add_row(guess_list[a][0])
                while len(guess_list[a][1]) != answer_line.number_of_elements:
                    guess_list[a][1].append("Empty")
                table2.add_row(guess_list[a][1])

            table3.add_row([table1, table2])
            table4.add_row([table3])
            # for a in range(0,len(guess_list)):
            #     print(f"Guess {a+1}: {guess_list[a][0]}")
            #     print(f"Response {a+1}: {guess_list[a][1]}")
            print(table4)

            break

    # print(answer_line.check_answer(test_guess))
