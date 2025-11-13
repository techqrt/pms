from dataclasses import dataclass


@dataclass
class GenerateExcelPDF:
    module_type: str
    file_name: str
    filter_key: str
    filter_value: str
    title: str
    download_type: str

