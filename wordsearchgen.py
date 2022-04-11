import string
import random
import time
from typing import List

class WordTooLongError(Exception):
    pass

class IllegalStringError(Exception):
    pass

class TooManyWordsError(Exception):
    pass

class CannotFitError(Exception):
    pass

class Word:
    def __init__(self, word, board_placement, direction):
        self.word = word
        self.placement: Point = board_placement
        self.direction = direction

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SquareWordSearch:
    """A square wordsearch generator class.
    Here are some examples of usage.

    >>># Generate a word search puzzle of size 8x8 with the words "Hello"
    >>># and "World" found somewhere within.
    >>>word_search = SquareWordSearch(["Hello", "World"])
    """
    directions =          [(1,0), (1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1), (1,1)]
    opposite_directions = [(-1,0),(-1,1),(0,1), (1,1),  (1,0), (1,-1),(0,-1),(-1,-1)]
    def __init__(self, words, size=8, seeded=False):
        """Generates a word search.

        Arguments:

        words -- list of strings containing english letters [A-Za-z].
        Inputting an invalid string in words will result in an InvalidStringError
        exception.
        Inputting a number of words greater than size will result in a
        TooManyWordsError exception.

        size -- integer length and width of the generated board. 
        Must be strictly greater than or equal to the length of the longest word,
        otherwise a WordTooLongError exception will be generated.

        seeded -- if True, each run will be randomly different from the last.
        """

        legal_characters = {c for c in string.ascii_letters}

        # Validate basic error cases.
        if len(words) > size:
            raise TooManyWordsError("Too many words were provided.")

        long_words = []
        illegal_words = []
        for word in words:
            for c in word:
                if c not in legal_characters:
                    illegal_words.append(word)

            if len(word) > size:
                long_words.append(word)        
        
        if illegal_words:
            raise IllegalStringError(f"The following strings contained letters other than a-z and A-Z: {illegal_words}")

        if long_words:
            raise WordTooLongError(f"The following words were too long: {long_words}")
        
        del illegal_words
        del long_words
        del legal_characters

        if seeded:
            random.seed(time.time())
        else:
            random.seed("Hello, WordSearch!")

        # Create a random board.
        self.result = [[random.choice(string.ascii_letters).upper() for column in range(size)] for row in range(size)]

        # Algorithm start.
        
        # Sort the words by their length, descending.
        words_by_len = [word.upper() for word in sorted(words, key=lambda x: len(x), reverse=True)]
        
        # Create a board (2D array) with empty tiles where the words will be placed.
        # The board will go down as y gets larger, and go right as x gets larger.
        board = [['' for column in range(size)] for row in range(size)]

        # A list of class Word instances for each word that has been entered.
        # Represents words that have been added to the board.
        added_words: List[Word] = []

        while words_by_len:
            current_word: str = words_by_len[0]
            
            if len(current_word) == 0:
                break
            possible_intersected_words: List[Word] = []
            # Look for places where 2 words could intersect.
            for added_word in added_words:
                # The positions where the added word has letters that intersect
                # with the current word.
                collision_positions: Point = []
                # The starting position of the word on the board, from the first
                # letter.
                pos = added_word.placement
                # The direction the word is written on the board. 
                dir = added_word.direction
                # The characters of the current word that intersect with the
                # added word.
                collision_chars = set()
                # Find matching characters between the two words
                for c in set(current_word):
                    for i, c2 in enumerate(added_word.word):
                        if c == c2:
                            new_point = Point(pos.x + dir[0] * i, pos.y + dir[1] * i)
                            collision_chars.add(c)
                            collision_positions.append(new_point)

                for point in collision_positions:
                    for i, c in enumerate(current_word):
                        if c in collision_chars:
                            print(c)
                            before = i
                            after = len(current_word) - (i + 1)
                            
                            direction_index = SquareWordSearch.directions.index(added_word.direction)
                            opposite = (-added_word.direction[0], -added_word.direction[1])
                            possible_dirs = [dir for dir in SquareWordSearch.directions if dir not in (added_word.direction, opposite)]
                            
                            possible_pos: List[Point] = []
                            to_remove = []
                            for i, dir in enumerate(possible_dirs):
                                beginning_x = point.x + before * -dir[0]
                                beginning_y = point.y + before * -dir[1]
                                ending_x = point.x + after * dir[0]
                                ending_y = point.y + after * dir[1]
                                
                                if beginning_x >= 0 and beginning_x < size and \
                                beginning_y >= 0 and beginning_y < size and \
                                ending_x >= 0 and ending_x < size and \
                                ending_y >= 0 and ending_y < size:
                                    possible_pos.append(Point(beginning_x, beginning_y))
                                else:
                                    to_remove.append(i)

                            for index in to_remove[::-1]:
                                possible_dirs.pop(index)
                            
                            if len(possible_dirs) != len(possible_pos):
                                raise Exception("The length of possible directions was different than that of the possible positions.")

                            to_remove = []

                            # Filter by intersections with other words already on the board
                            for i, pos in enumerate(possible_pos):
                                for j in range(len(current_word)):
                                    # if the board at any point in the word is occupied, remove that possibility.
                                    x = pos.x + j*possible_dirs[i][0]
                                    y = pos.y + j*possible_dirs[i][1]

                                    if board[y][x] != current_word[j] and i not in to_remove:
                                        to_remove.append(i)

                            for index in to_remove[::-1]:
                                possible_dirs.pop(index)
                                possible_pos.pop(index)
                            
                            if possible_pos:
                                for i, pos in enumerate(possible_pos):
                                    possible_intersected_words.append(Word(current_word, pos, possible_dirs[i]))

            # Generate permutations of where a single word could be placed.
            end = len(current_word) - 1
            possible_single_words: List[Word] = []
            for dir in SquareWordSearch.directions:
                for y, row in enumerate(board):
                    for x, col in enumerate(row):
                        if x + end * dir[0] > size - 1 or y + end * dir[1] > size - 1 or \
                            x + end * dir[0] < 0 or y + end * dir[1] < 0:
                            continue
                        else:
                            for i in range(len(current_word)):
                                if board[y + i * dir[1]][x + i * dir[0]] and board[y + i * dir[1]][x + i * dir[0]] != current_word[i]:
                                    print(board[y + i * dir[1]][x + i * dir[0]], current_word, current_word[i])
                                    break
                            else:
                                possible_single_words.append(Word(current_word, Point(x,y), dir))

            print('\n'.join([' '.join([c if c != '' else ' ' for c in x]) for x in board]))
            choice: Word = None
            print(possible_intersected_words)
            if possible_intersected_words and random.randint(0,1):
                choice = random.choice(possible_intersected_words)
            elif possible_single_words:
                choice = random.choice(possible_single_words)
            else:
                raise CannotFitError("Could not fit word into the puzzle.")
            # TODO: Remember to pop word out of words_by_len at the end.
            for i, c in enumerate(current_word):
                pos = choice.placement
                dir = choice.direction
                board[pos.y + i * dir[1]][pos.x + i * dir[0]] = c
            
            added_words.append(choice)
            words_by_len.pop(0)
        
        self.added_words = added_words
        self.result = [[self.result[y][x] if not board[y][x] else board[y][x] for x, _ in enumerate(row)] for y, row in enumerate(self.result)]

    def __str__(self) -> str:
        return '\n'.join([' '.join(x) for x in self.result])


if __name__=="__main__":
    # Enter your list of words below:
    word_list = ["Hello","World"]
    x = SquareWordSearch(word_list, size=25)
    print(x)