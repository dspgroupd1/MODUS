# Import required libraries
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)
import dash
import plotly.express as px
from dash.dependencies import Input, Output
from reddit_toolbox import *
from reddit import *
from drugsforum import *
from dash import dcc, html
import dash_dangerously_set_inner_html


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "NPS Monitoring Dashboard"
server = app.server

#NPS options for dropwdown
nps_type_options = ['1B-LSD', '1D-LSD', '1P-LSD', '1V-LSD', '1CP-AL-LAD', '1CP-LSD', '1CP-MIPLA', '2+3-FEA', '2-CB', '2-FA', '2-FEA', '2-FMA', '2-FPM', '2-MMC', '2C-B-FLY', '2C-C', '2C-D', '2C-E', '2C-E-NBOME', '2F-DCK', '2F-KETAMINE', '3-CEC', '3-CMC', '3-CPM', '3-FA', '3-FEA', '3-FMA', '3-FPM', '3-HO-PCE', '3-HO-PCP', '3-MEC', '3-MEO-PCE', '3-MMA', '3-MMC', '3-ME-PCE', '3-ME-PCP', '3-ME-PCPY', '3-MEO-PCP', '3.4-DMMC', '3D-MXE', '4-ACO-MET', '4-ACO-DET', '4-ACO-DPT', '4-ACO-MIPT', '4-CDC', '4-CEC', '4-CL-PVP', '4-CMC', '4-EMC', '4-FMPH', '4-HO-DET', '4-HO-DPT', '4-HO-EPT', '4-HO-MALT', '4-HO-MET', '4-HO-MIPT', '4-HO-MCPT', '4-ME-MABP', '4-MEC', '4-MPD', '4-MPM', '4B-MAR', '4C-MAR', '4F-MAR', '4F-MPH', '4F-METHYLFENIDAAT', '4F-RITALIN', '4FMA', '5-APB', '5-BR-DMT', '5-BROMO-DMT', '5-DBFPV', '5-EAPB', '5-HTP', '5-MAPB', '5-MEO-DALT', '5-MEO-DIPT', '5-MEO-MIPT', '5-MMPA', '5-MEO-DMT', '5-MEO-MET', '5-METHYLETHYLONE', '5BR-ADB-INACA', '5F-ADB', '5F-PCN', '5F-SGT-151', '6-APB', '6-CL-ADB-A', '6-CL-ADBA', '7-ABF', '7-ADD', 'A-PCYP', 'A-PHP', 'A-PIHP', 'ADB', 'ADB-BUTINACA', 'AL-LAD', 'ALD-52', 'AMT', 'BB-8', 'BK-2C-B', 'BK-BBDP', 'BK-EBDP', 'BOH-2C-B', 'BROMAZOLAM', 'BROMONORDIAZEPAM', 'CBD', 'CLONAZOLAM', 'DC-C', 'DC-TROPA-MIX', 'DCK', 'DESOXY-MDA', 'DESOXY-MDMA', 'DHM', 'DMC', 'DMXE', 'DOC', 'DPT', 'DESCHCLOROKETAMINE', 'DESCHLOROKETAMINE', 'DESCHLOROETIZOLAM', 'DICLAZEPAM', 'ED-DB', 'EPT', 'ETH-LAD', 'ETHYL-HEX', 'ETHYL-PENTEDRONE', 'ETIZOLAM', 'FLUALPRAZOLAM', 'FLUBROMAZEPAM', 'FLUBROMAZOLAM', 'FLUBROTIZOLAM', 'FLUETIZOLAM', 'FLUNITRAZOLAM', 'FLUOREXETAMINE', 'GW-0742', 'GW-501516', 'GIDAZEPAM', 'HEP', 'HEX-EN', 'HXE', 'IDRA-21', 'JWH-210', 'L-THEANINE', 'LGD-4033', 'LSD', 'LSZ', 'MD-PHP', 'MDPHP', 'MEAI', 'MET', 'MF-PVP', 'MK-2866', 'MK-677', 'MXPR', 'MXIPR', 'MEPHEDRENE', 'METHALLYLESCALINE', 'N-ETHYL-HEXEDRONE', 'N-ETHYLHEXEDRONE', 'NB-5-MEO-DALT', 'NB-5-MEO-MIPT', 'NDH', 'NEP', 'NORFLURAZEPAM', 'O-DSMT', 'O-PCE', 'PHENIBUT', 'PHOSPHATIDYLSERINE', 'PYRAZOLAM', 'RAD-140', 'RAD-150', 'RIBOFLAVINE', 'S-23', 'S-4', 'SGT-152', 'SR-9009', 'SR-9011', 'SULBUTIAMINE', 'SYNTHACAINE', 'THC-C4', 'TRYPTAMINE', 'VINPOCETINE', 'YK-11', 'A-D2PV', 'BK-MDDMA', 'Α-PIHP', 'ΒOH-2C-B']

#Create pie chart at launch
data_pie = get_current_max_chart_data(nps_df, count=10)
fig_pie_chart = px.pie(data_pie, values='values', names='labels', title="% of the total views on Drugsforum")


