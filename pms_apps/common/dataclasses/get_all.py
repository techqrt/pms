from dataclasses import dataclass


@dataclass
class GetAll:
    values: str
    page_num: int
    limit: int
    sort_by: str
    sort_order: str
    filter_key: str
    filter_value: str
    search_key: str
    

    def __post_init__(self):
        self.values_list = self.values.split(',') if len(self.values.split(',')) > 0 and self.values != '' else []
        if not self.sort_by:
            self.sort_by = 'name'
        if not self.sort_order:
            self.sort_order = 'asc'

        self.ordering = f"{'-' if self.sort_order == 'desc' else ''}{self.sort_by}"
