import itertools
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, callback, dcc, html
from layout import page_main
from lib.utils import Page, get_full_path

title = 'Test API'
pages = [
    Page(module=page_main, url='', display='Home'),
]
content = html.Div(id="page-content", className="area-content")
location = dcc.Location(id="url")

dash_app = Dash(external_stylesheets=[dbc.themes.MATERIA], assets_folder=get_full_path('assets'))
dash_app.title = "Automated Unit Test Generation for Data-intensive Applications"
dash_app.layout = html.Div([
    location,
    content,
], className="app-container", style={"display":"inherit","text-align":"left"})
dash_app.validation_layout = html.Div(
    [
        location,
        content,
    ] + list(itertools.chain.from_iterable([page.module.content for page in pages]))
)
@callback(
    Output("page-content", "children"),
    Input("url", "pathname"))
def render_page_content(pathname):
    matched_page = next(filter(lambda page: pathname == '/' + page.url, pages), None)
    if matched_page is not None:
        return matched_page.module.content
    return dbc.Container(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

app = dash_app.server

if __name__ == "__main__":
    dash_app.run_server(debug=False)
