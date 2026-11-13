from dataclasses import dataclass, field
from typing import Any, List, Optional

@dataclass
class Uppgift:
    fraga: str
    ratt_svar: Any
    input_typ: str = "text"          # "text", "flera_text", "radio", "selectbox"
    svarstyp: str = "float"          # "int", "float", "procent", "string", "string_math", "ekvation_x", "ekvation_linje", "array_float", "ekvationssystem", "punkt", "ordered_float", "faktoriserad"
    info_text: Optional[str] = None
    latex_text: Optional[str] = None
    info_box_text: Optional[str] = None
    info_box_style: Optional[str] = None
    plotly_fig: Optional[Any] = None
    alternativ: List[str] = field(default_factory=list)
    suffix: Optional[str] = None
    undertext: Optional[str] = None
    visnings_kategori: Optional[str] = None
    flera_labels: List[str] = field(default_factory=list)
    tolerans: float = 0.02
    krav_inga_parenteser: bool = False
