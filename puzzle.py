from search import SearchSpace, dfs

class PuzzleSearchSpace(SearchSpace):

    def __init__(self, joints):
        super().__init__()
        self.start_state = ("E", )
        self.joints = joints


    def get_start_state(self):
        """Returns the start state."""
        return self.start_state


    def is_goal_state(self, state):
        """Checks whether a given state is a goal state.

        Parameters
        ----------
        state
            A state of the search space

        Returns
        -------
        bool
            True iff the state is a goal state
        """      
        coordinates = []   
        first_block = [0,0,0] 
        coordinates.append(first_block)
        for block in state:
            coordinates.append(self.getNextCoordinate(block, coordinates[-1]))

        if len(state) == 26:
            for x in range(0,3):
                for y in range(0,3):
                    for z in range(0,3):
                        if [x, y, z] not in coordinates:
                            return False
            state + tuple(state[-1])
            return True
        else:
            return False


    def get_successors(self, state):
        """Determines the possible successors of a state.

        Parameters
        ----------
        state
            A state of the search space

        Returns
        -------
        list
            The list of valid successor states.
        """

        previous_block = state[-1]
        joint = True if self.joints[len(state)-1] else False
        successor_states = []
        coordinates = []   
        first_block = [0,0,0] 
        coordinates.append(first_block)
        for block in state:
            coordinates.append(self.getNextCoordinate(block, coordinates[-1]))

        if joint:
            current_direction = previous_block
            #using current_direction, determine the direction that the next block is allowed to be
            #and then using helper function, figure out the coordinate of the next block for all directions
            #and add them to successor_states

            if current_direction in ["E", "W"]:
                next_directions = ["N", "S", "D", "U"]
            elif current_direction in ["N", "S"]:
                next_directions = ["E", "W", "D", "U"]
            elif current_direction in ["U", "D"]:
                next_directions = ["E", "W", "N", "S"]

            for direction in next_directions:
                next_state = [direction, self.getNextCoordinate(direction, coordinates[-1])]
                if (all(n in range(0,3) for n in next_state[1]) and (next_state[1] not in coordinates)):
                    successor_states.append(next_state[0])
    
        else:
            #using same direction as previous block, figure out what the coordinate of the next block is
            next_state = [previous_block, self.getNextCoordinate(previous_block, coordinates[-1])]
            if (all(n in range(0,3) for n in next_state[1]) and (next_state[1] not in coordinates)):
                successor_states.append(next_state[0])
        return [state + tuple([successor]) for successor in successor_states]


    def getNextCoordinate(self, direction, coordinate):
        #getting coordinate according to direction
        result = [coordinate[0], coordinate[1], coordinate[2]]
        if direction == "U":
            result[2] = coordinate[2]+1
        elif direction == "D":
            result[2] = coordinate[2]-1
        elif direction == "N":
            result[1] = coordinate[1]+1
        elif direction == "S":
            result[1] = coordinate[1]-1
        elif direction == "E":
            result[0] = coordinate[0]+1
        elif direction == "W":
            result[0] = coordinate[0]-1
        return result


"""Computes a solution to the block puzzle.

    The solution is a trajectory, i.e. a sequence of directions
    from the set {'N', 'S', 'E', 'W', 'U', 'D'}. This trajectory is
    consistent with the shape of the puzzle and visits each subcube
    of a 3x3 cube exactly once.
    """
def puzzle_solution():
    
    puzzle = [0,1,1,1,0,1,1,0,1,1,1,0,1,0,1,1,1,1,0,1,0,1,0,1,0,0,0]
    return dfs(PuzzleSearchSpace(puzzle))


def solution_b():
    puzzle = [0,1,0,1,0,1,1,1,1,1,1,0,1,0,1,0,1,1,0,1,1,0,1,1,0,0,0]
    return dfs(PuzzleSearchSpace(puzzle))


def solution_c():
    puzzle = [0,1,1,0,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,0,1,0,1,1,1,1,0]
    return dfs(PuzzleSearchSpace(puzzle))

if __name__ == '__main__':
    print(puzzle_solution())


