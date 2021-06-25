input_height = 32
input_width = 32

filter_height = 8
filter_width = 8

nr_filters = 20

S = 2
P = 1

new_height = (input_height - filter_height + 2 * P)/S + 1
new_width = (input_width - filter_width + 2 * P)/S + 1

print(f"{int(new_height)}*{int(new_width)}*{nr_filters}")