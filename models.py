from dataclasses import dataclass, field
from typing import Any, Optional, Callable, Dict, List

@dataclass
class Uppgift:
    fraga: str
    ratt_svar: Any
    input_typ: str
    svarstyp: str
    layout: Optional[str] = None
    graf_funktion: Optional[Callable] = None
    losningsforslag: Optional[str] = None
    extra_data: Dict[str, Any] = field(default_factory=dict)
