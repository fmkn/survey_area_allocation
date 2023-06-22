import ast

def generate_output(input_list, filename):
    output = ""
    pairs = []
    for sub_list in input_list:
        for inner_list in sub_list:
            for i in range(len(inner_list)):
                pairs.append((inner_list[i], inner_list[(i+1)%len(inner_list)]))
    pairs.sort(key=lambda x: (x[0], x[1]))
    for pair in pairs:
        output += str(pair[0]) + "," + str(pair[1]) + "\n"
    with open(filename, "w") as f:
        f.write(output)

def read_input_list(filename):
    with open(filename, "r") as f:
        input_list = ast.literal_eval(f.read())
    return input_list

input_list = read_input_list("result_cycles.txt")
generate_output(input_list, "ttc_cycle_pairs.txt")
