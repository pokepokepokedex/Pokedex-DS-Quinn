import sqlite3 as sl
import pandas as pd  # type: ignore


def clean_lite_6(datf: pd.DataFrame) -> pd.DataFrame:
    return (datf.fillna('')
            .assign(Legendary=[1 if x else 0 for x in datf.Legendary],
                    Sp_Attack=datf['Sp. Atk'],
                    Sp_Defense=datf['Sp. Def'],
                    Type1=datf['Type 1'],
                    Type2=datf['Type 2'])
            .drop(['Sp. Atk', 'Sp. Def', 'Type 1', 'Type 2'], axis=1)
            .rename(lambda s: s.lower() + '_g6', axis='columns')
            )


df6 = pd.read_csv('../Pokemon.csv').pipe(clean_lite_6)

df7 = pd.read_csv('../pokemon_w7.csv')

df = df7.merge(df6, how='outer', left_on='name', right_on='name' + '_g6')

df.to_json('pokemon7.json')

df.to_csv('pokemon7.csv')

#conn = sl.connect('pokemon7.sqlite3')

#df.to_sql('pokemon', conn)
