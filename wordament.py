import argparse
import numpy as np
from string import ascii_lowercase
import time
import nltk


class Finder:
    def __init__(self, table, words):
        self.table = table
        self.size = table.shape
        self.words = words
        self.found_list = []

    def find(self):
        index = 1
        for word in self.words:
            path = []
            visited = np.zeros(self.size)
            found, path = self.find_word(word=word, visited=visited, path=path)
            if found:
                self.found_list.append((word, path))
                self.print_result(word, path, index)
                index += 1
        print('\n=====================\n\nFound: {0} words'.format(len(self.found_list)))

    def find_word(self, word, visited, path):
        for (row, col), value in np.ndenumerate(self.table):
            if (np.sum(visited) == 0 or
                    self.is_neighbour(prev_row=path[-1][0], prev_col=path[-1][1], row=row, col=col)):
                is_valid = True
            else:
                is_valid = False
            if visited[row, col] == 0 and is_valid:
                letters_match = (value == word[0]) if len(value) == 1 else (value == word[:2])
                if letters_match:
                    new_word = word[1:] if len(value) == 1 else word[2:]
                    path.append((row, col))
                    visited[row, col] = 1
                    if len(new_word) == 0:
                        return True, path
                    found, path = self.find_word(word=new_word, visited=visited, path=path)
                    if found:
                        return True, path
                    else:
                        visited[row, col] = 0
                        del path[-1]
        return False, path

    @staticmethod
    def is_neighbour(prev_row, prev_col, row, col):
        if (row >= prev_row - 1) and (row <= prev_row + 1) and (col >= prev_col - 1) and (col <= prev_col + 1) \
                and (row != prev_row or col != prev_col):
            return True
        else:
            return False

    def print_result(self, word, path, index):
        # create array we the letters to print
        print('\n=====================\n[{0}] {1}'.format(index, word))
        empty = np.empty(self.size, dtype=object)
        empty[:] = '+'
        for (row, col) in path:
            empty[row, col] = self.table[row, col]
        out_str = ''

        # if the table has two letters make the print nicer
        for (row, col), value in np.ndenumerate(empty):
            if len(value) == 2 and value[0] != ' ':
                for r in range(self.size[0]):
                    if r != row:
                        empty[r, col] = ' ' + empty[r, col]
        # build the string to print
        for (row, col), value in np.ndenumerate(empty):
            out_str += value
            if col == self.size[1]-1:
                print(out_str)
                out_str = ''


def get_words(file_name):
    with open(file_name, 'r') as f:
        words = f.read().splitlines()
    return words


def get_words_nltk():
    try:
        words = nltk.corpus.words.words()
        return words
    except LookupError:
        print('\nfirst run:\n\n>>>import nltk\n>>>nltk.download()\n\nand then run me again')
        exit(1)


def get_table_mock(size=(4, 4)):
    table = np.chararray(size, unicode=True)
    row = 0
    col = 0
    for c in ascii_lowercase:
        if ord(c) == ord('a') + np.prod(size):
            return table
        else:
            table[row, col] = c
            col += 1
            if col == size[1]:
                row += 1
                col = 0
    return table


def get_table_from_letters(letters, size=(4, 4)):
    table = np.empty(size, dtype=object)
    two_letters = False
    two_letters_str = ''
    index = 0
    for letter in letters:
        if letter == ' ':
            two_letters = not two_letters
            if two_letters:
                continue
            else:
                letter = two_letters_str
                two_letters_str = ''
        if two_letters:
            two_letters_str += letter
            continue
        row, col = np.unravel_index(index, size)
        index += 1
        table[row, col] = letter
    return table


def get_table_from_input(size=(4, 4)):
    letters = input("\nType letters matrix from left to right, top to bottom:\n"
                    "(if you have two letters in the same bracket, put space on each side of those two, "
                    "for example: ' ae bcdefghijklmnop'):\n")
    return get_table_from_letters(letters, size)


def main():
    words = get_words_nltk()
    table = get_table_from_input(size=(4, 4))

    t = time.process_time()
    finder = Finder(table=table, words=words)
    finder.find()
    print('Elapsed Time', time.process_time() - t)


def test():
    file_name = 'words_small_test.txt'
    words = get_words(file_name=file_name)

    table = get_table_mock(size=(4, 4))
    t = time.process_time()
    finder = Finder(table=table, words=words)
    finder.find()
    print('Elapsed Time', time.process_time() - t)

    table = get_table_from_letters(letters=' aa bcdefghijkqzzzw', size=(4, 4))
    t = time.process_time()
    finder = Finder(table=table, words=words)
    finder.find()
    print('Elapsed Time', time.process_time() - t)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Wordament game word finder')
    parser.add_argument('--test', action='store_true', help='run a small test with an example')
    args = parser.parse_args()
    if args.test:
        test()
    else:
        main()
