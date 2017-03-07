#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 20:05:23 2017

@author: Sith
"""

import numpy as np
import csv
import matplotlib.pyplot as plt
from collections import Counter

class MovieRatings:
    
    def __init__(self):
        self.user_id = []
        self.movie_id = []
        self.ratings = []
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
            for row in reader:
                if (n < header):
                    n = n + 1
                else:
                    self.movie_dict[int(row[0])] = row[1]
        return 0
    
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
        
        for movie in self.movie_id:
            movie_high[movie][count] = movie_high[movie][count] + 1
            movie_high[movie][rating] = movie_high[movie][rating] + self.ratings[movie]
        
        zero_index = 0
        for i in xrange(0, len(movie_high)):
            if movie_high[i][ID] == 0:
                zero_index = i
            elif movie_high[i][count] == 0:
                movie_high[i][ave] = 0
            else:
                movie_high[i][ave] = movie_high[i][rating] / movie_high[i][count]
        
        movie_high.pop(zero_index)
        sorted_best = sorted(movie_high, key = lambda x: x[ave], reverse = True)
        print sorted_best
        
        best = []
        for i in xrange(0, 10):
            best.append([sorted_best[i][ID], sorted_best[i][ave]])
        return best
    
if __name__ == '__main__':
    Rating = MovieRatings()
    
    user_file = "data.txt"
    movie_file = "movies.txt"
    
    Rating.read_users(user_file)
    Rating.read_movies(movie_file)
    
    popular = Rating.popular_movies()
    
    for movie in popular:
        print Rating.movie_dict[movie[0]]
        print "Count: " + str(movie[1])
    
    best = Rating.highest_ratings()
    for movie in best:
        print Rating.movie_dict[movie[0]]
        print "Rating: " + str(movie[1])
    
    """
    for ID in Rating.user_id:
        print Rating.movie_dict[ID]
    """