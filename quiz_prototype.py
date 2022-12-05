import info

lives = 3
num_correct = 0
round_count = 1

#name of the wiki pages:
page1 = "Apple"
page2 = "Pear"
game_over = False

print("Try to guess which wikipedia article has more links to other articles!")
print("If you guess correctly 5 times, then you win!")
print("If you guess 3 incorrectly, then you lose!")
while not game_over:
    print(f"Round {round_count}")

    #updates/changes the wikipedia page name every round:
    if (round_count != 1):
        page1 = rand_links1
        page2 = rand_links2

    #wikipedia object (from class made in the info python file)
    wiki1 = info.Wikipedia(page1)
    wiki2 = info.Wikipedia(page2)
    
    print("\n\n\n SUMMARY:\n")
    wiki1.summary()

    #Number of links on each respective page:
    links1 = wiki1.links()[1]
    links2 = wiki2.links()[1]

    #Selects a random link from one of the pages:
    rand_links1 = wiki1.randomlinks(1)[0][0]
    rand_links2 = wiki2.randomlinks(1)[0][0]

    #produces what the correct answer is:
    answer = None
    if (links1 > links2):
        answer = "1"
    else:
        answer = "2"


    print(f"Wikipedia Article 1: {page1}")
    print(f"Wikipedia Article 2: {page2}")

    print(f"Guess Which Article has more Links")
    print(f"Option 1: {page1}")
    print(f"Option 2: {page2}")
    guess = input(f"Input Answer (type \'1\' for {page1} and \'2\' for {page2}): ")

    #Checks if the user's guess is correct or not
    #if it is correct, add to the total amount of correct guesses
    #if it is incorrect, deduct 1 from the user's lives
    if guess == answer: 
        print("Correct!")
        num_correct += 1
    elif guess == "exit": #gives player a way to exit the game
        game_over = True
    else: 
        print("Incorrect")
        lives -= 1

    #gets rid of the '/wiki/' text from the rand_links variables so it can 
    #be used in the Wikipedia class again for the next iteration of the loop
    rand_links1 = rand_links1[6:]
    rand_links2 = rand_links2[6:]

    print(f"\nLives: {lives}")
    print(f"Number of Correct Guesses: {num_correct}/5\n")

    #Lose condition:
    if (lives <= 0):
        game_over = True
        print("You ran out of lives! You lose!")
    #Win condition:
    elif (num_correct >= 5): 
        game_over = True
        print("You guessed 5 articles correctly! You Win!")

    round_count += 1
    print("\n\n")