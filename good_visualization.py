
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import seaborn as sns

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
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'margin': '0 -10px'})
    ], style={'backgroundColor': '#f9f9f9', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0px 0px 15px rgba(0, 0, 0, 0.1)', 'margin': '20px 0'}),
    html.Div([
        html.H2("Visualizations", style={'textAlign': 'left', 'fontFamily': 'Helvetica', 'fontSize': '28px', 'padding': '10px 0'}),
        html.Div([
            html.P("This map shows the average review ratings across different states for the selected seasons.",
                   style={'fontFamily': 'Helvetica', 'fontSize': '18px'}),
            dcc.Graph(id='choropleth-map', style={'width': '100%', 'height': '500px', 'marginBottom': '40px'}),
        ], style={'padding': '10px'}),
        html.Div([
            html.P("This bar chart displays the average review ratings of different items purchased for the selected seasons.",
                   style={'fontFamily': 'Helvetica', 'fontSize': '18px'}),
            dcc.Graph(id='bar-chart', style={'width': '100%', 'height': '500px', 'marginBottom': '40px'}),
        ], style={'padding': '10px'}),
        html.Div([
            html.P("This bubble plot aggregates shopping trends, showing review ratings, purchase amounts, and previous purchases for the selected seasons. The bubble size represents the total number of previous purchases.",
                   style={'fontFamily': 'Helvetica', 'fontSize': '18px'}),
            dcc.Graph(id='bubble-plot', style={'width': '100%', 'height': '500px', 'marginBottom': '40px'}),
        ], style={'padding': '10px'}),
        html.Div([
            html.P("This line plot shows the average review ratings by age group and gender for the selected seasons.",
                   style={'fontFamily': 'Helvetica', 'fontSize': '18px'}),
            dcc.Checklist(
                id='gender-overall-checklist',
                options=[
                    {'label': 'Male', 'value': 'Male'},
                    {'label': 'Female', 'value': 'Female'},
                    {'label': 'Overall', 'value': 'Overall'}
                ],
                value=['Male', 'Female', 'Overall'],
                inline=True,
                style={'fontFamily': 'Helvetica', 'fontSize': '18px'}
            ),
            dcc.Graph(id='scatter-plot', style={'width': '100%', 'height': '500px', 'marginBottom': '40px'}),
        ], style={'padding': '10px'})
    ], style={'backgroundColor': '#f9f9f9', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0px 0px 15px rgba(0, 0, 0, 0.1)', 'margin': '20px 0'})
])

# Callback to update the choropleth map
@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('season-filter', 'value'),
     Input('state-filter', 'value')]
)
def update_map(selected_seasons, selected_state):
    # Filter the data based on the selected seasons
    filtered_df = df[df['Season'].isin(selected_seasons)]

    # Aggregate the data to get the average review rating per state
    avg_ratings = filtered_df.groupby(['Location', 'state_abbr'])['Review Rating'].mean().reset_index()

    if selected_state:
        avg_ratings = avg_ratings[avg_ratings['state_abbr'] == selected_state]

    # Create the choropleth map
    fig = px.choropleth(
        avg_ratings,
        locations='state_abbr',
        locationmode='USA-states',
        color='Review Rating',
        color_continuous_scale='OrRd',
        scope='usa',
        labels={'Review Rating': 'Avg Review Rating'},
        title=f'Average Review Ratings by State for {", ".join(selected_seasons)}',
        hover_data={'Location': True, 'state_abbr': False}
    )

    fig.update_layout(
        geo=dict(
            lakecolor='rgb(255, 255, 255)'
        ),
        coloraxis_colorbar=dict(
            title="Avg Review Rating",
            thickness=50,  # Enlarged thickness
            len=1.0  # Enlarged length of the color bar
        ),
        font=dict(size=16)  # Enlarges numbers on the axis
    )

    return fig

