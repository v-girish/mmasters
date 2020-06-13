# mmasters
Practice flask web app

## Problem statement

"MMasters" is a movie inventory company and they wish to introduce new features in their system.

MMasters is an "API first" company providing a lot of APIs around movie snapshots. They would like to introduce few features in the system -
They wish to pull movie snapshots from OMDB (http://www.omdbapi.com/) and store in our system.
They would also like to allow anyone to retrieve these movie snapshots.

As mentioned, they are an "API first" company and they now expect to build two APIs -
    - one that gets all the movie snapshots from our system
        - is an OPEN API
    - one that creates movie snapshots in our system by fetching the information from omdb
        - is a protected API
        - every request should contain a header "x-api-key" with "d2ViLWFwcGxpY2F0aW9uLWluLWZsYXNr" as the value
        - *allow our people to pass mutiple movie titles to be fetched from OMDB

They expect proper REST status in the system:
- 500 for INTERNAL_SERVER_ERROR
- 200 for OK
- 201 for CREATED
- 401 for UNAUTHORIZED

...and so on

Movie snapshot includes - 
- title
- release year
- release date
- director
- and ratings which is a collection

Summarizing -

As a part of the system
- build APIs, 
- ensure security, 
- fetch from OMDB, 
- store in the system, 
- get all movie snapshots from the system
- and needless to say, ensure that the system is properly tested

### Running Migrations
```shell script
export FLASK_APP='run_app.py'
flask db upgrade
```

### Running the Application
```shell script
export API_KEY='<private api key>'
export OMDB_API_KEY='<your omdb api key>'
export FLASK_APP='run_app.py'
flask run
```

