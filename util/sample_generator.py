import json
import random
# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.

#https://www.youtube.com/watch?v=WumyfLEa6bU
#Title, Description, Room Description
#output to JSON objects

# importing names and descriptions that have been generated elsewhere
with open('util/names.txt', 'r') as file1:
    names_list = json.load(file1)

with open('util/desc_json.txt', 'r') as file2:
    descriptions_list = json.load(file2)


class Room:
    def __init__(self, id, name, description, x, y):
        self.id = id
        self.name = name
        self.description = description
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.x = x
        self.y = y
    def __repr__(self):
        if self.e_to is not None:
            return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
        return f"({self.x}, {self.y})"
    def connect_rooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room)
        setattr(connecting_room, f"{reverse_dir}_to", self)
    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")


class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0
        self.room_list = []
        self.coordinates = []

    def generate_rooms(self, dimension, max_tunnels, max_length):
        '''
        Randomly generate rooms using the Random Walk Algorithm
        '''
        # Initialize grid
        self.width = dimension
        self.height = dimension
        self.grid = [None] * dimension
        for i in range(len(self.grid)):
            self.grid[i] = [None] * dimension

        # Start at random point on map
        x = random.randint(0, dimension)
        y = random.randint(0, dimension)
        print("Starting at: ", x, y)
        room_count = 0

        N = (0, 1, 'n')
        E = (1, 0, 'e')
        S = (0, -1, 's')
        W = (-1, 0, 'w')

        # While the number of tunnels is not zero
        previous_room = None
        tunnels = max_tunnels
        while tunnels > 0:
            # Choose randon length from max_length
            length = random.randint(0, max_length)
            # Choose random direction to turn (N,E,S,W)
            direction = random.choice([[0, 1, 'n'], [1, 0, 'e'], [0, -1, 's'], [-1, 0, 'w']])
            # Draw a tunnel of chosen length in chosen direction and avoid edges of map
            while length > 0:
                # check if room already exists in this square
                coords = (x, y)
                if coords not in self.coordinates:
                    # create room
                    room = Room(room_count, random.choice(names_list), random.choice(descriptions_list), x, y)
                    # add coordinates to coords list
                    self.coordinates.append((x, y))

                    # add to json file for iOS guys
                    room_dict = json.dumps(room.__dict__)
                    self.room_list.append(room_dict)
                    #print("Room created at: ", x, y)
                    #print("Moving in direction: ", direction[2])
                    #print("Length of this tunnel is", length)

                    # save room to world grid
                    self.grid[y][x] = room

                    # connect room to previous room
                    if previous_room is not None:
                        previous_room.connect_rooms(room, room_direction)

                    # Update iteration variables
                    previous_room = room
                    room_count += 1

                # Try to move in chosen direction if inside grid
                if 0 <= (x + direction[0]) < dimension and 0 <= (y + direction[1]) < dimension:
                    # if new x and new y are in range, keep them and set room direction
                    x = x + direction[0]
                    y = y + direction[1]
                    room_direction = direction[2]
                else:
                    # if x or y is not in range, break loop and restart
                    length = 0

                # decrement length until 0
                length -= 1

            # Decrement the number of tunnels and repeat while loop
            tunnels -= 1


        # Loop continues until number of tunnels == 0

    '''

    def generate_rooms(self, size_x, size_y, num_rooms):
        """
        Fill up the grid, bottom to top, in a zig-zag pattern
        """

        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range( len(self.grid) ):
            self.grid[i] = [None] * size_x

        # Start from lower-left corner (0,0)
        x = -1 # (this will become 0 on the first step)
        y = 0
        room_count = 0

        # Start generating rooms to the east
        direction = 1  # 1: east, -1: west


        # While there are rooms to be created...
        previous_room = None
        while room_count < num_rooms:

            # Calculate the direction of the room to be created
            if direction > 0 and x < size_x - 1:
                room_direction = "e"
                x += 1
            elif direction < 0 and x > 0:
                room_direction = "w"
                x -= 1
            else:
                # If we hit a wall, turn north and reverse direction
                room_direction = "n"
                y += 1
                direction *= -1

            # Create a room in the given direction
            room = Room(room_count, "A Generic Room", "This is a generic room.", x, y)
            # Note that in Django, you'll need to save the room after you create it
            room_dict = json.dumps(room.__dict__)
            self.room_list.append(room_dict)

            # Save the room in the World grid
            self.grid[y][x] = room

            # Connect the new room to the previous room
            if previous_room is not None:
                previous_room.connect_rooms(room, room_direction)

            # Update iteration variables
            previous_room = room
            room_count += 1
    '''

    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"

        # The console prints top to bottom but our array is arranged
        # bottom to top.
        #
        # We reverse it so it draws in the right direction.
        reverse_grid = list(self.grid) # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(str)


w = World()
#num_rooms = 100
#width = 15
#height = 15
dimension = 15
max_tunnels = 60
max_length = 8
w.generate_rooms(dimension, max_tunnels, max_length)
w.print_rooms()

with open('rooms.txt', 'w') as file:
    json.dump(w.room_list, file)
#with open('rooms.txt', 'r') as read_file:
#    data = json.load(read_file)
#print(data)


#print(f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")
print(f"\n\nWorld\n  dimension: {dimension}\n  max_tunnels: {max_tunnels}\n  max_length: {max_length}\n number of rooms: {len(w.coordinates)}")
