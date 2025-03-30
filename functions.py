# Link to published dashboard: https://fifa-world-cup-dashboard-15d7.onrender.com/
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv("world_cup_data.csv")
wins = df['Winner'].value_counts().reset_index()
wins.columns = ['country', 'wins']
runnerups = df['Runner-up'].value_counts().reset_index()
runnerups.columns = ['country', 'runnerups']
country_stats = pd.merge(wins, runnerups, on='country', how='outer').fillna(0)

country_codes = {
    'Brazil': 'BRA',
    'Germany': 'DEU',
    'Italy': 'ITA',
    'Argentina': 'ARG',
    'Uruguay': 'URY',
    'France': 'FRA',
    'England': 'GBR',
    'Spain': 'ESP',
    'Netherlands': 'NLD',
    'Sweden': 'SWE',
    'Croatia': 'HRV',
    'Czechoslovakia': 'CZE',
    'Hungary': 'HUN'
}

country_stats['iso_alpha'] = country_stats['country'].map(country_codes)

fig = px.choropleth(
    country_stats,
    locations = 'iso_alpha',
    color = 'wins',
    hover_name = 'country',
    color_continuous_scale = px.colors.sequential.Plasma,
    title = 'FIFA World Cup Wins by Country'
)

app = dash.Dash(__name__)
server = app.server
app.title = "FIFA World Cup Dashboard"

app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard"),
    dcc.Graph(id = 'world-cup-map', figure = fig),
    html.Div([
        html.H3("Countries that have ever won a World Cup:"),
        html.Ul([html.Li(country) for country in sorted(wins['country'])]),
    ]),

    html.Div([
        html.H3("Select a country to view its number of World Cup titles:"),
        dcc.Dropdown(
            id = 'country-dropdown',
            options = [{'label': c, 'value': c} for c in sorted(wins['country'])],
            value = 'Brazil'
        ),
        html.Div(id = 'country-wins-output')
    ], style = {'margin-top': '20px'}),

    html.Div([
        html.H3("Select a year to see its final match details:"),
        dcc.Dropdown(
            id = 'year-dropdown',
            options=[{'label': str(y), 'value': y} for y in sorted(df['Year'])],
            value=1930
        ),
        html.Div(id = 'year-final-output')
    ], style = {'margin-top': '20px'})
], style = {'backgroundColor': 'white', 'color': 'black', 'padding': '20px'})

@app.callback(
    Output('country-wins-output', 'children'),
    [Input('country-dropdown', 'value')]
)
def update_country_wins(selected_country):
    row = wins[wins['country'] == selected_country]
    if not row.empty:
        count = row['wins'].values[0]
        return f"{selected_country} has won the World Cup {int(count)} time(s)."
    else:
        return f"{selected_country} has never won the World Cup."

@app.callback(
    Output('year-final-output', 'children'),
    [Input('year-dropdown', 'value')]
)
def update_year_final(selected_year):
    row = df[df['Year'] == selected_year]
    if not row.empty:
        winner = row['Winner'].values[0]
        runner_up = row['Runner-up'].values[0]
        return (f"In {selected_year}, {winner} won the World Cup, "
                f"with {runner_up} as the runner-up.")
    else:
        return "No data for that year."

if __name__ == '__main__':
    app.run(debug = True)
