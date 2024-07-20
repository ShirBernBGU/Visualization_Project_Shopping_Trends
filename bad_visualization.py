
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load the dataset
df = pd.read_csv('shopping_trends_updated.csv')

# Mapping full state names to their abbreviations
state_abbrev = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
    'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
    'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
    'Wisconsin': 'WI', 'Wyoming': 'WY'
}

# Add a 'state_abbr' column to the DataFrame
df['state_abbr'] = df['Location'].map(state_abbrev)

# Bin the ages into 5-year intervals with a range from 15 to 70
bins = list(range(15, 76, 5))
labels = [f'{i}-{i+4}' for i in range(15, 71, 5)]
df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

# Calculate the average review rating for each age group and gender
average_ratings = df.groupby(['Age Group', 'Gender'])['Review Rating'].mean().reset_index()

category_colors = {
    'Clothing': '#FFEDA0',
    'Footwear': '#FEB24C',
    'Accessories': '#FC4E2A',
    'Outerwear': '#BD0026'
}

color_package = "OrRd"

font_dict = dict(family="Helvetica, sans-serif", size=18)

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div([
        html.H1("Shopping Trends Dashboard", style={'textAlign': 'center', 'fontFamily': 'Helvetica', 'fontSize': '34px', 'padding': '20px 0'}),
        html.P(
            "Explore and analyze customer review ratings, purchase amounts, and trends across different states, seasons, and demographics. Use the filters to customize the visualizations and gain insights into shopping behaviors.",
            style={'textAlign': 'center', 'fontFamily': 'Helvetica', 'fontSize': '20px', 'maxWidth': '800px', 'margin': '0 auto', 'padding': '10px 0'}
        )
    ], style={'backgroundColor': '#f9f9f9', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0px 0px 15px rgba(0, 0, 0, 0.1)'}),
    html.Div([
        html.H2("Filter Options", style={'textAlign': 'left', 'fontFamily': 'Helvetica', 'fontSize': '28px', 'padding': '10px 0'}),
        html.Div([
            html.Div([
                html.Label("Seasons", style={'fontFamily': 'Helvetica', 'fontSize': '20px'}),
                dcc.Checklist(
                    id='season-filter',
                    options=[{'label': season, 'value': season} for season in df['Season'].unique()],
                    value=list(df['Season'].unique()),  # Default to show all seasons
                    inline=True,
                    style={'fontFamily': 'Helvetica', 'fontSize': '18px'}
                ),
            ], style={'flex': '1', 'padding': '10px'}),
            html.Div([
                html.Label("State", style={'fontFamily': 'Helvetica', 'fontSize': '20px'}),
                dcc.Dropdown(
                    id='state-filter',
                    options=[{'label': state, 'value': abbrev} for state, abbrev in state_abbrev.items()],
                    placeholder="Select a state",
                    clearable=True,
                    style={'fontFamily': 'Helvetica', 'fontSize': '18px'}
                ),
            ], style={'flex': '1', 'padding': '10px'}),
            html.Div([
                html.Label("Gender", style={'fontFamily': 'Helvetica', 'fontSize': '20px'}),
                dcc.Checklist(
                    id='gender-checklist',
                    options=[
                        {'label': 'Male', 'value': 'Male'},
                        {'label': 'Female', 'value': 'Female'}
                    ],
                    value=['Male', 'Female'],
                    inline=True,
                    style={'fontFamily': 'Helvetica', 'fontSize': '18px'}
                ),
            ], style={'flex': '1', 'padding': '10px'}),
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'margin': '0 -10px'})
    ], style={'backgroundColor': '#f9f9f9', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0px 0px 15px rgba(0, 0, 0, 0.1)', 'margin': '20px 0'}),
    html.Div([
        html.H2("Visualizations", style={'textAlign': 'left', 'fontFamily': 'Helvetica', 'fontSize': '28px', 'padding': '10px 0'}),
        html.Div([
            html.P("This bar chart displays the average review ratings by state and season.",
                   style={'fontFamily': 'Helvetica', 'fontSize': '18px'}),
            dcc.Graph(id='state-season-bar-chart', style={'width': '100%', 'height': '500px', 'marginBottom': '40px'}),
        ], style={'padding': '10px'}),
        html.Div([
            html.P("These pie charts show the average review ratings for items purchased in each season.",
                   style={'fontFamily': 'Helvetica', 'fontSize': '18px'}),
            dcc.Graph(id='season-item-pie-charts', style={'width': '100%', 'height': '1500px', 'marginBottom': '40px'}),  # Adjusted height
        ], style={'padding': '10px'}),
        html.Div([
            html.P("This bubble plot aggregates shopping trends, showing review ratings, purchase amounts, and previous purchases for the selected seasons.",
                   style={'fontFamily': 'Helvetica', 'fontSize': '18px'}),
            dcc.Graph(id='bubble-plot', style={'width': '100%', 'height': '500px', 'marginBottom': '40px'}),
        ], style={'padding': '10px'}),
        html.Div([
            html.P("This bar chart shows the average review ratings by gender and age group.",
                   style={'fontFamily': 'Helvetica', 'fontSize': '18px'}),
            dcc.Graph(id='gender-age-bar-chart', style={'width': '100%', 'height': '500px', 'marginBottom': '80px'}),  # Added more space
        ], style={'padding': '10px'})
    ], style={'backgroundColor': '#f9f9f9', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0px 0px 15px rgba(0, 0, 0, 0.1)', 'margin': '20px 0'})
])

# Callback to update the state-season bar chart
@app.callback(
    Output('state-season-bar-chart', 'figure'),
    [Input('season-filter', 'value'),
     Input('state-filter', 'value')]
)
def update_state_season_bar_chart(selected_seasons, selected_state):
    # Filter the data based on the selected seasons
    filtered_df = df[df['Season'].isin(selected_seasons)]

    if selected_state:
        filtered_df = filtered_df[filtered_df['state_abbr'] == selected_state]

    # Group data by Location (State) and Season
    state_season_avg_rating = filtered_df.groupby(['Location', 'Season'])['Review Rating'].mean().reset_index()

    # Create the plot
    fig = px.bar(state_season_avg_rating, x='Location', y='Review Rating', color='Season', barmode='group',
                 title='Average Review Ratings by State and Season',
                 labels={'Review Rating': 'Average Review Rating', 'Location': 'State'})

    return fig

# Callback to update the pie charts for each season
@app.callback(
    Output('season-item-pie-charts', 'figure'),
    [Input('season-filter', 'value'),
     Input('state-filter', 'value')]
)
def update_season_item_pie_charts(selected_seasons, selected_state):
    # Filter the data based on the selected seasons
    filtered_df = df[df['Season'].isin(selected_seasons)]

    if selected_state:
        filtered_df = filtered_df[filtered_df['state_abbr'] == selected_state]

    # Grouping data for Question 2
    q2_data = filtered_df.groupby(['Season', 'Item Purchased'])['Review Rating'].mean().reset_index()

    # Create subplots for pie charts
    fig = make_subplots(rows=2, cols=2, subplot_titles=("Average Review Ratings for Items in Winter",
                                                        "Average Review Ratings for Items in Spring",
                                                        "Average Review Ratings for Items in Summer",
                                                        "Average Review Ratings for Items in Fall"),
                        specs=[[{'type': 'pie'}, {'type': 'pie'}],
                               [{'type': 'pie'}, {'type': 'pie'}]])

    seasons = q2_data['Season'].unique()
    for i, season in enumerate(seasons):
        season_data = q2_data[q2_data['Season'] == season]
        row, col = divmod(i, 2)
        fig.add_trace(
            go.Pie(labels=season_data['Item Purchased'], values=season_data['Review Rating'], name=season),
            row=row+1, col=col+1
        )

    fig.update_layout(title_text='Average Review Ratings for Items in Each Season')

    return fig

# Callback to update the bubble plot
@app.callback(
    Output('bubble-plot', 'figure'),
    [Input('season-filter', 'value'),
     Input('state-filter', 'value')]
)
def update_bubble_plot(selected_seasons, selected_state):
    # Filter the data based on the selected seasons
    filtered_df = df[df['Season'].isin(selected_seasons)]

    # If a state is selected, further filter the data
    if selected_state:
        filtered_df = filtered_df[filtered_df['state_abbr'] == selected_state]

    # Aggregate data for the bubble plot
    aggregated_data = filtered_df.groupby(['Item Purchased', 'Category']).agg({
        'Review Rating': 'mean',
        'Purchase Amount (USD)': 'mean',
        'Previous Purchases': 'mean'  # Calculate the average instead of the sum
    }).reset_index()

    custom_palette = ["#EE82EE", "#87CEFA", "#3CB371", "#F4A460"]

    # Create the bubble plot
    fig = px.scatter(
        data_frame=aggregated_data,
        x='Review Rating',
        y='Previous Purchases',
        size='Purchase Amount (USD)',
        color='Category',
        hover_name='Item Purchased',
        title=f'Aggregated Bubble Plot of Shopping Trends for {", ".join(selected_seasons)}',
        labels={
            'Purchase Amount (USD)': 'Purchase Amount (USD)',
            'Review Rating': 'Review Rating',
            'Previous Purchases': 'Previous Purchases',
            'Category': 'Category'
        },
        color_discrete_sequence=custom_palette  # Apply the custom color palette
    )

    fig.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')))  # Add outline to bubbles

    fig.update_layout(
        height=600,
        xaxis_title=dict(font=dict(size=18)),  # Enlarged axis title
        yaxis_title=dict(font=dict(size=18)),  # Enlarged axis title
        margin=dict(l=50, r=50, t=50, b=50),
        font=dict(size=16)  # Enlarges numbers on the axis
    )
    return fig

# Callback to update the bar chart for average review ratings by gender and age group
@app.callback(
    Output('gender-age-bar-chart', 'figure'),
    [Input('season-filter', 'value'),
     Input('gender-checklist', 'value')]
)
def update_gender_age_bar_chart(selected_seasons, selected_genders):
    # Filter the data based on the selected seasons and genders
    filtered_df = df[df['Season'].isin(selected_seasons)]
    filtered_df = filtered_df[filtered_df['Gender'].isin(selected_genders)]

    # Group data by Gender and Age Group
    gender_age_avg_rating = filtered_df.groupby(['Gender', 'Age Group'])['Review Rating'].mean().reset_index()

    # Create the plot
    fig = px.bar(gender_age_avg_rating, x='Age Group', y='Review Rating', color='Gender', barmode='group',
                 title='Average Review Ratings by Gender and Age Group',
                 labels={'Review Rating': 'Average Review Rating', 'Age Group': 'Age Group'})

    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)