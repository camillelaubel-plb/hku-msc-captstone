import logging
import sys
import traceback
import dash_bootstrap_components as dbc
from dash import Input, Output, callback, dash_table, dcc, html, ctx
from layout.style import TABLE_HEADER_STYLE, TABLE_ROW_STYLE, TABLE_STYLE, TABLE_CELL_STYLE
from lib import data_service
from flask import jsonify

_request_data = html.Div([
    html.Div([html.U('API Key'), html.Br(), dcc.Input(id='api_key', type='text', name="ApiKey", debounce=True, style={'width': '100%'}, value="AIzaSyBxS7SoWldz_rvMRY181ju4uNY-mFvwtEA")]), html.Br(),
    html.Div([html.U('Input Type'), html.Br(), dcc.Input(id='input_type', type='text', name="InputType", debounce=True, style={'width': '100%'})]), html.Br(),
    html.Div([html.U('Boundary'), html.Br(), dcc.Input(id='boundary', type='text', name="Boundary", debounce=True, style={'width': '100%'})]), html.Br(),
    html.Div([html.U('Expected Output'), html.Br(), dcc.Input(id='expected_output', type='text', name="ExpectedOutput", debounce=True, style={'width': '100%'})]), html.Br(),
    html.Div([html.U('Code'), html.Br(), dcc.Textarea(id='code', style={'width': '100%', 'height': 300})]), html.Br(),
    html.Div([dbc.Button("Submit", id='btn_submit', size="sm", n_clicks=0, color="secondary"), html.Div([html.Br(), html.I('(Submitting... Please wait.)', style={'color':'orange'})], id='div_loading')]), html.Br(),
])

_error_msg = html.B('', id='error_msg', style={'color': 'red'})
_validation_result_cols = [{'col_cfg': {'id': 'validation_result', 'name': '', 'type': 'text'}},]
_validation_result = dash_table.DataTable(
    id='table_validation_result', columns=[x['col_cfg'] for x in _validation_result_cols],
    style_as_list_view=False, sort_action="native", sort_mode="single", style_header=TABLE_HEADER_STYLE, style_table=TABLE_STYLE, style_data_conditional=TABLE_ROW_STYLE, style_cell=TABLE_CELL_STYLE, page_size=30, is_focused=True,
)
_sample_data_cols = [{'col_cfg': {'id': 'sample_data', 'name': '', 'type': 'text'}},]
_sample_data = dash_table.DataTable(
    id='table_sample_data', columns=[x['col_cfg'] for x in _sample_data_cols],
    style_as_list_view=False, sort_action="native", sort_mode="single", style_header=TABLE_HEADER_STYLE, style_table=TABLE_STYLE, style_data_conditional=TABLE_ROW_STYLE, style_cell=TABLE_CELL_STYLE, page_size=30, is_focused=True,
)
_suggestions_cols = [{'col_cfg': {'id': 'suggestion', 'name': '', 'type': 'text'}}]
_suggestions = dash_table.DataTable(
    id='table_suggestions', columns=[x['col_cfg'] for x in _suggestions_cols],
    style_as_list_view=False, sort_action="native", sort_mode="single", style_header=TABLE_HEADER_STYLE, style_table=TABLE_STYLE, style_data_conditional=TABLE_ROW_STYLE, style_cell=TABLE_CELL_STYLE, page_size=30, is_focused=True,
)
_metrics_cols = [
    {'col_cfg': {'id': 'execution_time', 'name': 'Execution Time', 'type': 'text'}},
    {'col_cfg': {'id': 'memory_usage', 'name': 'Memory Usage', 'type': 'text'}},
]
_metrics = dash_table.DataTable(
    id='table_metrics', columns=[x['col_cfg'] for x in _metrics_cols],
    style_as_list_view=False, sort_action="native", sort_mode="single", style_header=TABLE_HEADER_STYLE, style_table=TABLE_STYLE, style_data_conditional=TABLE_ROW_STYLE, style_cell=TABLE_CELL_STYLE, page_size=30, is_focused=True,
)
_coverage_cols = [
    {'col_cfg': {'id': 'test_suite', 'name': 'Test Suite', 'type': 'text'}},
    {'col_cfg': {'id': 'coverage', 'name': 'Coverage', 'type': 'text'}}
]
_coverage = dash_table.DataTable(
    id='table_coverage', columns=[x['col_cfg'] for x in _coverage_cols],
    style_as_list_view=False, sort_action="native", sort_mode="single", style_header=TABLE_HEADER_STYLE, style_table=TABLE_STYLE, style_data_conditional=TABLE_ROW_STYLE, style_cell=TABLE_CELL_STYLE, page_size=30, is_focused=True,
)
_tests_cols = [{'col_cfg': {'id': 'test', 'name': '', 'type': 'text'}}]
_passed_tests = dash_table.DataTable(
    id='table_passed_tests', columns=[x['col_cfg'] for x in _tests_cols],
    style_as_list_view=False, sort_action="native", sort_mode="single", style_header=TABLE_HEADER_STYLE, style_table=TABLE_STYLE, style_data_conditional=TABLE_ROW_STYLE, style_cell=TABLE_CELL_STYLE, page_size=30, is_focused=True,
)
_failed_tests = dash_table.DataTable(
    id='table_failed_tests', columns=[x['col_cfg'] for x in _tests_cols],
    style_as_list_view=False, sort_action="native", sort_mode="single", style_header=TABLE_HEADER_STYLE, style_table=TABLE_STYLE, style_data_conditional=TABLE_ROW_STYLE, style_cell=TABLE_CELL_STYLE, page_size=30, is_focused=True,
)

