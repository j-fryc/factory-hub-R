from typing import Optional, Any

from pydantic import BaseModel


class MongoCriteriaFilter(BaseModel):
    query: dict


class MongoCriteriaFilterBuilder:
    def __init__(self):
        self._criteria: dict = {}

    def add_text_search(self, field_value: Optional[str]) -> None:
        if field_value:
            self._criteria["$text"] = {"$search": field_value}

    def add_exact_match(self, field_name: str, field_value: Any) -> None:
        if field_value is not None:
            self._criteria[field_name] = field_value

    def add_greater_than(self, field_name: str, field_value: Any) -> None:
        if field_value is not None:
            if field_name not in self._criteria:
                self._criteria[field_name] = {}
            self._criteria[field_name]["$gt"] = field_value

    def add_less_than(self, field_name: str, field_value: Any) -> None:
        if field_value is not None:
            if field_name not in self._criteria:
                self._criteria[field_name] = {}
            self._criteria[field_name]["$lt"] = field_value

    def add_nested_fields(self, parent_field: str, nested_object: Any) -> None:
        if nested_object and hasattr(nested_object, 'model_dump'):
            nested_data = nested_object.model_dump(exclude_defaults=True)
            for field_name, field_value in nested_data.items():
                if field_value is not None:
                    self._criteria[f"{parent_field}.{field_name}"] = field_value

    def build(self) -> MongoCriteriaFilter:
        return MongoCriteriaFilter(query=self._criteria)