# Create app layout
app.layout = html.Div(
    [dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        #header
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("uvalogo2.png"),
                            id="plotly-image",
                            style={
                                "height": "100px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        ),
                        html.Img(
                            src=app.get_asset_url("logo-politie.png"),
                            id="plotly-image1",
                            style={
                                "height": "100px",
                                "width": "200px",
                                "margin-bottom": "25px",
                            },
                        ),
                        html.Img(
                            src=app.get_asset_url("logo-4nps.png"),
                            id="plotly-image2",
                            style={"height": "100px", "width": "200px","margin-bottom": "20px", 'position': 'absolute', 'float': 'right', 'right': 0},
                        ),
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "NPS Monitoring Dashboard",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Group D1", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),

        #filters
        html.Div(
            [
                html.Div(
                    [

                        html.P(["This dashboard gives the opportunity to research the popularity of any drug of interest on drugsforum.nl and Reddit. As popularity indicators, respectively the number of views and number of mentions are used for Reddit and Drugsforum. In order to search for a specific drug of interest; use the dropdown menu on the left (NPS that currently are being sold on vendor webshops) or type in the name of drug in the search box.  It is possible to select a specific time range of interest.  A flagging system of new popular upcoming NPS is presented based on the popularity indicator of drugsforum.nl.", html.Br(), html.B('Note: '), 'The dashboard will take a few seconds to load.']),
                        html.P(
                            "Filter by year:",
                            className="control_label",
                        ),

                        dcc.RangeSlider(id = 'range_slider',
                            min=2008,
                            max=2022,
                            step=1,
                            marks={
                                2008: '2008',
                                2010: '2010',
                                2012: '2012',
                                2014: '2014',
                                2016: '2016',
                                2018: '2018',
                                2020: '2020',
                                2022: '2022',
                            },
                            value=[2008,2022]
                        ),

                        html.Div(id='selected_time_range'),


                        html.P("Select your NPS of interest:", className="control_label"),
                        dcc.Dropdown(
                                id='dropdown',
                                options=[{'label': x, 'value': x} for x in nps_type_options],
                                value= None
                            ),

                        html.Div(id='selected_value_dropdown'),

                        html.Center(html.H4("OR", className="control_label")),

                        html.P("Search for the NPS of interest:", className="control_label"),
                        dcc.Input(id="input1", type="text", placeholder="Enter the name of the NPS", size = '45', debounce=True),
                        html.Div(id='search_value_textfield'),

                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                #create info boxes
                html.Div(
                    [
                        html.Div(
                            [
                               html.Div(
                                  [html.H6(id="top5nps"), html.P([html.B("Top 5 popular NPS")]), dash_dangerously_set_inner_html.DangerouslySetInnerHTML(get_current_max_nps_string(nps_df, count=5, days=90, metric='views'))],
                                    id="top5nps_box",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="top5risers"), html.P([html.B("Top 5 rising NPS")]), dash_dangerously_set_inner_html.DangerouslySetInnerHTML(get_increasing_nps(nps_df, piecewise_df))],
                                    id="top5risers_box",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="totalviews"), html.P([html.B("Total views on Drugsforum")]), html.P(get_total_views_nps(nps_df))],
                                    id="totalviews_box",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="Top5newoccurring"), html.P([html.B("Top 5 newly occurring NPS")]), dash_dangerously_set_inner_html.DangerouslySetInnerHTML(get_newly_occurring_nps(nps_df, count = 5, days = 90))],
                                    id="top5new",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [dcc.Graph(id="count_graph", figure = fig_pie_chart, style={"width": '90vh', 'height': '50vh', 'top': '0px', 'right': '0px', 'position': 'static'})],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
           ],
             className="row flex-display",
        ),

        #create graphs
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id = "drugsforum_graph", style={'width': '170vh'})],
                    className="pretty_container seven columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="reddit_graph", style={'width': '170vh'})],
                    className="pretty_container seven columns",
                ),
            ],
            className="row flex-display",
        ),

        html.Div(style={'background-color': '#eee', 'padding': '10px'}, children=[
            html.Div(style={'text-align': 'center'}, children= html.A('Visit our Github for more details (code, report etc.) on this project ', href='https://github.com/dspgroupd1/MODUS'))
        ])

    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},

)


#-------------------------------
#CALLBACKS
#preview value dropdown
@app.callback(
    Output("selected_value_dropdown", "children"),
    [Input("dropdown", "value")]
)
def print_value_selector(selected_value):
        return f'You have selected: {selected_value}'

#preview value of searchfield
@app.callback(
    Output("search_value_textfield", "children"),
    [Input("input1", "value")]
)
def print_value_textfield(search_value):
        return f'You have searched for: {search_value}'

#preview selected time range yearslider
@app.callback(
    Output('selected_time_range', 'children'),
    [Input('range_slider', 'value')])
def update_output(value):
    return 'You have selected {}'.format(value)

#update main graphs with input from searchfield/selector and yearslider
@app.callback(
    [Output("drugsforum_graph", "figure"), Output("reddit_graph", "figure")],
    [Input('range_slider', 'value'), Input("input1", "value"),Input("dropdown", "value")])
def update_graph(input_range_slider, input_searchfield, input_dropdown):
    begin_year = input_range_slider[0]
    end_year = input_range_slider[1]
    if input_searchfield:
        print(input_searchfield, begin_year, end_year)
        df_drugsforum = search_drug_drugsforum(input_searchfield, begin_year, end_year)
        df_reddit = search_drug_reddit(input_searchfield, begin_year, end_year)
    elif input_dropdown:
        print(input_dropdown, begin_year, end_year)
        df_drugsforum = search_drug_drugsforum(input_dropdown, begin_year, end_year)
        df_reddit = search_drug_reddit(input_dropdown, begin_year, end_year)
    else:
        print("Please provide input either from textfield or dropdown")

    fig_drugsforum= px.line(df_drugsforum, x="month-year", y="moving-avg-views", labels={
                     "month-year": "time",
                     "moving-avg-views": "Number of views"}, title='Number of views on drugsforum.nl')
    fig_reddit = px.line(df_reddit, x="year_month", y="moving-avg-mentions", labels = {"month-year": "time",
                     "moving-avg-mentions": "Number of mentions"}, title='Number of mentions on Reddit')
    return fig_drugsforum, fig_reddit

# Main
if __name__ == "__main__":
    app.run_server(debug=False)
