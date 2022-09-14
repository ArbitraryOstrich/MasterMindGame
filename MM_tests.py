# def test_empty():
#     a_set = []
#     for index in range(0,100000):
#         a = 0
#         vwr = viewer(number_of_colours = 8, number_of_elements = 3 , multiples_of_element = 2, allow_Emptys = True)
#         while "Empty" not in vwr.controler.model.return_line():
#             a = a+1
#             print(a)
#             print(vwr.controler.model.return_line())
#             vwr = viewer(number_of_colours = 8, number_of_elements = 3 , multiples_of_element = 2, allow_Emptys = True)
#         a_set.append(a)
#     print(sum(a_set)/len(a_set))

# def test_random(vwr, loops):
#     # vwr = viewer(number_of_colours = 8, number_of_elements = 10 , multiples_of_element = 2, allow_Emptys = True)
#     index = 0
#     correct_response = []
#     for number in range(0,vwr.controler.model.number_of_elements):
#         correct_response.append('Black')
#
#     ### While loop so i can dec index from within the loop
#     while index < loops:
#         print(index)
#         index = index + 1
#         test_guess = random.sample(vwr.controler.model.colour_pool, vwr.controler.model.number_of_elements)
#         if test_guess in vwr.controler.model.return_guess_list()[0]:
#             index = index - 1
#             continue
#         response = vwr.controler.check_guess(test_guess)
#         print(response[0])
#         if response[0] == correct_response:
#             print(f"won after {index} guesses")
#             print(test_guess)
#             print(vwr.controler.model.return_line())
#             break

# def test_viwer():
#     vwr = viewer(number_of_colours = 8, number_of_elements = 6 , multiples_of_element = 2, allow_Emptys = False)
#     ##too many
#     test_guess = ['White', 'Black', 'Green', 'Orange', 'Red', 'Orange', 'Orange']
#     vwr.controler.check_guess(test_guess)
#     ##not enough
#     test_guess = ['White', 'Black', 'Yellow', 'Orange', 'Orange']
#     vwr.controler.check_guess(test_guess)
#     ##triples
#     test_guess = ['White', 'Black', 'Green', 'Orange', 'Orange', 'Orange']
#     vwr.controler.check_guess(test_guess)
#     ### unkown text
#     test_guess = ['White', 'Black', 'dfafs', 'Black', 'Orange', 'Orange']
#     vwr.controler.check_guess(test_guess)
#     #blank
#     vwr = viewer(number_of_colours = 8, number_of_elements = 6 , multiples_of_element = 2, allow_Emptys = True)
#     test_guess = ['White', 'Black', 'Green', 'Orange', 'Blue', 'Empty']
#     vwr.controler.check_guess(test_guess)
#     ##double blank
#     test_guess = ['White', 'Black', 'Green', 'Orange', 'Empty', 'Empty']
#     vwr.controler.check_guess(test_guess)
#     ##
#     test_guess = ['Red',  'Blue', 'Green', 'Yellow', 'Brown', 'Orange']
#     vwr.controler.check_guess(test_guess)

### Looks like sequential and dict both fail due to int not allowing leading 0's


def correct_response_gen(vwr):
    """
    Takes viwer and generates a list containing the word black repeated
    number_of_elements times.
    """
    correct_response = []
    for number in range(0, vwr.controler.model.number_of_elements):
        correct_response.append("Black")
    return correct_response


def sequential_brute(vwr):

    ### Something about this is not complete?? Sometimes it will fail to find answer so the combi pool must be wrong.
    from itertools import combinations

    cp = vwr.controler.model.return_colour_pool()
    correct_response = correct_response_gen(vwr)

    ## Builds list as a pool of possible elemnts
    element_pool = []
    for number in range(0, vwr.controler.model.multiples_of_element):
        for digit in range(0, vwr.controler.model.number_of_colours):
            element_pool.append(digit)

    combi = combinations(element_pool, vwr.controler.model.number_of_elements)
    combi = list(combi)

    guess_index = 0
    print(f"Possible Guesses: {len(combi)}")
    for digits in combi:
        guess_index += 1
        stringy = "".join(map(str, digits))
        response = vwr.controler.check_guess(stringy)
        if response[0] == correct_response:
            print(f"Stoped on guess: {guess_index}")
            print(f"Correct answer: {response[1]}")
            print(vwr.controler.model.return_line())
            break


def dict_brute(vwr):
    correct_response = correct_response_gen(vwr)
    # sequential_brute builds a bunch of guess just to throw them away with validation
    # Generate a dict of possible guesses first
    possible_guesses = []
    max_guess = ""
    min_guess = ""

    ##gen two strings of digits
    for digit in range(0, vwr.controler.model.number_of_elements):
        max_guess = max_guess + str(vwr.controler.model.number_of_colours)

    for guess in range(0, int(max_guess)):
        if vwr.controler.validate_guess(str(guess))[0] == True:
            possible_guesses.append(guess)

    possible_guesses = list(set(possible_guesses))

    index = 0
    response = vwr.controler.check_guess(str(possible_guesses[index]))
    while not response[0] == correct_response:
        print(index, response)
        index = index + 1
        if index >= len(possible_guesses):
            response = vwr.controler.check_guess(str(possible_guesses[index]))
            break

    print("----------------")
    print(f"took {index} guesses")
    print(f"Correct Answer was {test_guess}")
    print(response[0], vwr.controler.model.return_line())
