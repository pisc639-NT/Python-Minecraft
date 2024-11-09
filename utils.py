import pygame
import os

def color_text(text, color: any = (255, 255, 255), show:bool = False) -> str:
    text = str(text).strip()
    color = pygame.color.Color(color)
    R, G, B = color.r, color.g, color.b
    R, G, B = int(R), int(G), int(B)
    text = f"\033[38;2;{R};{G};{B}m{text}\033[0m"
    if show:
        print(text)
    return text

def center_text(text, width:int = 0, fillchar: str = ' ', color: any = (255, 255, 255), show:bool = False) -> str:
    text = str(text)
    text = text.center(os.get_terminal_size()[0] if width == 0 else width, fillchar)
    text = color_text(text, color)
    if show:
        print(text)
    return text

def sort(d = None):
    if type(d) == dict:
        ret = {}
        for i in d:
            ret[i] = sort(d[i])
        ret = dict(sorted(ret.items()))
    elif type(d) == list:
        ret = []
        for i in d:
            ret.append(sort(i))
        ret = sorted(ret)
    elif type(d) == tuple:
        ret = tuple(sort(list(d)))
    elif type(d) == str:
        ret = d.lower()
    else:
        ret = d
    return ret