_response_data = html.Div([
    html.Div([_error_msg]), html.Br(),
    html.Div([html.U('Sample Data'), html.Br(), _sample_data]), html.Br(),
    html.Div([html.U('Validation Result'), html.Br(), _validation_result]), html.Br(),
    html.Div([html.U('Passed Tests'), html.Br(), _passed_tests]), html.Br(),
    html.Div([html.U('Failed Tests'), html.Br(), _failed_tests]), html.Br(),
    html.Div([html.U('Metrics'), html.Br(), _metrics, html.Br(), _coverage]), html.Br(),
    html.Div([html.U('Suggestions'), html.Br(), _suggestions]), html.Br(),
])

_main_div = html.Div([
    _request_data,
    html.Hr(), html.Br(),
    html.H1(html.U("Result")), html.Br(),
    _response_data,
])

_interval = dcc.Interval(id='refresh_submit_btn_display_interval', interval=500, n_intervals=0)
_is_submitting = False
_btn_submit_count = 0
@callback(
    Output("error_msg", 'children'),
    Output('table_validation_result', 'data'),
    Output('table_sample_data', 'data'),
    Output('table_suggestions', 'data'),
    Output('table_metrics', 'data'),
    Output('table_coverage', 'data'),
    Output('table_passed_tests', 'data'),
    Output('table_failed_tests', 'data'),
    Input('api_key', 'value'),
    Input('code', 'value'),
    Input('input_type', 'value'),
    Input('boundary', 'value'),
    Input('expected_output', 'value'),
    Input('btn_submit', 'n_clicks')
)
def button_clicked(api_key, code, input_type, boundary, expected_output, btn_submit):
    global _is_submitting
    global _btn_submit_count
    if btn_submit != _btn_submit_count:
        _is_submitting = True
        _btn_submit_count = btn_submit
        try:
            (is_success, json_rsp_data) = data_service.submit_request(api_key, code, input_type, boundary, expected_output)
            _is_submitting = False
            if is_success:
                validation_result = _parse_validation_result(json_rsp_data["validation_result"])
                sample_data = _parse_sample_data(json_rsp_data["sample_data"])
                suggestions = _parse_suggestions(json_rsp_data["suggestions"])
                metrics = _parse_metrics(json_rsp_data["metrics"])
                coverage = _parse_coverage(json_rsp_data["metrics"]["coverage"], json_rsp_data["test_suite"])
                passed_tests = _parse_tests(json_rsp_data["unit_tests"]["passed_tests"])
                failed_tests = _parse_tests(json_rsp_data["unit_tests"]["failed_tests"])
                return None, validation_result, sample_data, suggestions, metrics, coverage, passed_tests, failed_tests
            else:
                if "error" in json_rsp_data:
                    error_msg = "[Error] " + json_rsp_data["error"]
                    if "details" in json_rsp_data:
                        error_msg += " " + json_rsp_data["details"]
                else:
                    error_msg = "[Error] " + str(json_rsp_data)
                return error_msg, None, None, None, None, None, None, None
        except:
            _is_submitting = False
            error_msg = str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1])
            return error_msg, None, None, None, None, None, None, None
    return None, None, None, None, None, None, None, None
@callback(
    Output("btn_submit", 'disabled'),
    Output("div_loading", 'style'),
    Input('refresh_submit_btn_display_interval', 'n_intervals'),
)
def _on_time_interval(_n_intervals):
    global _is_submitting
    if _is_submitting:
        return True, {"display": "block"}
    else:
        return False, {"display": "none"}

def _parse_validation_result(data):
    result = []
    row = {}
    row["validation_result"] = data
    result.append(row)
    return result
def _parse_test_suite(data):
    result = []
    row = {}
    row["test_suite"] = data
    result.append(row)
    return result
def _parse_sample_data(data):
    result = []
    for d in data:
        sample_data = ""
        if isinstance(d, dict):
            for k, v in d.items():
                sample_data = sample_data + k + ": " + str(v) + "\n"
        else:
            sample_data = str(d) + "\n"
        row = {}
        row["sample_data"] = sample_data
        result.append(row)
    return result
def _parse_suggestions(data):
    result = []
    for d in data:
        row = {}
        row["suggestion"] = d
        result.append(row)
    result.reverse()
    return result
def _parse_metrics(data):
    result = []
    row = {}
    row["execution_time"] = f"{round(data['execution_time'], 4)} Seconds"
    row["memory_usage"] = f"{data['memory_usage']} KB"
    result.append(row)
    return result
def _parse_coverage(coverage, test_suite):
    result = []
    row = {}
    line_count = test_suite.count("\n")
    test_suite_line_num_added = "  1.   " + test_suite
    for i in range(line_count):
        num = str(i + 2)
        if len(num) == 1:
            num = "  " + num
        elif len(num) == 2:
            num = " " + num
        test_suite_line_num_added = nth_repl(test_suite_line_num_added, "\n", f"\n{num}.   ", i+1)
    row["coverage"] = coverage
    row["test_suite"] = test_suite_line_num_added
    result.append(row)
    return result
def _parse_tests(data):
    result = []
    for d in data:
        row = {}
        row["test"] = d
        result.append(row)
    return result

def nth_repl(s, sub, repl, n):
    find = s.find(sub)
    # If find is not -1 we have found at least one match for the substring
    i = find != -1
    # loop util we find the nth or we find no match
    while find != -1 and i != n:
        # find + 1 means we start searching from after the last match
        find = s.find(sub, find + 1)
        i += 1
    # If i is equal to n we found nth match so replace
    if i == n:
        return s[:find] + repl + s[find+len(sub):]
    return s

content = [_interval, _main_div]
