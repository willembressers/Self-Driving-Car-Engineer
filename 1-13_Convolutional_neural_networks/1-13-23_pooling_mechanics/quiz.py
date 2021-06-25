input_height = 4
input_width = 4
input_depth = 5

filter_height = 2
filter_width = 2

S = 2

new_height = (input_height - filter_height)/S + 1
new_width = (input_width - filter_width)/S + 1

print(f"{int(new_height)}*{int(new_width)}*{input_depth}")