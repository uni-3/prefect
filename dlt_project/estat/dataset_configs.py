from abc import ABC, abstractmethod
from typing import Dict, Any, List # Added List for potential use in parse method's return value, though Dict[str, Any] is primary.

class EstatDatasetConfigBase(ABC):
    """
    Abstract Base Class for e-stat dataset configurations.
    Subclasses must define class attributes for 'stats_data_id' (str)
    and 'resource_name_suffix' (str), and implement the 'parse' method.
    """
    stats_data_id: str 
    resource_name_suffix: str

    @abstractmethod
    def parse(self, statistical_data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]: # Adjusted return type for more common dlt resource structure
        """
        Parses the STATISTICAL_DATA part of the API response for this specific dataset.
        Should return a dictionary where keys are table name parts (e.g., "category", "value")
        and values are lists of dictionaries (data items) to be loaded by dlt.
        """
        pass

class PopulationDatasetConfig(EstatDatasetConfigBase):
    """
    Configuration for fetching and parsing e-stat population estimation data.
    """
    stats_data_id: str = "0003443840" # Explicitly assign, already correct
    resource_name_suffix: str = "population" # Explicitly assign, already correct

    def parse(self, statistical_data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]: # Adjusted return type
        """
        Parses the STATISTICAL_DATA for population estimation.
        Extracts category information and values.
        dlt resources typically expect an iterable of dictionaries.
        """
        # CLASS_OBJ is usually a list of dictionaries (categories)
        # VALUE is usually a list of dictionaries (data rows)
        cat_info: List[Dict[str, Any]] = statistical_data["CLASS_INF"]["CLASS_OBJ"]
        values: List[Dict[str, Any]] = statistical_data["DATA_INF"]["VALUE"]
        
        # Ensure the parser returns data in a format dlt.resource expects (e.g., list of dicts)
        # If cat_info or values are not already List[Dict], they might need transformation.
        # Assuming they are, based on typical e-stat structures.
        return {"category": cat_info, "value": values}

# Example of how another dataset would be added:
# class AnotherDatasetConfig(EstatDatasetConfigBase):
#     stats_data_id = "YOUR_OTHER_ID"
#     resource_name_suffix = "your_suffix"
#
#     def parse(self, statistical_data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]: # Note the return type
#         # Custom parsing logic for this dataset
#         # Example:
#         # custom_data: List[Dict[str, Any]] = statistical_data["SOME_OTHER_STRUCTURE"]["DATA"]
#         # return {"custom_table": custom_data}
#         raise NotImplementedError("Parsing for AnotherDatasetConfig not implemented yet.")
