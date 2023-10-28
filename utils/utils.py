def delete_duplicate(list_of_objects: list):
    unique_list_of_objects = []
    for element in list_of_objects:
        if element not in unique_list_of_objects:
            unique_list_of_objects.append(element)

    return unique_list_of_objects
