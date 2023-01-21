# Import required libraries
import dash
import pandas as pd
import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "NPS Monitoring Dashboard"
server = app.server

#NPS options for dropwdown
nps_type_options = ['1B-LSD', '1D-LSD', '1P-LSD', '1V-LSD', '1CP-AL-LAD', '1CP-LSD', '1CP-MIPLA', '2+3-FEA', '2-CB', '2-FA', '2-FDCK', '2-FEA', '2-FMA', '2-FPM', '2-MMC', '2/3-FEA', '2C-B-FLY', '2C-C', '2C-D', '2C-E', '2C-E-NBOME', '2F-DCK', '2F-KETAMINE', '3-CEC', '3-CMC', '3-CPM', '3-FA', '3-FEA', '3-FMA', '3-FPM', '3-HO-PCE', '3-HO-PCP', '3-MEC', '3-MEO-PCE', '3-MMA', '3-MMC', '3-ME-PCE', '3-ME-PCP', '3-ME-PCPY', '3-MEO-PCP', '3.4-DMMC', '3D-MXE', '4-ACO-MET', '4-ACO-DET', '4-ACO-DPT', '4-ACO-MIPT', '4-CDC', '4-CEC', '4-CL-PVP', '4-CMC', '4-EMC', '4-FMA', '4-FMPH', '4-HO-DET', '4-HO-DPT', '4-HO-EPT', '4-HO-MALT', '4-HO-MET', '4-HO-MIPT', '4-HO-MCPT', '4-ME-MABP', '4-MEC', '4-MPD', '4-MPM', '4B-MAR', '4C-MAR', '4F-MAR', '4F-MPH', '4F-METHYLFENIDAAT', '4F-RITALIN', '4FMA', '5-APB', '5-BR-DMT', '5-BROMO-DMT', '5-DBFPV', '5-EAPB', '5-HTP', '5-MAPB', '5-MEO-DALT', '5-MEO-DIPT', '5-MEO-MIPT', '5-MMPA', '5-MEO-DMT', '5-MEO-MET', '5-METHYLETHYLONE', '5BR-ADB-INACA', '5F-ADB', '5F-PCN', '5F-SGT-151', '6-APB', '6-CL-ADB-A', '6-CL-ADBA', '7-ABF', '7-ADD', 'A-PCYP', 'A-PHP', 'A-PIHP', 'ADB', 'ADB-BUTINACA', 'AL-LAD', 'ALD-52', 'AMT', 'BB-8', 'BK-2C-B', 'BK-BBDP', 'BK-EBDP', 'BOH-2C-B', 'BROMAZOLAM', 'BROMONORDIAZEPAM', 'CBD', 'CLONAZOLAM', 'DC-C', 'DC-TROPA-MIX', 'DCK', 'DESOXY-MDA', 'DESOXY-MDMA', 'DHM', 'DMC', 'DMXE', 'DOC', 'DPT', 'DESCHCLOROKETAMINE', 'DESCHLOROKETAMINE', 'DESCHLOROETIZOLAM', 'DICLAZEPAM', 'ED-DB', 'EPT', 'ETH-LAD', 'ETHYL-HEX', 'ETHYL-PENTEDRONE', 'ETIZOLAM', 'FLUALPRAZOLAM', 'FLUBROMAZEPAM', 'FLUBROMAZOLAM', 'FLUBROTIZOLAM', 'FLUETIZOLAM', 'FLUNITRAZOLAM', 'FLUOREXETAMINE', 'GW-0742', 'GW-501516', 'GIDAZEPAM', 'HEP', 'HEX-EN', 'HXE', 'IDRA-21', 'JWH-210', 'L-THEANINE', 'LGD-4033', 'LSD', 'LSZ', 'MD-PHP', 'MDPHP', 'MEAI', 'MET', 'MF-PVP', 'MK-2866', 'MK-677', 'MXPR', 'MXIPR', 'MEPHEDRENE', 'METHALLYLESCALINE', 'N-ETHYL-HEXEDRONE', 'N-ETHYLHEXEDRONE', 'NB-5-MEO-DALT', 'NB-5-MEO-MIPT', 'NDH', 'NEP', 'NORFLURAZEPAM', 'O-DSMT', 'O-PCE', 'PHENIBUT', 'PHOSPHATIDYLSERINE', 'PYRAZOLAM', 'RAD-140', 'RAD-150', 'RIBOFLAVINE', 'S-23', 'S-4', 'SGT-152', 'SR-9009', 'SR-9011', 'SULBUTIAMINE', 'SYNTHACAINE', 'THC-C4', 'TRYPTAMINE', 'VINPOCETINE', 'YK-11', 'A-D2PV', 'BK-MDDMA', 'Α-PIHP', 'ΒOH-2C-B']

# Load data
df = pd.read_csv("data/3mmc-data.csv")

# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
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
                        )
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
             ],
             className="row flex-display",
        ),

        #grafieken
        html.Div(
            [
                html.Div(
                    # dcc.Graph(id = "test_graph", figure=fig_test),
                    dcc.Graph(id = "test_graph"),
                ),
                html.Div(
                    [dcc.Graph(id="test_graph1")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="test_graph2")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="test_graph3")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

#-------------------------------
#Helper functions
# def filter_dataframe(df, well_statuses, well_types, year_slider):
#     dff = df[
#         df["Well_Status"].isin(well_statuses)
#         & df["Well_Type"].isin(well_types)
#         & (df["Date_Well_Completed"] > dt.datetime(year_slider[0], 1, 1))
#         & (df["Date_Well_Completed"] < dt.datetime(year_slider[1], 1, 1))
#     ]
#     return dff

#-------------------------------
#CALLBACKS
#dropdown
@app.callback(
    Output("selected_value_dropdown", "children"),
    [Input("dropdown", "value")]
)
def print_value_selector(selected_value):
        return f'You have selected: {selected_value}'

#searchfield
@app.callback(
    Output("search_value_textfield", "children"),
    [Input("input1", "value")]
)
def print_value_textfield(search_value):
        return f'You have searched for: {search_value}'

#yearslider
@app.callback(
    Output('selected_time_range', 'children'),
    [Input('range_slider', 'value')])
def update_output(value):
    return 'You have selected {}'.format(value)

#graph -> add selector as input / add or function between search field and selector (if another value is selected set the other one to none
@app.callback(
    [Output("test_graph", "figure"), Output("test_graph1", "figure"), Output("test_graph2", "figure"), Output("test_graph3", "figure")],
    [Input('range_slider', 'value'), Input("input1", "value")])
def update_graph(input_range_slider, input_searchfield):
    print("min:", input_range_slider[0], "max:", input_range_slider[1], "search field:", input_searchfield)
    #create corresponding dataframes (df1,df2,df3,df4)
    fig_test = px.line(df, x="month-year", y="moving-avg-views", title='Popularity')
    fig_test1 = px.bar(df, x="month-year", y="moving-avg-views", title='Popularity1')
    fig_test2 = px.scatter(df, x="month-year", y="moving-avg-views", title='Popularity2')
    fig_test3 = px.line(df, x="month-year", y="moving-avg-views", title='Popularity3')
    return fig_test, fig_test1, fig_test2, fig_test3


# Main
if __name__ == "__main__":
    app.run_server(debug=True)