# Callback to update the bar chart
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('season-filter', 'value'),
     Input('state-filter', 'value')]
)
def update_bar_chart(selected_seasons, selected_state):
    # Filter the data based on the selected seasons
    filtered_df = df[df['Season'].isin(selected_seasons)]

    # If a state is selected, further filter the data
    if selected_state:
        filtered_df = filtered_df[filtered_df['state_abbr'] == selected_state]

    # Calculate the average review rating for each item purchased
    avg_ratings = filtered_df.groupby(['Item Purchased'])['Review Rating'].mean().reset_index()

    # Merge with category data
    avg_ratings = avg_ratings.merge(filtered_df[['Item Purchased', 'Category']].drop_duplicates(), on='Item Purchased')

    # Sort the items by average review rating in descending order
    sorted_df = avg_ratings.sort_values(by='Review Rating', ascending=False)

    # Define the color palette 
    custom_palette = ["#EE82EE", "#87CEFA", "#3CB371", "#F4A460"]

    # Create the bar chart, coloring by category with a fixed color map
    fig = px.bar(
        sorted_df,
        x='Review Rating',
        y='Item Purchased',
        color='Category',  # Color bars by category
        color_discrete_sequence=custom_palette,  # Apply the spectral color palette
        orientation='h',
        labels={'Review Rating': 'Average Review Rating', 'Item Purchased': 'Item Purchased'},
        title=f'Average Review Ratings by Item Purchased for {", ".join(selected_seasons)}',
    )

    fig.update_layout(
        xaxis=dict(range=[sorted_df['Review Rating'].min() - 0.1, sorted_df['Review Rating'].max()]),
        xaxis_title=dict(font=dict(size=18)),  # Enlarged axis title
        yaxis_title=dict(font=dict(size=18)),  # Enlarged axis title
        height=600,
        margin=dict(l=50, r=50, t=50, b=50),
        yaxis={'categoryorder': 'total ascending'},  # Ensures sorting by review rating
        font=dict(size=16)  # Enlarges numbers on the axis
    )
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
        'Previous Purchases': 'sum'
    }).reset_index()

    custom_palette = ["#EE82EE", "#87CEFA", "#3CB371", "#F4A460"]

    # Create the bubble plot
    fig = px.scatter(
        data_frame=aggregated_data,
        x='Purchase Amount (USD)',
        y='Review Rating',
        size='Previous Purchases',
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

# Callback to update the scatter plot
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('gender-overall-checklist', 'value'),
     Input('season-filter', 'value'),
     Input('state-filter', 'value')]
)
def update_scatter_plot(selected_overall_genders, selected_seasons, selected_state):
    # Filter the data based on the selected seasons
    filtered_df = df[df['Season'].isin(selected_seasons)]

    # If a state is selected, further filter the data
    if selected_state:
      filtered_df = filtered_df[filtered_df['state_abbr'] == selected_state]

    # Recalculate the average review rating for each age group and gender
    average_ratings_filtered = filtered_df.groupby(['Age Group', 'Gender'])['Review Rating'].mean().reset_index()

    # Calculate the overall average review rating for each age group
    overall_average_ratings = filtered_df.groupby(['Age Group'])['Review Rating'].mean().reset_index()
    overall_average_ratings['Gender'] = 'Overall'

    # Combine the average ratings for male, female, and overall
    combined_ratings = pd.concat([average_ratings_filtered, overall_average_ratings])

    # Filter the combined ratings based on selected overall genders
    combined_ratings = combined_ratings[combined_ratings['Gender'].isin(selected_overall_genders)]

    # Create the scatter plot
    fig = px.scatter(
        combined_ratings,
        x='Age Group',
        y='Review Rating',
        color='Gender',
        color_discrete_map={'Male': '#3CB371', 'Female': '#EE82EE', 'Overall': '#000000'},
        labels={'Age Group': 'Age Group', 'Review Rating': 'Average Review Rating'},
        title='Average Review Rating by Age Group and Gender'
    )
    fig.update_traces(mode='markers+lines')

    fig.update_layout(
        xaxis_title=dict(font=dict(size=18)),  # Enlarged axis title
        yaxis_title=dict(font=dict(size=18)),  # Enlarged axis title
        font=dict(size=16)  # Enlarges numbers on the axis
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)