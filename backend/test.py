test_list = [0, 1, 2, 3, 4, 5]
test_list_two = [6, 7, 8]

modified_list = test_list[:]
modified_list.extend(test_list_two)

print(f"Modified List: {modified_list}")
print(f"Original List: {test_list}")
