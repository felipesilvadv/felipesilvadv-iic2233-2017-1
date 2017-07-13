from datetime import datetime as dt
from functools import reduce


def set_id():
    i = 0
    while True:  # Lo que quedaba mejor
        yield i
        i += 1
    #return (i for i in range(1000)) # lo que tenia antes


class Cast:
    def __init__(self, movie_title, name, character):
        self.name = name
        self.movie = movie_title
        self.character = character


class Movie:
    get_id = set_id()

    def __init__(self, title, rating, release, *args):
        self.id = next(Movie.get_id)
        self.title = title
        self.rating = float(rating)
        self.release = dt.strptime(release, '%Y-%m-%d')  # 2015-03-04
        self.genres = [arg for arg in args]

    # solo para que se vea mejor el resultado final
    def __repr__(self):
        return "nombre: {1}\n generos: {2} ".format(self.id, self.title, "-".join(self.genres))


def popular(peliculas, num):
    return list(filter(lambda l: l.rating >= num, peliculas))


def with_genres(peliculas, num):
    return list(filter(lambda l: len(l.genres) >= num, peliculas))


def tops_of_genre(peliculas, genero):
    lista_ratings = [pelicula.rating for pelicula in peliculas if genero in pelicula.genres]
    lista_ratings.sort()
    lista_ratings.reverse()
    if len(lista_ratings) > 10:
        lista_ratings = lista_ratings[0:10]
    return list(filter(lambda pelicula: pelicula.rating in lista_ratings, peliculas))


def actor_rating(actor, peliculas, cast):
    cast_actor = list(filter(lambda linea: linea.name == actor, cast))
    lista_peliculas = [valor.movie for valor in cast_actor]
    lista_peliculas = list(filter(lambda pelicula: pelicula.title in lista_peliculas, peliculas))
    lista_ratings = [pelicula.rating for pelicula in lista_peliculas]
    n = len(lista_ratings)
    suma = reduce(lambda x, y: (x + y), lista_ratings)
    return suma/n


def compare_actors(actor1, actor2, peliculas, cast):
    r1 = actor_rating(actor=actor1, peliculas=peliculas, cast=cast)
    r2 = actor_rating(actor=actor2, peliculas=peliculas, cast=cast)
    if r1 == r2:
        print("Son iguales")
        return
    return actor1 if r1 > r2 else actor2


def movies_of(actor, cast):
    peliculas_actor = filter(lambda personaje: personaje.name == actor, cast)
    return list(map(lambda valor: (valor.name, valor.character), peliculas_actor))


def from_year(año, peliculas):
    return [pelicula for pelicula in peliculas if pelicula.release.year == año]


if __name__ == "__main__":
    with open('movies.txt', 'r') as f:
        archivo = list(map(lambda linea: linea.strip().split(","), f))
        lista_peliculas = list(map(lambda pelicula: Movie(*pelicula[1:]), archivo))

    with open('cast.txt', 'r') as f:
        archivo = list(map(lambda linea: linea.strip().split(","), f))
        lista_casts = list(map(lambda actor: Cast(*actor), archivo))
    # inserte los valores que mejor le parezcan
    num = 10
    print(popular(lista_peliculas, num))
    num = 3
    print(with_genres(lista_peliculas, num))
    genero = "Action"
    print(tops_of_genre(lista_peliculas, genero))
    actor = "Hugh Jackman"
    print(actor_rating(actor, lista_peliculas, lista_casts))
    actor1 = "Natalie Portman"
    print(compare_actors(actor, actor1, lista_peliculas, lista_casts))
    print(movies_of(actor, lista_casts))
    año = 2017
    print(from_year(año, lista_peliculas))
