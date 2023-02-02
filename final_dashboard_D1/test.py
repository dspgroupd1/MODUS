import dash
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div(style={'background-color': '#eee', 'padding': '10px'}, children=[
            html.Div(html.Img(
                            src=app.get_asset_url("logo-4nps.png"),
                            id="plotly-image2",
                            style={"height": "100px", "width": "200px","margin-bottom": "20px", 'float': 'right', 'right': 0},
                        ))])

if __name__ == '__main__':
    app.run_server(debug=True)