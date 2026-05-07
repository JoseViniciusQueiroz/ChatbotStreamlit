from renders.text import render_text
from renders.table import render_table
from renders.expander import render_expander
from renders.tabs import render_tabs


RENDERERS = {
    "text": render_text,
    "table": render_table,
    "expander": render_expander,
    "tabs": render_tabs 
}