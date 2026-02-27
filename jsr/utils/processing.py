import datetime
from typing import List, Dict, Any

from jsr.utils.col_namespace import Sched, Trans, Ship
import polars as pl

def process_dataframes(data_folder_loc: str) -> Dict[str, pl.DataFrame]:
    """ Script to process the simulated data into three dataframes.
    Args:
        data_folder_loc: location of the data folder containing:
            WAREHOUSE_SHIPMENTS.csv, SHIFT_SCHEDULE.csv, and WAREHOUSE_TRANSACTIONS.csv

    Returns:
        Dictionary of processed dataframes.
    """
    # Process schedule first because we'll assign shift IDs to other dfs
    df_schedule = _process_schedule(
        data_folder_loc=data_folder_loc,
        csv_filename="SHIFT_SCHEDULE.csv",
    )

    df_transactions = _process_transactions(
        data_folder_loc=data_folder_loc,
        csv_filename="WAREHOUSE_TRANSACTIONS.csv",
        df_schedule=df_schedule
    )

    df_shipments = _process_shipments(
        data_folder_loc=data_folder_loc,
        csv_filename="WAREHOUSE_SHIPMENTS.csv",
        df_schedule=df_schedule
    )

    return {"transactions": df_transactions, "shipments": df_shipments, "schedule": df_schedule}


def _process_schedule(data_folder_loc: str,
                      csv_filename: str) -> pl.DataFrame:
    df = pl.read_csv(data_folder_loc + "/" + csv_filename, infer_schema_length=1000)

    # Remap shift start and stop times to datetime
    expr_start_datetime = (pl.col(Sched.SHIFT_START)
                           .str.to_datetime(format="%m/%d/%Y %R"))
    expr_end_datetime = (pl.col(Sched.SHIFT_END)
                         .str.to_datetime(format="%m/%d/%Y %R"))
    df = df.with_columns(expr_start_datetime, expr_end_datetime)
    return df

def _process_transactions(data_folder_loc: str, csv_filename: str,
                          df_schedule: pl.DataFrame) -> pl.DataFrame:
    df = pl.read_csv(data_folder_loc + "/" + csv_filename, infer_schema_length=1000)

    # Remap transaction start and stop times to datetime
    expr_start_datetime = (pl.col(Trans.START_TIME)
                           .str.to_datetime(format="%b %e, %Y %r"))
    expr_end_datetime = (pl.col(Trans.END_TIME)
                         .str.to_datetime(format="%b %e, %Y %r"))
    df = df.with_columns(expr_start_datetime, expr_end_datetime)

    # Remap transaction quantity onto integer values
    expr_quantity_integer = (
        pl.col(Trans.TRANSACTION_QTY)
        .str.replace_all(",", "")
        .cast(pl.Int64)
    )
    df = df.with_columns(expr_quantity_integer)

    # Add a new feature: duration in seconds for transaction
    df = df.with_columns(
        DURATION=(
                pl.col(Trans.END_TIME) - pl.col(Trans.START_TIME)
        ).dt.total_seconds() # convert to seconds
    )

    # Add a new feature: shift ID of shift working during start of transaction
    l_transaction_start_times = df[Trans.START_TIME].to_list()
    shift_ids = _find_shift_ids(l_transaction_start_times, df_schedule)
    df = df.with_columns(pl.Series(Trans.FEAT_SHIFT_ID, shift_ids))
    return df

def _process_shipments(data_folder_loc: str,
                       csv_filename: str, df_schedule: pl.DataFrame) -> pl.DataFrame:
    df = pl.read_csv(data_folder_loc + "/" + csv_filename, infer_schema_length=1000)

    # Remap ship date to datetime
    expr_ship_date = pl.col(Ship.SHIP_DATE).str.to_datetime(format="%m/%d/%Y")
    df = df.with_columns(expr_ship_date)

    # New feature: Joint shift id (A&B or C&D) that took place during shipment
    l_shipment_dates = df[Ship.SHIP_DATE].to_list()
    shift_ids = _find_shift_ids(l_shipment_dates, df_schedule)
    remap = dict(A="AB", B="AB", C="CD", D="CD")
    shift_ids = [remap[i] for i in shift_ids]
    df = df.with_columns(pl.Series(Ship.FEAT_SHIFT_ID, shift_ids))
    return df


def _find_shift_ids(events: List[datetime.datetime],
                    df_schedule: pl.DataFrame) -> List[str]:
    """ Finds the shift (A, B, C or D) that took place during the given event
    Args:
        events: List of timestamp events to find shift for

    Returns:
        List[str]: Shift IDs

    Notes:
        This is not an efficient function to map very large sets of shift IDs
        because it iterates over all schedule times for each event.
    """
    shift_list = df_schedule.to_struct().to_list()
    shift_ids = [_find_shift_id(event, shift_list) for event in events]
    return shift_ids

def _find_shift_id(event: datetime.datetime, shift_list: List[Dict]) -> Any | None:
    """ Helper function for _find_shift_ids
    """
    for shift in shift_list:
        start, end, shift_id = shift["SHIFT_START"], shift["SHIFT_END"], shift["SHIFT_ID"]
        if event < end and event >= start:
            return shift_id


