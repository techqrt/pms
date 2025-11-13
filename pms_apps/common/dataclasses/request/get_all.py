from dataclasses import dataclass


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
    present_url : str = None