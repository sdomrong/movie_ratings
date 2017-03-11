#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 20:05:23 2017
@author: Sith
"""

import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib.transforms as trn
from collections import Counter
import seaborn as sns
import prob2utils as p2util
import string

class MovieRatings:
    
    def __init__(self):
        self.user_id = []
        self.movie_id = []
        self.ratings = []
        self.movie_genre = []
        self.movie_dict = {}

    def read_users(self, filename):    
        header = 0
        with open(filename,'rU') as f:
            reader = csv.reader(f, delimiter = '\t')
            
            n = 0
            for row in reader:
                if (n < header):
                    n = n + 1
                else:
                    self.user_id.append(int(row[0]))
                    self.movie_id.append(int(row[1]))
                    self.ratings.append(int(row[2]))
        return 0
        
    def read_movies(self, filename):
        header = 0
        with open(filename,'rU') as f:
            reader = csv.reader(f, delimiter = '\t')
            
            n = 0
            self.movie_genre.append(0)
            for row in reader:
                score = []
                if (n < header):
                    n = n + 1
                else:
                    self.movie_dict[int(row[0])] = row[1]
                    for i in xrange(2, len(row)):
                        score.append(int(row[i]))
                    self.movie_genre.append(score)
        return 0
        
    def all_ratings(self):
        rating_list = [0.0 for i in xrange(6)]
                       
        for score in self.ratings:
            rating_list[score] = rating_list[score] + 1
        return rating_list
    
    # 1st most popular movie = popular[0][0]
    # 1st most popular movie count = popular[0][1]
    # 2nd most popular movie = popular[0][0]
    def popular_movies(self):
        b = Counter(self.movie_id)
        popular = b.most_common(10)
        return popular
    
    def highest_ratings(self):
        #Count, #Rating Addition, #Average #Movie_ID
        movie_high = [[0.0, 0.0, 0.0, i] for i in range(len(self.movie_dict.keys()) + 1)]
        
        count = 0
        rating = 1
        ave = 2
        ID = 3

        movie_ratings = np.column_stack((self.movie_id, self.ratings))
        
        for movie in self.movie_dict.keys():
            mov_filter = np.array(movie_ratings)[:, 0] == movie
            ratings = movie_ratings[mov_filter, 1].tolist()
            num_ratings = len(ratings)
            sum_ratings = sum(ratings)
            movie_high[movie][count] = num_ratings
            movie_high[movie][rating] = sum_ratings
        
        zero_index = 0
        for i in xrange(0, len(movie_high)):
            if movie_high[i][ID] == 0:
                zero_index = i
            elif movie_high[i][count] == 0:
                movie_high[i][ave] = 0
            else:
                movie_high[i][ave] = float(movie_high[i][rating]) / float(movie_high[i][count])
        
        movie_high.pop(zero_index)
        sorted_best = sorted(movie_high, key = lambda x: x[ave], reverse = True)

        best = []
        for i in xrange(0, 10):
            best.append([sorted_best[i][ID], sorted_best[i][ave]])
        return best
    
    # All movie ratings of a particular genre (0-5)
    def rating_genres(self, genre):
        #print self.movie_genre
        movie_list = []
        for i in xrange(1, len(self.movie_genre)):
            if (self.movie_genre[i][genre] == True):
                movie_list.append(i)
                
        #rating_list = [0.0 for i in xrange(6)]
        rating_list = []

        for i in xrange(0, len(self.movie_id)):
            if (self.movie_id[i] in movie_list):
                #rating_list[self.ratings[i]] = rating_list[self.ratings[i]] + 1
                rating_list.append(self.ratings[i])
        return movie_list, rating_list
        
def SVD(V):
    V_ = np.array(V)
    A,E,B = np.linalg.svd(V_)
    return np.dot(A[:,0:2].T, V_)
    
    
def do_histogram(x, title, xaxis):
    with sns.color_palette("cubehelix", 5):
        a = sns.distplot(x, kde = False, bins = 5, color = sns.xkcd_rgb["lilac"])
        sns.plt.xlim((0, 6))
        sns.plt.xticks(xrange(0, 7))
        sns.plt.title(title)
        sns.plt.xlabel(xaxis)
        sns.plt.ylabel("Frequency")
        sns.plt.show()

def do_2D_plot(x, y, title, labels = None):
    ax = sns.regplot(x, y, scatter = True, color = sns.xkcd_rgb["dark pink"], fit_reg = False)
    for i in xrange(0, len(labels)):
        ax.annotate(labels[i], xy = (x[i], y[i]), xytext = (-10, 10), textcoords = "offset points",
            ha = 'right', va = 'bottom', 
            bbox = dict(boxstyle='round,pad=0.5', ec = 'None', fc='white', alpha=0.5),
            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3, rad=0'))
    sns.plt.title(title)
    sns.plt.show()

def convert_to_ASCII(labellst):
    # Ripped unabashedly from StackOverflow.
    new_lst = []
    for i in xrange(0, len(labellst)):
        new_label = filter(lambda x: x in printable, labellst[i])
        new_lst.append(new_label)
    return new_lst

def find_best_model():
    pass

if __name__ == '__main__':
    Rating = MovieRatings()
    
    user_file = "data.txt"
    movie_file = "movies.txt"
    
    Rating.read_users(user_file)
    Rating.read_movies(movie_file)
    
    #do_histogram(Rating.ratings, "Histogram of All Ratings", "Rating")


    popular = Rating.popular_movies()
    popular_ratings = []
    movie_ratings = np.column_stack((Rating.movie_id, Rating.ratings))
    print np.array(Rating.movie_id)[:] == popular[0]
    
    # Get ratings for the top 10 popular movies
    for movie in popular:
        mov_filter = np.array(Rating.movie_id)[:] == movie[0]
        popular_ratings += movie_ratings[mov_filter, 1].tolist()

        print Rating.movie_dict[movie[0]]
        print "Count: " + str(movie[1])
    #do_histogram(popular_ratings, "Ratings of Top 10 Movies", "Rating")   
    
    best = Rating.highest_ratings()
    best_ratings = []

    for movie in best:
        mov_filter = np.array(Rating.movie_id)[:] == movie[0]
        print 'avg for movie', Rating.movie_dict[movie[0]], np.mean(movie_ratings[mov_filter, 1].tolist())
        best_ratings += movie_ratings[mov_filter, 1].tolist()
        print movie_ratings[mov_filter, 1].tolist()
        print Rating.movie_dict[movie[0]]
        print "Rating: " + str(movie[1])
    #do_histogram(best_ratings, "Ratings of Highest Avg Rated Movies", "Rating")  
    
    genre6_movies, genre_6_ratings = Rating.rating_genres(6)
    genre1_movies, genre_1_ratings = Rating.rating_genres(1)
    genre7_movies, genre_2_ratings = Rating.rating_genres(7)

    do_histogram(genre_6_ratings, "Ratings for Movies of Genre 6", "Rating")
    #do_histogram(genre_1_ratings, "Ratings for Movies of Genre 1", "Rating")
    #do_histogram(genre_2_ratings, "Ratings for Movies of Genre 7", "Rating")
    
    # Do matrix factorization
    M = max(Rating.user_id)
    N = max(Rating.movie_id)
    K = 20
    learning_rate = 0.02
    lam = 0.0
    Y = np.column_stack((Rating.user_id, Rating.movie_id, Rating.ratings))
    U, V, err = p2util.train_model(M, N, K, learning_rate, lam, Y)

    V_2D = SVD(V)

    # V should have 2 x N shape, i.e. 2 features for N movies.
    random_movies = np.random.choice(Rating.movie_dict.keys(), 10)
    print random_movies, len(random_movies)
    rand_movie_labels = [Rating.movie_dict[x] for x in random_movies]
    printable = set(string.printable)

    rand_movie_labels = convert_to_ASCII(rand_movie_labels)

    print rand_movie_labels, len(rand_movie_labels)
    do_2D_plot(V_2D[0, random_movies], 
        V_2D[1, random_movies], 
        "10 Random Movies in 2D Factorization",
        rand_movie_labels)

    popular_num = [movie[0] for movie in popular]
    print popular_num
    popular_labels = convert_to_ASCII([Rating.movie_dict[x] for x in popular_num])
    do_2D_plot(V_2D[0, popular_num], 
        V_2D[1, popular_num], 
        "Most Popular Movies in 2D Factorization",
        popular_labels)

    best_num = [movie[0] for movie in best]
    best_labels = convert_to_ASCII([Rating.movie_dict[x] for x in best_num])
    do_2D_plot(V_2D[0, best_num], 
        V_2D[1, best_num], 
        "Best Avg Rated Movies in 2D Factorization",
        best_labels)

    genre6_movies = np.random.choice(genre6_movies, 10)
    genre1_movies = np.random.choice(genre1_movies, 10)
    genre7_movies = np.random.choice(genre7_movies, 10)

    do_2D_plot(V_2D[0, genre6_movies], 
        V_2D[1, genre6_movies], 
        "Genre 6 in 2D Factorization",
        convert_to_ASCII([Rating.movie_dict[x] for x in genre6_movies]))
    do_2D_plot(V_2D[0, genre1_movies], 
        V_2D[1, genre1_movies], 
        "Genre 1 in 2D Factorization",
        convert_to_ASCII([Rating.movie_dict[x] for x in genre1_movies]))
    do_2D_plot(V_2D[0, genre7_movies], 
        V_2D[1, genre7_movies], 
        "Genre 7 in 2D Factorization",
        convert_to_ASCII([Rating.movie_dict[x] for x in genre7_movies]))



    """
    for ID in Rating.user_id:
        print Rating.movie_dict[ID]
    """