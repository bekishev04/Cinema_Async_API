from loader import PostgresToES
import schemas


def run_etl():
    index_dict = {
        "movies": {
            "index_schema": "schemas/index_schema_movies.json",
            "model_schema": schemas.Movie,
        },
        "genres": {
            "index_schema": "schemas/index_schema_genres.json",
            "model_schema": schemas.Genre,
        },
        "persons": {
            "index_schema": "schemas/index_schema_persons.json",
            "model_schema": schemas.Person,
        },
    }
    PostgresToES(index_dict=index_dict).migrate()


if __name__ == "__main__":
    run_etl()
