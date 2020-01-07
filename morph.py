import os, argparse, re

def main():
    parser = argparse.ArgumentParser(description='Word mophing.')
    parser.add_argument("dictionary", type=str, help="The path for the dictionay file to use for morphing. Every line should containe only one word.")
    parser.add_argument("start", type=str, help="The first word.")
    parser.add_argument("end", type=str, help="The second word.")
    parser.add_argument("-e", type=str, help="Exclue certain words from the dictionary.", nargs="+", metavar="E", dest="excludes")

    args = parser.parse_args()

    start = (args.start).lower()
    end = (args.end).lower()

    if args.excludes != None: excludes = args.excludes
    else: excludes = []

    if len(start) != len(end):
        print("Words must be of the same length.")
        exit(2)

    if len(start) == 1 or len(end) == 1:
        print("Words must be longer that 1 character.")
        exit(2)

    if start in excludes or end in excludes:
        print("Cannot exclude the start or end words.")
        exit(2)


    dictionary = get_dictionary(args.dictionary)
    dictionary = filter_dictionary(dictionary, len(start), excludes)

    try:
        start_index = dictionary.index(start)
    except ValueError:
        dictionary.append(start)
        start_index = dictionary.index(start)

    try:
        end_index = dictionary.index(end)
    except ValueError:
        dictionary.append(end)
        end_index = dictionary.index(end)

    print(f"Morphing [{start} <-> {end}] using [{args.dictionary}]", end = "")

    if excludes:
        if len(excludes) > 1:
            excludes_string = ", ".join(excludes[:-1])
            excludes_string += " and " + excludes[-1]
        else:
            excludes_string = excludes[0]

        print(" excluding ["+ excludes_string + "]", end = "")
    print(".")

    # <BFS> 
    visited = [False]*len(dictionary)
    parents = [-1]*len(dictionary)

    visited[start_index] = True
    queue = [start_index]
    found = False

    while not found and len(queue):
        word_index = queue.pop(0)
        word_neighbors_indeces, visited = get_not_visited_neighbors_indeces(word_index, dictionary, visited)
        for neighbor_index in word_neighbors_indeces:
            parents[neighbor_index] = word_index
            queue.append(neighbor_index)
            if neighbor_index == end_index:
                found = True
    
    # </BFS>
    
    if found:
        path_of_indeces = []
        current_index = end_index
        while current_index != -1:
            path_of_indeces.append(current_index)
            current_index = parents[current_index]

        path_of_indeces.reverse()

        print("Solution: ", end = "")
        for index, word_index in enumerate(path_of_indeces):
            if index == len(path_of_indeces) - 1: end = "\n"
            else: end = " <-> "
            
            print(dictionary[word_index], end=end)

    else:
        print(f"Could't find path between \"{start}\" and \"{end}\" in the provided dictionary.")

def get_dictionary(file_path): 
    try:
        f = open(file_path, 'r')
        dictionary = f.read().splitlines()
        f.close()
    except FileNotFoundError:
        print(f"ERROR: Could not find \"{os.path.abspath(file_path)}\"")
        exit(1)
        
    except:
        print("ERROR: Couldn't open/read the dictionary file.")
        exit(1)
    
    return dictionary

def filter_dictionary(dictionary, word_length, excludes):
    filtered_dictionary = []
    for word in dictionary:
        if len(word) != word_length: continue
        if word in excludes: continue
        filtered_dictionary.append(word)
    
    return filtered_dictionary

def make_neighbors_regex(word):
    regex = []
    regex.append(f"^(?!{word[0]})[a-z]{word[1:]}$")
    regex.append(f"^{word[:-1]}(?!{word[-1]})[a-z]$")
    for i in range(1, len(word) - 1):
        regex.append(f"^{word[:i]}(?!{word[i:i+1]})[a-z]{word[i+1:]}$")
    
    return re.compile("|".join(regex))

def get_not_visited_neighbors_indeces(root_index, dictionary, visited):
    root = dictionary[root_index]
    regex = make_neighbors_regex(root)
    matches = []

    for index, word in enumerate(dictionary):
        if visited[index]: continue
        if regex.match(word):
            matches.append(index)
            visited[index] = True

    return matches, visited

if __name__ == "__main__":
    main()