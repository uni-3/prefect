from typing import Dict, Any

class EstatDatasetConfigBase:
    """
    Base class for e-stat dataset configurations.
    Subclasses should define class attributes for 'stats_data_id' 
    and 'resource_name_suffix', and implement the 'parse' method.
    """
    stats_data_id: str
    resource_name_suffix: str

    def parse(self, statistical_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses the STATISTICAL_DATA part of the API response for this specific dataset.
        Should return a dictionary where keys are table name parts (e.g., "category", "value")
        and values are the data items to be loaded.
        """
        raise NotImplementedError("Subclasses must implement the 'parse' method.")


class PopulationDatasetConfig(EstatDatasetConfigBase):
    """
    Configuration for fetching and parsing e-stat population estimation data.
    """
    stats_data_id = "0003443840"
    resource_name_suffix = "population"

    def parse(self, statistical_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses the STATISTICAL_DATA for population estimation.
        Extracts category information and values.
        """
        cat_info = statistical_data["CLASS_INF"]["CLASS_OBJ"]
        values = statistical_data["DATA_INF"]["VALUE"]
        return {"category": cat_info, "value": values}

# Example of how another dataset would be added:
# class AnotherDatasetConfig(EstatDatasetConfigBase):
#     stats_data_id = "YOUR_OTHER_ID"
#     resource_name_suffix = "your_suffix"
#
#     def parse(self, statistical_data: Dict[str, Any]) -> Dict[str, Any]:
#         # Custom parsing logic for this dataset
#         # Example:
#         # custom_data = statistical_data["SOME_OTHER_STRUCTURE"]["DATA"]
#         # return {"custom_table": custom_data}
#         raise NotImplementedError("Parsing for AnotherDatasetConfig not implemented yet.")
