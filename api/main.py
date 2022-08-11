import numpy as np
import pandas as pd

from typing import List

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from pydantic import BaseModel, ValidationError, validator
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


class PredictRequest(BaseModel):
    data: float

class PredictResponse(BaseModel):
    data: List[str]


app = FastAPI()

debug=True

def get_movies(row_limit):

    if debug:print('getting file_locations')

    name_basics = "https://datasets.imdbws.com/name.basics.tsv.gz"
    title_akas = "https://datasets.imdbws.com/title.akas.tsv.gz"
    title_basics = 'https://datasets.imdbws.com/title.basics.tsv.gz'
    title_crew = 'https://datasets.imdbws.com/title.crew.tsv.gz'
    title_episode = 'https://datasets.imdbws.com/title.episode.tsv.gz'
    title_principles = 'https://datasets.imdbws.com/title.principals.tsv.gz'
    title_ratings = 'https://datasets.imdbws.com/title.ratings.tsv.gz'

    import pandas as pd

    def read_in(name, max_rows=row_limit):
        if debug: print(f'reading in file:{name}, max_rows={max_rows}')
        # data_name_basics = pd.read_csv(name, error_bad_lines=False, nrows=10, sep='\t')
        if max_rows == 0:
            dataframe = pd.read_csv(name, on_bad_lines='error', sep='\t')
        else:
            dataframe = pd.read_csv(name, on_bad_lines='error', nrows=max_rows, sep='\t')
        return dataframe

    df_title_basics = read_in(title_basics, max_rows=row_limit)
    df_title_ratings = read_in(title_ratings, max_rows=row_limit)

    if debug:print('processing output')

    df_ratings_rated = df_title_ratings[df_title_ratings["numVotes"] > 100]

    df_ratings_combined = df_title_basics.merge(df_ratings_rated, on='tconst')

    averageNumberOfVotes = df_title_ratings['numVotes'].sum()
    averageNumberOfVotes

    df_ratings_combined['ranking'] = df_ratings_combined['numVotes'] / averageNumberOfVotes * df_ratings_combined[
        'averageRating']
    # (numVotes /averageNumberOfVotes) * averageRating
    df_ratings_combined = df_ratings_combined[['originalTitle', 'numVotes', 'averageRating', 'ranking']]
    df_ratings_combined.sort_values('ranking', ascending=False)

    top_15 = df_ratings_combined.sort_values('ranking', ascending=False)[:15]
    top15_array = top_15['originalTitle'].to_list()

    if debug:print('top15_array:', top15_array, type(top15_array))

    return top15_array


@app.post("/predict", response_model=PredictResponse)
def predict(input: PredictRequest):
    row_limit = np.array(input.data)
    if debug:print('row_limit:', row_limit, type(row_limit))

    top15_array = get_movies(row_limit)

    if debug:print('top15_array:', top15_array, type(top15_array))

    result = PredictResponse(data=top15_array)

    return result


# out = get_movies(10)
# print(out)
