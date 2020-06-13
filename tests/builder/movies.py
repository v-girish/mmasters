from mmasters.client.model.movie import Movie, Rating

Dangal = Movie(title="Dangal",
               release_year="2009",
               release_date="25 Dec 2009",
               director="Rajkumar Hirani",
               ratings=[Rating("Internet Movie Database", "8.4/10"), Rating("Rotten Tomatoes", "100%")])

Wanted = Movie(title="Wanted",
               release_year="2008",
               release_date="27 June 2008",
               director="Timur Bekmambetov",
               ratings=[Rating("Internet Movie Database", "6.7/10"), Rating("Rotten Tomatoes", "71%")])
