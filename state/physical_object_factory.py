import state.physical_object as po
from state.game_object import GameObject


def get_physical_object(symb: str) -> GameObject:
    if symb == "#":
        return po.Wall()
    if symb == " ":
        return po.FreeSpace()
    if symb == "_":
        return po.MapBorder()
    if symb == "c":
        return po.Coin()
    if symb in ["^", ">", "<", "v"]:
        return po.Thorn(symb)
    if symb == "+":
        return po.ExitPortal()

    return po.Wall()
