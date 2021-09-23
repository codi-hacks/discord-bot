from io import StringIO
from random import randint


class Hangman():

    def __init__(self) -> None:
        # The number the user is trying to guess
        self.word = self.generate_word()
        # Number of guesses made at getting the right number
        self.fail_count = 0
        # Track who is actually playing the game.
        self.guesser = ''
        # Track if the game is active.
        self.active = True

    def generate_word(self):
        #todo: change to newline separated txt file
        with open ("extensions\\words_for_hangman.txt",'r') as f:
            for i in f.readlines():
                word_list = i.split('|')
        index = randint(0,len(word_list)-1)
        return word_list[index]

    def guess(self):
        user_guess = input("Guess a letter that is in the word or the whole word: ")
        if len(user_guess) > 1:
            whole_word_guess = user_guess
            return ("whole_word_guess", whole_word_guess)
        else:
            return ("user_guess",user_guess)

    def game_logic(self):
        building_word = ''
        while self.active == True and self.fail_count < 6:
            word_screen = ''
            for let in self.word:
                if let not in building_word:
                    word_screen+='_ '
                else:
                    word_screen+=let
            print(word_screen)

            if word_screen == self.word:
                return "YOU WIN!"

            guess = self.guess()
            if guess[0] == "whole_word_guess":
                if guess[1] == self.word:
                    return "Hey you've guessed the word and you win!"
                else: 
                    self.fail_count +=1
                    if self.fail_count == 6:
                        print("GAME OVER.")
                    print("Sorry! {0} is not correct! You have {1} guesses left. ".format(guess[1], 6-self.fail_count))
            else:
                if guess[1] in self.word:
                    print("that's great! {0} is one of the letters!".format(guess[1]))
                    building_word+=guess[1]
                else:
                    self.fail_count +=1
                    if self.fail_count == 6:
                        print("GAME OVER.")
                    print("Sorry {0} is NOT in the word".format(guess[1]))
                    #todo: output the word on failure.


            

            


if __name__ == "__main__":

    h = Hangman()

    h.generate_word()
    print(h.game_logic())