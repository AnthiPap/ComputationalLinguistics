import sys
import re
import requests
from bs4 import BeautifulSoup   #all the libraries needed for the program to work.

from timeit import default_timer as timer #used to time the function for evaluation
import string

#Function for asking for information on a TV show, if it is among IMDb's 250 to TV shows.
#Also provides the option of creating a .txt file with information on all 250 TV shows, if he search is not fruitful.
#To test:
    #e.g. type 'Cosmos' or 'cosmos' as the search term to get information on a specific TV show.
    #e.g type 'Titanic' or 'titanic' and then also type 'yes', when asked if you want the file with the information.
#! Please, note that it takes about 5-6 minutes to gather the information before being able to be searched. !

def main():
    start = timer()
    print('Please wait while information on IMDb\'s Top TV Shows is being retrieved.', '\n')
    
    url = 'https://www.imdb.com/chart/toptv'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser') #use BS to access the page

    #use the soup object to isolate components from the html code of the page
    ratings=[]
    links=[]
    cast=[]
    votes=[]
    movies = soup.select('td.titleColumn')
    for link in soup.select('td.titleColumn a'):
        links.append(link.attrs.get('href'))
    for cast_member in soup.select('td.titleColumn a'):
        cast.append(cast_member.attrs.get('title'))
    for rating in soup.select('td.posterColumn span[name=ir]'):
        ratings.append(rating.attrs.get('data-value')[:3]) #get a rating format similar to IMDb's, e.g. 9.5 instead of all decimal points one gets without this.
    for vote in soup.select('td.ratingColumn strong'):
        votes.append(vote.attrs.get('data-value'))
    
    #Access the links extracted before to get the summary of each show, and append it to a list.
    #I mostly make use of the title id IMDb has for searching.
    summaries=[]
    for link in links:
        url_link='https://www.imdb.com'+link[0:17]
        response_url = requests.get(url_link) #open the each link
        soup_summary = BeautifulSoup(response_url.text, 'html.parser') #use BS to access the url
        s= soup_summary.find('div', attrs={"class":"summary_text"}).text.strip() #get only text
        summaries.append(s)

    

    imdb = [] #list in which dictionary items will be stored.

    for i in range(0, len(movies)): #separates the series into components
        movie_string = movies[i].get_text() #get the whole text e.g. 53.      Peaky Blinders (2013)
        movie = (' '.join(movie_string.split()).replace('.', '')) #change the format of the str
        movie_title = movie[len(str(i))+1:-7] #isolate the tile through list manipulation
        date = re.search('\((.*?)\)', movie_string).group(1) #use regexp to catch the dates. They are always inbetween parenthesis.
        rank = movie[:len(str(i))-(len(movie))] #isolate the rank of the movie through list manipulation
        data = {"s_title": movie_title,
            "date": date,
            "rank": rank,
            "cast": cast[i],
            "rating": ratings[i],
            "vote": votes[i],
            "summary": summaries[i]} #create a dictionary of all the data
        imdb.append(data) #put them in a list for futher processing
        
     
    print('Process is completed. Please, type the name of the show, e.g. Cosmos, Band of Brothers, etc.', '\n',\
          'If it is among the 250 most famous TV show of IMDb, you will get information about it.')
    end=timer()
    print('Retrieval time is', '{:0.4f}'.format((end-start)/60.0), 'minutes.')
    #user query begin here
    start2=timer()
    search_term = input('Type in the name here:   ')
    exception=['and', 'of', 'om', 'for', 'the']
    if search_term.islower():
        search_term= ' '.join(word
               if word in exception
               else word.title()
               for word in search_term.capitalize().split(' '))
    for i in imdb:
        if search_term in i['s_title']: #info on one particular TV show
            print('Rank:', i['rank'], 'out of 250', '-', i['s_title'], '('+i['date']+') -', 'Starring:', i['cast']+',', 'with a rating of', i['rating']+'.', '\n', 'Summary: ', i['summary'], '\n')
            end2=timer()
            print('Answer time is', '{:0.4f}'.format(end2-start2), 'seconds')
            return

    start3=timer()    
    print('TV show not found.', '\n') #if the show does not exist in the database
    print('Would you like a file containing information on all IMDb\'s Top TV shows instead?','\n')
    
    while True: #in case of wrong user input, so that the program is able to ask for inout again
        file_cr=input('Type Y for yes, or N for no.  ').split()
        if ''.join(file_cr)== 'N': #no file creation
            print('Thank you. Bye.')
            break
    
        elif ''.join(file_cr)=='Y': #file creation with all 250 TV shows
            print('Please, wait while the file is being created.', '\n')
            standard = sys.stdout
            sys.stdout = open('IMDb.txt','w', encoding='utf-8') #using the utf-8 option here to avoid encoding errors while writting to the file.
            print('Top Rated TV Shows', '\n') #txt creation file
            for i in imdb:
                print(i['rank'], '-', i['s_title'], '('+i['date']+') -', 'Starring:', i['cast']+',', 'with a rating of', i['rating']+'.', '\n', 'Summary: ', i['summary'], '\n')
            sys.stdout=standard
            print('Process is completed.', '\n','You will find a .txt file with the information in the same directory as irlIMDB.py.', '\n')
            end3=timer()
            print('File creation time is', '{:0.4f}'.format(end3-start3), 'seconds')
            break
    
        else:
            print('Only Y or N, please.', '\n') #wrong user input
            continue
        
    
    
if __name__ == '__main__':
    main()
