from dataclasses import dataclass


@dataclass
class Get:
    values: str

    def __post_init__(self):
        self.values_list = self.values.split(',') if self.values and len(self.values.split(',')) > 0 else []
