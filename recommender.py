# Chase Paules
# 11/16/2016
#
# This program's behavior is to recommend users books, determine the best book given its ratings,
# and to manually add book data. For more information, refer to the readme

from review import *

def main():
    intro_message()
    ratings_dict = create_dict()
    # Prompts the user for different options that they could perform
    response = ''
    while (response != "quit"):
        response = input("next task? ")
        if (response == "add"): 
            add(ratings_dict)
        elif (response == "best"):
            best(ratings_dict)
        elif (response == "recommend"):
            recommend(ratings_dict)

def intro_message():
    print("Welcome to the Book Recommender. Type the word in the")
    print("left column to do the action on the right.")
    print("recommend : recommend books for a particular user")
    print("best      : the book with the highest rating among all users")
    print("add       : add a new book")
    print("quit      : exit the program")

# Reads a text file containg data about users and books that they have rated and
# creates a dictionary mapping the two with users as the keys and their review as the values
def create_dict():
    ratings_dict = {}
    file = open("ratings.txt")
    lines = file.readlines()
    for i in range(0,len(lines), 4):
        # Input file has extra whitespace, need to strip each line
        review = Review(lines[i+1].strip(), lines[i+2].strip(), lines[i+3].strip())
        if (not lines[i].strip() in ratings_dict):                  
            ratings_dict[lines[i].strip()] = set()
        ratings_dict[lines[i].strip()].add(review)
    return ratings_dict

# Allows the user to manually add a review into the dictionary
def add(ratings_dict):
    user = input("user? ")
    title = input("title? ")
    author = input("author? ")
    rating = input("rating? ")
    review = Review(title, author, rating)
    if (not user in ratings_dict):
        ratings_dict[user] = set()
    ratings_dict[user].add(review)

# Prints the highest rated book along with its average rating 
def best(ratings_dict):
    best_dict = {} # book title to touple of ratings sum & review count.
    review_count = 0
    ratings_sum = 0
    ratings_touple = ()
    for user in ratings_dict:
        # creates a dictionary mapping book titles to a tuple containing the culmulative sum of
        # their ratings and the number of times it was rated
        for review in ratings_dict[user]:
            if not review.get_title() in best_dict:
                best_dict[review.get_title()] = (0, 0)
            review_count = best_dict[review.get_title()][1] + 1
            ratings_sum = best_dict[review.get_title()][0] + review.get_rating()
            ratings_touple = (ratings_sum, review_count)
            # saves count and sum across all reviews before grabbing average
            best_dict[review.get_title()] = ratings_touple
    average_dict = {}
    # creates another dictionary in order to map each title to its average rating
    for title in best_dict:
        average = best_dict[title][0] / best_dict[title][1]
        average_dict[title] = average
        highest_average = average
    # finding the title with the highest average rating
    highest_title = ''
    for title in average_dict:
        if highest_average <= average_dict[title]:
            highest_average = average_dict[title]
            highest_title = title
    print("The highest rated book is:")
    print(highest_title)
    print("with an overall score of " + str(highest_average))

# Prompts the user for someone who needs book recommendations and prints their
# recommended books by finding another person with similar tastes to them and
# recommending them books that they haven't read yet and that the other person
# has rated positively           
def recommend(ratings_dict):
    similarity_score = 0
    user_similarity = {}
    user_to_recommend = input("User? ")
    for user in ratings_dict:
        if user!= user_to_recommend:
            similarity_score = 0
            # How is similarity score calculated?
            for review in ratings_dict[user]:    
                first_rating = review.get_rating()
                second_rating = book_rating_search(review.get_title(),ratings_dict[user_to_recommend])
                similarity_score += first_rating * second_rating
            user_similarity[user] = similarity_score  
    max_score = similarity_score
    max_user = ''
    # Find the most common user. Then use them to find books our user hasn't read, but will probably enjoy.
    for user in user_similarity:        
        scores = user_similarity[user]        
        if max_score <= scores:
            max_score = scores
            max_user = user
    # Searches for books that max_user has read and prints them out if the other user has not read them
    for review in ratings_dict[max_user]:
        # making sure only positivly rated books are recommended
        if int(review.get_rating()) > 0:
            #if user hasn't read the book is true, print the book.
            if not (has_user_read_book(review, ratings_dict[user_to_recommend])):
                print(review)
         
# Searches through the similar user's books and compares to the other user's
# books and finds if any of the titles match. It then returns the rating of the
# matching book            
def book_rating_search(book_to_find, user_to_recommend_books):
    for book in user_to_recommend_books:
        if book.get_title() == book_to_find:
            return book.get_rating()        
    return 0

# Searches through the similar user's books and compares to the other user's
# books and finds if any of the titles match. It then returns the review of the
# book as long as the other user hasn't read it. 
def has_user_read_book(book, user_book_dict):
    for read_book in user_book_dict:
        if read_book.get_title() == book.get_title():
            return True
    return False
    
main()
