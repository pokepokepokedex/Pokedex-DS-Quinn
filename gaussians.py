from models import df, COLORS_by_TYPE
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
from scipy.stats import norm  # type: ignore
import altair as alt  # type : ignore
from typing import Optional
from functools import reduce
from itertools import chain


def Vcat(R, S): return R & S


def Ocat(C, D): return C + D


types = set(chain.from_iterable(df[['type1', 'type2']].values)) - {np.nan}

ordering = pd.DataFrame(
    np.ones(
        (len(types),
         len(types))),
    columns=types,
    index=types)


class PokeDescribe:
    def __init__(self, datf: pd.DataFrame):
        self.TYPE_COLOR_MAPPING = COLORS_by_TYPE
        self.HEIGHT = 30
        self.WIDTH = 330
        self.xlim = (0, 180)
        self.stats = ['hp', 'attack', 'defense',
                      'sp_attack', 'sp_defense', 'speed']
        self.df = datf

        # the shared x axis for the gaussians
        self.x = np.linspace(self.xlim[0], self.xlim[1], 1000)
        # instantiate the distribrution objects
        self.gaussians = {name: norm(loc=self.df[name].mean(),
                                     scale=self.df[name].std())
                          for name in self.stats}
        # apply the pdf to the x axis, store results in a df. 
        self.bells = pd.DataFrame({**{'x': self.x},
                                   **{name: self.gaussians[name].pdf(self.x)
                                      for name in self.stats}})
        
        #base chart, x axis
        self.C = alt.Chart(self.bells,
                           height=self.HEIGHT,
                           width=self.WIDTH
                           ).mark_line(color='white').encode(
            x=alt.X('x', title=None, axis=alt.Axis(labels=False)))
        
        # dictionaryr of complete charts                   
        self.charts = {
            name: self.C.encode(
                y=alt.Y(
                    name,
                    title=None,
                    axis=alt.Axis(
                        labels=False))) for name in self.stats}
        
        # stack of bellcurves, vconcat.             
        self.BellCurves = reduce(
            Vcat, [self.charts[name] for name in self.stats])


class PokeDescribeNAME(PokeDescribe):
    def __init__(self, datf: pd.DataFrame, Name: str):
        super().__init__(datf)
        self.PSI = 50
        self.pokename = Name
        self.typ = self.df[self.df.name == self.pokename].type1.values[0]
        self.typ_color = self.TYPE_COLOR_MAPPING[self.typ]
        
        # the height you want for the vlines
        self.y_max = 1.3 * \
            max([max(ls) for ls in [self.gaussians[st].pdf(self.x) for st in self.stats]])
        
        # shared y vals for vline
        self.y = pd.DataFrame({'y': np.linspace(0, self.y_max, self.PSI)})
        
        # base chart for vline
        self.D = alt.Chart(
            self.y).mark_line(
            color=self.typ_color).encode(
            y=alt.Y(
                'y',
                title=None))
        
        # dictionary of means for each stat
        self.means = {st: self.df[self.df.name ==
                                  self.pokename][st].mean() for st in self.stats}

        # dictionary of charts for each stat, combining base chart with mean
        self.Dcharts = {st: self.D.encode(x=alt.value(self.means[st]))
                        for st in self.stats}

        # bring it all together, overlay concat within vconcat 
        self.SHOW = reduce(Vcat, [self.charts[st] + self.Dcharts[st]
                                  for st in self.stats]
                           ).configure_text(color='white', angle=90)
