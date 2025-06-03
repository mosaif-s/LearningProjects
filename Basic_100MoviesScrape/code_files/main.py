import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"



response=requests.get(url=URL)
soup=BeautifulSoup(response.text,"html.parser")
listOfMovies=[]
listOfMovies=[str(movie.text)+"\n" for movie in soup.find_all("h3", class_="title") ]
listOfMovies.reverse()
print(listOfMovies)

with open("Movies.txt","w", encoding="utf-8") as file:
    for movie in listOfMovies:
        file.write(movie)

