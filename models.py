import sqlite3 as sl
import pandas as pd  # type: ignore


COLORS_by_TYPE = {
    'fire': 'red',
    'water': '#09E1FF',
    'normal': '#1DFDA8',
    'poison': '#B918FF',
    'electric': 'yellow',
    'ground': '#FF9C15',
    'fairy': '#FF69B4',
    'grass': '#34FF5C',
    'bug': '#90EE38',
    'psychic': '#B71ECF',
    'rock': '#DCB883',
    'fighting': '#FF3A17',
    'ghost': '#6817ff',
    'ice': '#52fffa',
    'dragon': '#a533ff',
    'dark': '#3D009C',
    'flying': '#4da1ff',
    'steel': '#bfbfbf'}


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


def clean_7(datf: pd.DataFrame) -> pd.DataFrame:
    '''we need to renamed `against_fight` to `against_fighting`'''
    return datf


df6 = pd.read_csv('Pokemon.csv').pipe(clean_lite_6)

df7 = pd.read_csv('pokemon_w7.csv').pipe(clean_7)

df = df7.merge(df6, how='outer', left_on='name', right_on='name' + '_g6')


#conn = sl.connect('pokemon7.sqlite3')

#df.to_sql('pokemon', conn)
