import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

# Load the data
df = pd.read_csv('Facebook Metrics of Cosmetic Brand.csv')

# Convert 'Post Weekday' to actual day names
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df['Weekday'] = df['Post Weekday'].apply(lambda x: days[x-1])

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Custom CSS for styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background-color: #1e2642;
                color: white;
                font-family: Arial, sans-serif;
            }
            .card {
                background-color: #2a3356;
                border: none;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .card-title {
                color: white;
                font-size: 0.9rem;
                font-weight: bold;
                text-transform: uppercase;
            }
            .card-text {
                font-size: 2rem;
                font-weight: bold;
                color: white;
            }
            h1 {
                font-size: 2rem;
                color: white;
                margin-bottom: 20px;
                text-align: center;
                font-weight: bold;
            }
            .positive-change {
                color: #4cd964;
                font-size: 0.9rem;
            }
            .negative-change {
                color: #ff3b30;
                font-size: 0.9rem;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Define the layout
app.layout = dbc.Container([
    html.H1("Facebook Ad Performance Dashboard", className="mt-4 mb-4"),
    
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='time-frame-dropdown',
                options=[
                    {'label': 'All Time', 'value': 'all'},
                    {'label': 'Last 7 Days', 'value': 'week'},
                    {'label': 'Last 30 Days', 'value': 'month'}
                ],
                value='all',
                clearable=False,
                style={'width': '200px', 'color': 'black'}
            )
        ])
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Reach", className="card-title"),
                    html.P(id="total-reach", className="card-text"),
                    html.P(id="reach-change", className="positive-change")
                ])
            ])
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Engagement", className="card-title"),
                    html.P(id="total-engagement", className="card-text"),
                    html.P(id="engagement-change", className="positive-change")
                ])
            ])
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Avg. Engagement Rate", className="card-title"),
                    html.P(id="avg-engagement-rate", className="card-text"),
                    html.P(id="rate-change", className="positive-change")
                ])
            ])
        ])
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='interactions-by-type')
                ])
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='engagement-by-weekday')
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='reach-vs-engagement')
                ])
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='engagement-by-hour')
                ])
            ])
        ], width=6)
    ])
], fluid=True, style={'backgroundColor': '#1e2642', 'minHeight': '100vh'})

# Define callback to update all components
@app.callback(
    [Output('total-reach', 'children'),
     Output('total-engagement', 'children'),
     Output('avg-engagement-rate', 'children'),
     Output('reach-change', 'children'),
     Output('engagement-change', 'children'),
     Output('rate-change', 'children'),
     Output('interactions-by-type', 'figure'),
     Output('engagement-by-weekday', 'figure'),
     Output('reach-vs-engagement', 'figure'),
     Output('engagement-by-hour', 'figure')],
    [Input('time-frame-dropdown', 'value')]
)
def update_dashboard(time_frame):
    filtered_df = df.copy()
    if time_frame == 'week':
        filtered_df = filtered_df.tail(7)
    elif time_frame == 'month':
        filtered_df = filtered_df.tail(30)

    total_reach = filtered_df['Lifetime Post Total Reach'].sum()
    total_engagement = filtered_df['Lifetime Engaged Users'].sum()
    avg_engagement_rate = (total_engagement / total_reach) * 100 if total_reach > 0 else 0

    # Simulating changes (you may want to calculate actual changes based on your data)
    reach_change = "+5.2% vs last period"
    engagement_change = "+3.7% vs last period"
    rate_change = "+0.5% vs last period"

    color_scheme = ['#4cd964', '#5ac8fa', '#007aff', '#ff9500']

    interactions_by_type = px.pie(filtered_df, names='Type', values='Total Interactions', title='Interactions by Post Type',
                                  color_discrete_sequence=color_scheme)
    
    engagement_by_weekday = px.bar(filtered_df.groupby('Weekday')['Lifetime Engaged Users'].sum().reset_index(), 
                                   x='Weekday', y='Lifetime Engaged Users', title='Engagement by Weekday',
                                   color_discrete_sequence=[color_scheme[1]])
    
    reach_vs_engagement = px.scatter(filtered_df, x='Lifetime Post Total Reach', y='Lifetime Engaged Users', 
                                     title='Reach vs Engagement', labels={'Lifetime Post Total Reach': 'Reach', 'Lifetime Engaged Users': 'Engagement'},
                                     color_discrete_sequence=[color_scheme[2]])
    
    engagement_by_hour = px.line(filtered_df.groupby('Post Hour')['Lifetime Engaged Users'].mean().reset_index(), 
                                 x='Post Hour', y='Lifetime Engaged Users', title='Average Engagement by Hour',
                                 color_discrete_sequence=[color_scheme[3]])

    # Update layout for all figures
    for fig in [interactions_by_type, engagement_by_weekday, reach_vs_engagement, engagement_by_hour]:
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_size=16,
            title_font_color='white'
        )
        fig.update_xaxes(gridcolor='#3a4165', zerolinecolor='#3a4165')
        fig.update_yaxes(gridcolor='#3a4165', zerolinecolor='#3a4165')
    
    return (
        f"{total_reach:,}",
        f"{total_engagement:,}",
        f"{avg_engagement_rate:.2f}%",
        reach_change,
        engagement_change,
        rate_change,
        interactions_by_type,
        engagement_by_weekday,
        reach_vs_engagement,
        engagement_by_hour
    )

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)