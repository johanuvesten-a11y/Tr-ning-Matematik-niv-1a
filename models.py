from dataclasses import dataclass, field
from typing import Optional, Any, Callable, Dict


@dataclass
class Uppgift:
    fraga: str
    ratt_svar: Any
    input_typ: str
    svarstyp: str
    visnings_kategori: str = ""

    # Valfria fält (UI & Layout)
    info_text: Optional[str] = None
    latex_text: Optional[str] = None
    info_box_text: Optional[str] = None
    info_box_style: Optional[str] = None
    info_text_italic: Optional[str] = None
    undertext: Optional[str] = None
    html_table: Optional[str] = None
    layout: Optional[str] = None
    losningsforslag: Optional[str] = None

    # Valfria fält (Graf & Plotly)
    graf_f: Optional[Callable] = None
    graf_funktion: Optional[Callable] = None
    q_type_vis: str = "vis_none"
    trace_x: Optional[float] = None
    trace_y: Optional[float] = None
    trace_alla_x: Optional[list] = None
    plotly_fig: Optional[Any] = None

    # Valfria fält (Alternativ och speciell rättning)
    alternativ: Optional[list] = None
    ratt_svar_lista: Optional[list] = None
    ratt_svar_visning: Optional[str] = None
    suffix: Optional[str] = None
    extra_data: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.graf_f is None and self.graf_funktion is not None:
            self.graf_f = self.graf_funktion

        for key in (
            "info_text",
            "latex_text",
            "info_box_text",
            "info_box_style",
            "info_text_italic",
            "undertext",
            "html_table",
            "q_type_vis",
            "trace_x",
            "trace_y",
            "trace_alla_x",
            "alternativ",
            "suffix",
        ):
            if key in self.extra_data and getattr(self, key) in (None, "vis_none"):
                setattr(self, key, self.extra_data[key])
