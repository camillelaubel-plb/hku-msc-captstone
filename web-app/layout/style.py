RADIO_BTN = {
    "margin-left": "0px",
    "margin-right": "5px",
    "margin-top": "2px",
    "margin-bottom": "2px",
    'display':'inline-block'
}
LEFT_PANEL = {
    "padding-right": "20px",
    'display':'inline-block',
    "vertical-align": "top",
    "text-align":"left",
    "max-width": "220px"
}
RIGHT_PANEL = {
    'display':'inline-block',
    "vertical-align": "top",
    "text-align":"left",
    "max-width": "870px"
}
DIV_INLINE = {
    "padding-right": "20px",
    "padding-bottom": "20px",
    'display':'inline-block',
    "vertical-align": "top",
    "text-align":"left",
}
DIV_BLOCK = {
    "padding-right": "20px",
    'display': 'block',
    "vertical-align": "top",
}

TABLE_STYLE = {
    'fontSize': '12px',
}

TABLE_HEADER_STYLE = {
    'backgroundColor': '#006c9a',
    'fontWeight': 'bold',
    'color': 'white',
    'textAlign': 'left',
    'padding': '5px',
    'border': '1px solid lightgrey',
}

TABLE_ROW_STYLE = [
    {
        'textAlign': 'left',
        'padding': '5px',
        'border': '1px solid lightgrey',
    },
    {
        "if": {"state": "selected"},
        "backgroundColor": "inherit !important",
        #"border": "inherit !important"
    }
]

TABLE_CELL_STYLE = {
    "vertical-align": "top",
    "whiteSpace": "pre-wrap",
    'textAlign': 'left',
    'minWidth': 0,
    "word-wrap": "normal",
    "max-width":"600px",
    'backgroundColor': '#FFFFFF'
}