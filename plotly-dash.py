import dash
from dash import dcc,html
import requests
import plotly.graph_objects as go
import plotly.colors

app = dash.Dash(__name__)

# Fetch data from the API
api_url='https://c5hbwkkh55.execute-api.us-east-1.amazonaws.com/api/'
response = requests.get(api_url)
data = response.json()['body']

# Process the data for the pie chart
categories = [item['category'] for item in data]
category_counts = {}
for category in categories:
    if category in category_counts:
        category_counts[category] += 1
    else:
        category_counts[category] = 1

labels = list(category_counts.keys())
values = list(category_counts.values())

# Create the Pie chart figure
fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
fig.update_layout(
    title='Companies that belong to different Category under Computer & Internet',
)



# Bar chart for the category distribution in the data
# Generate a color scale based on the number of categories
colors = plotly.colors.qualitative.Dark24[:len(labels)]

bar = go.Figure(data=[go.Bar(x=labels, y=values,marker=dict(color=colors))])
bar.update_layout(
    title='Number of companies that belong to different Category under Computer & Internet',
    xaxis=dict(title='Category'),
    yaxis=dict(title='Count'),
    showlegend=False
)



# Check the number of companies which has websites
has_website_count = 0
no_website_count = 0

for item in data:
    if item['website'] is not None:
        has_website_count += 1
    else:
        no_website_count += 1

# print("Data with website:", has_website_count)
# print("Data without website:", no_website_count)

bar_labels = ['With Website', 'No Website']
bar_values = [has_website_count, no_website_count]

colors=['green','red']
website_bar = go.Figure(data=[go.Bar(x=bar_labels, y=bar_values,marker=dict(color=colors))])

website_bar.update_layout(
    title='Number of Companies with and without Website',
    xaxis=dict(title='Website'),
    yaxis=dict(title='Count'),
    showlegend=False
)




# Check the number of companies in different districts
districts=[item['district_location'] for item in data]
district_counts={}

for district in districts:
    if district in district_counts:
        district_counts[district]+=1
    else:
        district_counts[district]=1

del district_counts['[email\xa0protected]']

# Count number of None values
none_count = district_counts.pop(None, 0)

# Remove None from district_counts
if None in district_counts:
    del district_counts[None]

# Sort district_counts in descending order based on values
district_counts = dict(sorted(district_counts.items(), key=lambda x: x[1], reverse=True))

# district_counts
district_names = list(district_counts.keys())
district_names = [name.upper() for name in district_names]
district_values = list(district_counts.values())

# print(district_names,district_values)

# Create the bar trace
bar_trace = go.Bar(
    x=district_names,
    y=district_values,
    marker=dict(color='blue')
)

# Create the layout
layout = go.Layout(
    title='Number of Companies in a District (Nepal)',
    xaxis=dict(title='District'),
    yaxis=dict(title='Log10(Number of Companies)'),
)

# Create the figure
district_bar = go.Figure(data=[bar_trace], layout=layout)




# Company establisheed in certain year
# Filter out the companies with establishment year not specified
filtered_data = [item for item in data if item['establishment_year'] != 'Not Specified']

# Count the number of companies for each establishment year
year_counts = {}
for item in filtered_data:
    year = item['establishment_year']
    if year in year_counts:
        year_counts[year] += 1
    else:
        year_counts[year] = 1

# Sort the establishment years in ascending order
sorted_years = sorted(year_counts.keys())

# Create the bar trace
bar_trace = go.Bar(
    x=sorted_years,
    y=[year_counts[year] for year in sorted_years],
    marker=dict(color='blue')
)

# Create the layout
layout = go.Layout(
    title='Number of Companies Established in specific year',
    xaxis=dict(title='Establishment Year'),
    yaxis=dict(title='Count')
)

# Create the figure
company_est_year = go.Figure(data=[bar_trace], layout=layout)

app.layout = html.Div([
    html.Div([
        dcc.Graph(
            id='pie-chart',
            figure=fig
        )
    ]),
    html.Div([
        dcc.Graph(
            id='bar-chart',
            figure=bar
        )
    ]),
    html.Div([
        dcc.Graph(
            id='website-bar',
            figure=website_bar
        )
    ]),
    html.Div([
        dcc.Graph(
            id='district-bar',
            figure=district_bar
        )
    ]),
    html.Div([
        dcc.Graph(
            id='company_est_year',
            figure=company_est_year
        )
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)