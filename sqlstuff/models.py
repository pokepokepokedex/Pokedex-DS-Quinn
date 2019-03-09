import sqlite3 as sl
import pandas as pd  # type: ignore


datpath = "https://raw.githubusercontent.com/pokepokepokedex/Pokedex/master/Pokemon.csv"


def cleansk(datf: pd.DataFrame) -> pd.DataFrame:
    return (datf.fillna('')  # note: type 2 is the only one with any nulls at all
                .assign(Legendary=[1 if x else 0 for x in datf.Legendary]))


df = pd.read_csv(datpath).pipe(cleansk)

conn = sl.connect('pokemon.sqlite3')

df.to_sql('pokemon', conn)
