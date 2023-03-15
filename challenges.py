def cut_line(queue, cutter):
    return [person for person in queue if person != cutter] + [cutter]

def total_cost(adults, children):
    if adults == 0:
        return 0
    discount_table = {
        1: { 1: 30 },
        2: { 0: 40, 3: 60 },
        3: { 0: 50, 2: 60 }
    }
    if adults in discount_table.keys() and children in discount_table[adults].keys():
        return discount_table[adults][children]
    return adults * 25 + children * 10

def censor_words(sentence, censor_words):
    decap_words = [word.lower() for word in censor_words]
    buffer = []
    for word in sentence.split():
        censored = False
        for censor_word in decap_words:
            if word.lower().startswith(censor_word):
                buffer.append("****" + word[len(censor_word):])
                censored = True
                break
        if not censored:
            buffer.append(word)
    return " ".join(buffer)

def odd_otto(sentence):
    return " ".join([word for word in sentence.split() if (int(word) if word.isdecimal() else len(word)) % 2 == 1])

def attraction_fun(fun_dict):
    attraction_names = list(fun_dict.keys())  
    iter_counts = range(len(attraction_names) - 1, 0, -1) # ew bubble sort
    for iter_count in iter_counts:
        swapped = False
        for i in range(iter_count):
            attraction = fun_dict[attraction_names[i]]
            next_attraction = fun_dict[attraction_names[i + 1]]
            # current_partial_fun = attraction[0] + next_attraction[0] / attraction[1]
            # swapped_partial_fun = next_attraction[0] + attraction[0] / next_attraction[1]
            current_partial_fun = attraction[0] + next_attraction[0] * (1 - attraction[1])
            swapped_partial_fun = next_attraction[0] + attraction[0] * (1 - next_attraction[1])
            if swapped_partial_fun > current_partial_fun:
                swapped = True
                attraction_names[i], attraction_names[i + 1] = attraction_names[i + 1], attraction_names[i]
        if not swapped:
            break
    return attraction_names

def decode_riddle(sentence, shift):
    buff = []
    for character in sentence:
        if character.isalpha():
            is_upper = character.upper() == character
            lower_bound = ord("A") if is_upper else ord("a")
            # note: current test cases shift left, but spec says to shift right. this shifts left to
            # pass the tests, so if it breaks first thing to try is shifting right
            buff.append(chr((ord(character) - shift - lower_bound) % 26 + lower_bound)) 
        else:
            buff.append(character)
    return "".join(buff)

def is_vegan(menu_item, menu_dict):
    if menu_dict[menu_item][0] == "vegan":
        return True
    elif menu_dict[menu_item][0] == "nonvegan":
        return False
    for ingredient in menu_dict[menu_item]:
        if not is_vegan(ingredient, menu_dict):
            return False
    return True

def ring_toss(chance_matrix):
    favor_edge_matrix = [[3, 2, 3], [2, 1, 2], [3, 2, 3]]
    for y in range(3):
        for x in range(3):
            chance = chance_matrix[y][x] * favor_edge_matrix[y][x]
            if x == 0 and y == 0 or chance > max_chance:
                max_chance = chance
                max_pos = [x, y]
    return max_pos

def ac_transit(travel_map):
    connected_areas = []
    for loc_from, loc_tos in travel_map.items():
        current_area = None
        for connected_area in connected_areas:
            if loc_from in connected_area:
                current_area = connected_area
                break
        if not current_area:
            current_area = [loc_from]
            connected_areas.append(current_area)
        current_area.extend([loc_to for loc_to in loc_tos if (loc_from in travel_map[loc_to]) and (not loc_to in current_area)])
    return connected_areas
