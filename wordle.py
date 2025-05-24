import random
import time
import copy
import os
from termcolor import colored


# converts file containing valid words into a python list for the program to use
def read_file_to_list(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        lines = [line.strip() for line in lines]
        return lines
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

# storing list of valid words here
valid_words = read_file_to_list("wordle_words.txt")

def start_new_game():
    return WordleBoard(random.choice(valid_words))


class WordleBoard(object):

    def __init__(self, word):
        self.board = [["[   ]" for j in range(5)] for i in range(6)]
        self.goal_word = word
        self.number_of_guesses = 0
        self.previous_guesses = []
        self.letters = []
        self.keyboard = KeyBoard(self.goal_word)

    def get_board(self):
        return self.board
    
    def copy(self):
        new_board = []
        for row in self.get_board():
            new_board.append([[letter] for letter in row])
        game = WordleBoard(self.goal_word)
        game.board = new_board
        game.previous_guesses = copy.copy(self.previous_guesses)
        game.letters = self.letters
        game.keyboard = self.keyboard
        game.number_of_guesses = self.number_of_guesses
        return game

    def game_over(self):
        word = ""
        for letter in self.get_board()[self.number_of_guesses-1]:
            word += letter[0]
        if word == self.goal_word:
            return True, True
        elif self.number_of_guesses == 6:
            return True, False
        else:
            return False, False
        
    def get_input(self):
        guess = input("Enter a 5 letter word: ")
        if guess == "0":
            quit()
        if guess == "1":
            GameLoop()
        if (guess in valid_words) and guess not in self.previous_guesses:
            self.previous_guesses.append(guess)
            new_row = []
            letter_index = 0
            self.keyboard.key_update(guess)
            for letter in guess:
                self.letters.append(letter)
                new_row.append(self.letter_color_evaluation(letter, letter_index))
                letter_index += 1
            self.board[self.number_of_guesses] = new_row
            self.number_of_guesses += 1
        elif guess in self.previous_guesses:
            print("Try a new word.\n")
            time.sleep(1.2)
        else:
            print("Not a valid word. Try again.\n")
            time.sleep(1.2)

    def letter_color_evaluation(self, letter, letter_index):
        if letter == self.goal_word[letter_index]:
            return [letter, "green"]
        elif letter in self.goal_word:
            return [letter, "yellow"]
        else:
            return [letter, "light_red"]

    def __str__(self):
        out_string = ""
        for row in self.board[:self.number_of_guesses]:
            for letter in row:
                out_string += "[ " + colored(letter[0], letter[1]) + " ]"
            out_string += "\n"
        for row in self.board[self.number_of_guesses:]:
            for item in row:
                out_string += str(item)
            out_string += "\n"
        return out_string
    

class KeyBoard(object):

    def __init__(self, word):
        self.goal_word = word
        self.letters = []

    def __str__(self):
        row1 = "qwertyuiop"
        row2 = "asdfghjkl"
        row3 = "zxcvbnm"
        keys = [row1, row2, row3]
        out_string = ""
        for row in keys:
            for letter in row:
                flag = True
                for sletter in reversed(self.letters):
                    if letter == sletter[0]:
                        out_string += colored(letter, sletter[1]) + " "
                        flag = False
                        break
                if flag:
                    out_string += colored(letter, "white") + " "           
            out_string += "\n"
        return out_string
    
    def key_update(self, word):
        index = 0
        for letter in word:
            if letter == self.goal_word[index]:
                self.letters.append([letter, "green"])
                index += 1
            elif letter in self.goal_word:
                self.letters.append([letter, "yellow"])
                index += 1
            else:
                self.letters.append([letter, "light_red"])
                index += 1
            

class GameLoop(object):

    def __init__(self):
        self.game = start_new_game()
        self.GameLaunch()
        self.MainLoop()
        self.PlayAgain()

    def GameLaunch(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n\nWordle in the Terminle\n")
        time.sleep(.8)
        print("Created by Ben Menko\n\n")
        time.sleep(1.7)

    def GameFrame(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n")
        print("Wordle in the Terminle")
        print("Enter 0 to quit or 1 to restart\n")
        print(self.game)
        print(self.game.keyboard)

    def MainLoop(self):
        while self.game.number_of_guesses < 6:
            self.GameFrame()
            if self.game.game_over()[0]:
                if self.game.game_over()[1]:
                    self.GameFrame()
                    print("You win!\nThe word was " + self.game.goal_word)
                    break
                else:
                    self.GameFrame()
                    print("You lose!\nThe word was " + self.game.goal_word)
                    break
            self.game.get_input()
        if self.game.game_over()[1]:
            self.GameFrame()
            print("You win!\nThe word was " + self.game.goal_word)
        else:
            self.GameFrame()
            print("You lose!\nThe word was " + self.game.goal_word)

    def PlayAgain(self):
        not_satisfied = True
        while not_satisfied:
            go_again = input("Play again? (y/n): ")
            if go_again in ["y","n","Y","N","Yes","No","yes","no"]:
                not_satisfied = False
            else:
                print("Invalid input\n")
                time.sleep(1.2)
                os.system('cls' if os.name == 'nt' else 'clear')
        if go_again in ["y","Y","Yes","yes"]:
            os.system('cls' if os.name == 'nt' else 'clear')
            GameLoop()
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            quit()

if __name__ == "__main__":
    GameLoop()
