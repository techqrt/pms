from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetAll:
    values : str
    page_num : int
    limit : int
    sort_by : str
    sort_order : str
    filter_key : str
    filter_value : str
    search_key : str
    from_date : datetime 
    to_date : datetime
    present_url : str = None