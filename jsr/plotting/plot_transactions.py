import polars as pl
from polars import col
from polars import selectors as cs
import plotly.graph_objects as go
import plotly.express as px
from jsr.utils.col_namespace import Sched, Ship, Trans
from jsr.utils.plotting import plot_write_image

def ship_demo1_transaction_schedule(df_transactions: pl.DataFrame, write_image=False):
    k = (df_transactions
         # .filter(col(Trans.START_TIME).dt.day() == 21)
         # .filter(col(Trans.START_TIME).dt.day() == 10)
         .filter(col(Trans.START_TIME).dt.day() == 19)
         .filter(col(Trans.START_TIME).dt.month() == 10)
         .sort("OPERATOR_ID")
         .with_columns(col(Trans.OPERATOR_ID).cast(str))
         # .filter(col(Trans.OPERATOR_ID) == 35)
         )  # .sort("START_TIME")
    pass
