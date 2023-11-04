import pygame


def delete_duplicate(list_of_objects: list):
    unique_list_of_objects = []
    for element in list_of_objects:
        if element not in unique_list_of_objects:
            unique_list_of_objects.append(element)

    return unique_list_of_objects


def collision_test(main_rect: pygame.Rect, rects: list[pygame.Rect]) -> list[pygame.Rect]:
    hit_list: list[pygame.Rect] = []
    
    for rect in rects:
        if main_rect.colliderect(rect):
            hit_list.append(rect.copy())
            
    return hit_list