class Sched:
    """ Provides constant str values for columns in SHIFT_SCHEDULE.csv
    """
    SHIFT_START = "SHIFT_START"
    SHIFT_END = "SHIFT_END"
    SHIFT_ID = "SHIFT_ID"

class Ship:
    """ Provides constant str values for columns in WAREHOUSE_SHIPMENTS.csv
    """
    SHIP_DATE = "SHIP_DATE"
    ORDER_ID = "ORDER_ID"
    ORDER_LINE_ID = "ORDER_LINE_ID"
    VALUE = "VALUE"

    # Added features
    FEAT_SHIFT_ID = "SHIFT_ID"

class Trans:
    """ Provides constant str values for columns in WAREHOUSE_TRANSACTIONS.csv
    """
    START_TIME = "START_TIME"
    END_TIME = "END_TIME"
    OPERATOR_ID = "OPERATOR_ID"
    TRANSACTION_TYPE = "TRANSACTION_TYPE"
    TRANSACTION_QTY = "TRANSACTION_QTY"

    # Added feature
    FEAT_DURATION = "DURATION"
    FEAT_SHIFT_ID = "SHIFT_ID"
    FEAT_SHIFT_START = "SHIFT_START"
    FEAT_GAP = "GAP"


