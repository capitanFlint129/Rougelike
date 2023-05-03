import pytest
from state.game_map import Room, GameObject, GameMap, Enemy
from state.physical_object import Door

"""
    Tests for Room
"""


def test_room_initialization():
    room = Room("test_room")

    assert room.width == 0
    assert room.height == 0
    assert room.name == "test_room"
    assert room.type is None
    assert room.connections == {"left": None, "right": None, "top": None, "bottom": None}
    assert room.game_map == []
    assert room.enemies == set()
    assert room.is_finale is False


def test_opposite_direction():
    room = Room("test_room")

    assert room.opposite_direction("left") == "right"
    assert room.opposite_direction("right") == "left"
    assert room.opposite_direction("top") == "bottom"
    assert room.opposite_direction("bottom") == "top"
    assert room.opposite_direction("invalid") == ""


def test_connect():
    room1 = Room("room1")
    room2 = Room("room2")

    room1.connect(room2, "left")

    assert room1.connections["left"] == room2
    assert room2.connections["right"] == room1

    with pytest.raises(ValueError):
        room1.connect(room2, "invalid")


def test_get_available_rooms():
    room1 = Room("room1")
    room2 = Room("room2")
    room3 = Room("room3")

    room1.connect(room2, "left")
    room1.connect(room3, "top")

    available_rooms = room1.get_available_rooms()

    assert available_rooms == {room2: "left", room3: "top"}


def test_add_doors_to_room():
    room1 = Room("room1")
    room2 = Room("room2")
    room1.width = 10
    room1.height = 10
    room2.width = 10
    room2.height = 10
    room1.game_map = [[None for _ in range(room1.width)] for _ in range(room1.height)]
    room2.game_map = [[None for _ in range(room2.width)] for _ in range(room2.height)]

    room1.connect(room2, "left")
    door = Door()

    room1.add_doors_to_room(door)

    assert room1.game_map[5][0] == door
    assert room1.game_map[4][0] == door
    assert room1.game_map[0][5] is None
    assert room1.game_map[9][5] is None


"""
    Tests for GameMap
"""


def test_game_map_initialization():
    starting_room = Room("starting_room")
    game_map = GameMap(starting_room, 10)

    assert game_map.current_room == starting_room
    assert game_map.number_of_rooms == 10


def test_move():
    starting_room = Room("starting_room")
    room2 = Room("room2")
    starting_room.connect(room2, "left")
    game_map = GameMap(starting_room, 2)

    assert game_map.move("left") is None
    assert game_map.current_room == room2
    assert game_map.move("right") is None
    assert game_map.current_room == starting_room
    assert game_map.move("invalid") == "Cannot move in the invalid direction."


def test_add_room_to_current_room():
    starting_room = Room("starting_room")
    room2 = Room("room2")
    game_map = GameMap(starting_room, 2)

    game_map.add_room_to_current_room(room2, "left")

    assert starting_room.connections["left"] == room2
    assert room2.connections["right"] == starting_room


def test_get_enemies():
    starting_room = Room("starting_room")
    enemy = Enemy()
    starting_room.enemies.add(enemy)
    game_map = GameMap(starting_room, 1)

    assert game_map.get_enemies() == {enemy}


def test_get_map():
    starting_room = Room("starting_room")
    game_map = GameMap(starting_room, 1)

    assert game_map.get_map() == starting_room.game_map


def test_get_object_at():
    starting_room = Room("starting_room")
    game_map = GameMap(starting_room, 1)

    assert game_map.get_object_at(0, 0) is None


def test_set_object_at():
    starting_room = Room("starting_room")
    starting_room.width = 10
    starting_room.height = 10
    starting_room.game_map = [[None for _ in range(starting_room.width)] for _ in range(starting_room.height)]

    game_object = Door()
    game_map = GameMap(starting_room, 1)

    game_map.set_object_at(0, 0, game_object)

    assert game_map.get_object_at(0, 0) == game_object


def test_current_room_is_finale():
    starting_room = Room("starting_room")
    game_map = GameMap(starting_room, 1)

    assert game_map.current_room_is_finale() is False

    starting_room.is_finale = True

    assert game_map.current_room_is_finale() is True


def test_get_height():
    starting_room = Room("starting_room")
    starting_room.height = 10
    game_map = GameMap(starting_room, 1)

    assert game_map.get_height() == 10


def test_get_width():
    starting_room = Room("starting_room")
    starting_room.width = 10
    game_map = GameMap(starting_room, 1)

    assert game_map.get_width() == 10