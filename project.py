'''
Project
Name: Nika Kolin Melocoton
Student ID: 211015210
Class: CP321
Date: 04-04-25
'''
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import json

app = Dash(suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    html.H1('Project Dashboard (Canada Occupation 2023 Census)', style = {'textAlign': 'center'}),

    # V1: distribution of of human resources in essential services per admin unit
    html.Div([
        html.Label('Select Canada Region'),
        dcc.RadioItems(
            id = 'canada-regions1', # first fig input
            options = [
                {'label':'All', 'value':'All'},
                {'label':'Atlantic Region', 'value':'Atlantic Region'},
                {'label':'Central Canada and West Coast', 'value':'Central Canada and West Coast'},
                {'label':'Prairie Provinces', 'value':'Prairie Provinces'},
                {'label':'North', 'value':'North'}
            ],
            value = 'All',
            inline = True,
            inputStyle = {'margin-left':'20px'}
        )
    ]), 
    dcc.Graph(id = 'first-fig'), # first fig output

    # V2: distribution of men and women workers in several fields
    html.Br(),
    html.Div([
        html.Label('Select Occupation:'),
        dcc.Dropdown(
            id = 'noc-occupations', # second fig input
            options = [
                {'label':'1 - Business', 'value':'1 - Business'},
                {'label':'2 - Natural/Applied Sciences', 'value':'2 - Natural/Applied Sciences'},
                {'label':'3 - Health', 'value':'3 - Health'},
                {'label':'4 - Education/Law/Community', 'value':'4 - Education/Law/Community'},
                {'label':'5 - Art/Culture/Sport', 'value':'5 - Art/Culture/Sport'},
                {'label':'6 - Sales/Service', 'value':'6 - Sales/Service'},
                {'label':'7 - Trades/Transport/Equipment Operators', 'value':'7 - Trades/Transport/Equipment Operators'},
                {'label':'8 - Natural Resources/Agriculture', 'value':'8 - Natural Resources/Agriculture'},
                {'label':'9 - Manufacturing/Utilities', 'value':'9 - Manufacturing/Utilities'}
            ],
            value = '1 - Business'
        )
    ]),
    dcc.Graph(id = 'second-fig'), # second fig output

    # V3: engineer manpower in canada's provinces to analyze what is enough 
    html.Br(),
    html.Div([
        dcc.Tabs(
            id = 'tabs-input', # tabs input
            value = 'tab-1',
            children = [
                dcc.Tab(label = 'Total Engineer Distribution', value = 'tab-1'),
                dcc.Tab(label = 'Distribution of Engineer Types',value = 'tab-2')
            ]
        ),
        html.Div(id = 'tabs-content') # tabs output
    ]),

    # V4: distribution of manpower in certain fields in canada
    html.Br(),
    html.Div([
        html.Label('Select Field:'),
        dcc.Dropdown(
            id = 'noc-field', # fourth fig input 
            options = [
                {'label':'1 - Business', 'value':'1 - Business'},
                {'label':'2 - Natural/Applied Sciences', 'value':'2 - Natural/Applied Sciences'},
                {'label':'3 - Health', 'value':'3 - Health'},
                {'label':'4 - Education/Law/Community', 'value':'4 - Education/Law/Community'},
                {'label':'5 - Art/Culture/Sport', 'value':'5 - Art/Culture/Sport'},
                {'label':'6 - Sales/Service', 'value':'6 - Sales/Service'},
                {'label':'7 - Trades/Transport/Equipment Operators', 'value':'7 - Trades/Transport/Equipment Operators'},
                {'label':'8 - Natural Resources/Agriculture', 'value':'8 - Natural Resources/Agriculture'},
                {'label':'9 - Manufacturing/Utilities', 'value':'9 - Manufacturing/Utilities'}
            ],
            value = '1 - Business'
        )
    ]),
    dcc.Graph(id = 'fourth-fig'), # fourth fig output 
    dcc.RadioItems(
        id = 'canada-regions2', # fourth fig other input
        options = [
            {'label':'All', 'value':'All'},
            {'label':'Atlantic Region', 'value':'Atlantic Region'},
            {'label':'Central Canada and West Coast', 'value':'Central Canada and West Coast'},
            {'label':'Prairie Provinces', 'value':'Prairie Provinces'},
            {'label':'North', 'value':'North'}
        ],
        value = 'All',
        inline = True,
        inputStyle = {'margin-left':'20px'}
    )
])

def update_v1(selected_region):
    data = pd.read_csv('data.csv')

    occupation_col = data.columns[2]
    gender_col = data.columns[3]

    # the essential digits for this visualization
    nurse_digits = ('31300','31301','31302','32101')
    police_digits = ('40040', '42100')
    firefight_digits = ('40041','42101')

    # only keeping track of total values (disregarding gender values)
    total_gender = data[data[gender_col] == 'Total - Gender']
    admin_units = ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick', 'Newfoundland and Labrador', 'Nova Scotia', 'Northwest Territories', 'Nunavut', 'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan', 'Yukon']

    # creating a new dataframe that contains the nurse, police, and firefighter percentage
    nurse_percent = []
    police_percent = []
    firefighter_percent = []
    for admin in admin_units:
        admin_data = total_gender.loc[total_gender['GEO']==admin]
        n_sum = admin_data[admin_data[occupation_col].str.startswith(nurse_digits)]['VALUE'].sum()
        p_sum = admin_data[admin_data[occupation_col].str.startswith(police_digits)]['VALUE'].sum()
        f_sum = admin_data[admin_data[occupation_col].str.startswith(firefight_digits)]['VALUE'].sum()
        all_sum = n_sum+p_sum+f_sum

        nurse_percent.append(round((n_sum/all_sum)*100,2))
        police_percent.append(round((p_sum/all_sum)*100,2))
        firefighter_percent.append(round((f_sum/all_sum)*100,2))

    admin = []
    service_name = []
    dist_percent = []
    for i in range(len(admin_units)):
        admin.append(admin_units[i])
        service_name.append('Nurse')
        dist_percent.append(nurse_percent[i])

        admin.append(admin_units[i])
        service_name.append('Police')
        dist_percent.append(police_percent[i])

        admin.append(admin_units[i])
        service_name.append('Firefighter')
        dist_percent.append(firefighter_percent[i])

    new_data = pd.DataFrame({
        'Admin':admin,
        'Service Name':service_name,
        'Human Resources (%)':dist_percent
    })

    canada_regions = {
        'All':admin_units,
        'Atlantic Region':['Newfoundland and Labrador','Prince Edward Island','Nova Scotia','New Brunswick'],
        'Central Canada and West Coast':['Quebec','Ontario','British Columbia'],
        'Prairie Provinces':['Manitoba','Saskatchewan','Alberta'],
        'North':['Nunavut','Northwest Territories','Yukon']
    }
    selected_data = new_data[new_data['Admin'].str.contains('|'.join(canada_regions[selected_region]))]

    fig = px.bar(selected_data, x = 'Human Resources (%)',
                y = 'Admin',
                color = 'Service Name',
                orientation = 'h',
                title = f"Canada's Human Resources (%) in Essential Services - {selected_region}")
    fig.update_layout(
        title_x = 0.5,
        yaxis_title = 'Provinces/Territories'
    )
    
    return fig

def update_v2(selected_occupation):
    data = pd.read_csv('data.csv')
    occupation_col = data.columns[2]
    gender_col = data.columns[3]

    # filter data with selected occupation and calculate the percentage of men and women working in that selected occupation
    filtered_data = data[data[occupation_col].str.startswith(selected_occupation[:2])]
    total_data = filtered_data[filtered_data[gender_col]=='Total - Gender']
    total_val = []
    for val in list(total_data['VALUE']):
        total_val.extend([val,val])
    new_data = filtered_data[filtered_data[gender_col].str.startswith(('Men+','Women+'))].copy()
    new_data['Total Value'] = total_val
    new_data['Percentage'] = round(new_data['VALUE']/new_data['Total Value']*100,2)

    men_percentage = new_data[new_data[gender_col] == 'Men+']
    women_percentage = new_data[new_data[gender_col] == 'Women+']

    # do grouped bar for men and women in selected occupation 
    fig = go.Figure(data = [
        go.Bar(name = 'Men+', x = men_percentage['GEO'], y = men_percentage['Percentage']),
        go.Bar(name = 'Women+', x = women_percentage['GEO'], y = women_percentage['Percentage'])
    ])

    # update graph layout to change the xtick values to be shorter and to set the xlabel, ylabel, and title
    admin_units = ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick', 'Newfoundland and Labrador', 'Nova Scotia', 'Northwest Territories', 'Nunavut', 'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan', 'Yukon']
    fig.update_layout(
        height = 500,
        title = f"Canada's Gender Statistics in {selected_occupation}",
        title_x = 0.5,
        barmode = 'group',
        xaxis = dict(
            tickvals = admin_units
        ),
        legend = dict(
            title = dict (
                text = 'Gender'
            )
        ),
        xaxis_title = 'Provinces/Territories',
        xaxis_tickangle = 45,
        yaxis_title = 'Human Resources (%)')
    return fig    

def update_v3(selected_engineer):
    data = pd.read_csv('data.csv')
    occupation_col = data.columns[2]
    gender_col = data.columns[3]
    total_data = data[data[gender_col] == 'Total - Gender']
    admin_units = ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick', 'Newfoundland and Labrador', 'Nova Scotia', 'Northwest Territories', 'Nunavut', 'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan', 'Yukon']

    computer_digits = ('21311','21231','21232')
    mechanical_digits = ('21301','22301')
    electrical_digits = ('21310','22310')

    computer_engineers = total_data[total_data[occupation_col].str.startswith(computer_digits)]
    mechanical_engineers = total_data[total_data[occupation_col].str.startswith(mechanical_digits)]
    electrical_engineers = total_data[total_data[occupation_col].str.startswith(electrical_digits)]
    all_occupations = total_data[total_data[occupation_col].str.startswith('All')]

    # calculating total values for all the engineering types
    total_computer = []
    total_mechanical = []
    total_electrical = []
    total_engineers = []
    total_all_occupations = []
    for i,admin in enumerate(admin_units):
        total_computer.append(computer_engineers[computer_engineers['GEO']==admin]['VALUE'].sum())
        total_mechanical.append(mechanical_engineers[mechanical_engineers['GEO']==admin]['VALUE'].sum())
        total_electrical.append(electrical_engineers[electrical_engineers['GEO']==admin]['VALUE'].sum())
        total_engineers.append(total_computer[i]+total_mechanical[i]+total_electrical[i])
        total_all_occupations.append(all_occupations.loc[all_occupations.index[i],'VALUE'])

    # calculating the percentages to create a new dataset
    comp_percent = []
    mech_percent =[]
    elect_percent =[]
    all_types_percent = []
    for i in range(len(total_all_occupations)):
        comp_percent.append(round((total_computer[i]/total_engineers[i])*100,2))
        mech_percent.append(round((total_mechanical[i]/total_engineers[i])*100,2))
        elect_percent.append(round((total_electrical[i]/total_engineers[i])*100,2))
        all_types_percent.append(round((total_engineers[i]/total_all_occupations[i])*100,2))

    new_data = pd.DataFrame({
        'Admin Units':admin_units,
        'Computer (%)':comp_percent,
        'Mechanical (%)':mech_percent,
        'Electrical (%)':elect_percent,
        'All Engineering Types (%)':all_types_percent
    })

    # finding which percentages is the max and min to create line
    order_dict = {}
    for i in range(len(selected_engineer)):
        order_dict[i] = selected_engineer[i]
    order_max = []
    order_min = []

    if len(selected_engineer)>1:
        for i in range(len(new_data)):
            temp_values = []
            if len(selected_engineer)>2:
                temp_values.extend([new_data[selected_engineer[0]][i],new_data[selected_engineer[1]][i],new_data[selected_engineer[2]][i]])
            else:
                temp_values.extend([new_data[selected_engineer[0]][i],new_data[selected_engineer[1]][i]])
            max_index = temp_values.index(max(temp_values))
            min_index = temp_values.index(min(temp_values))

            order_max.append(order_dict[max_index])
            order_min.append(order_dict[min_index])
    
    # creating the figure depending on the tab and checklist
    fig = go.Figure()

    # FOR MULTIPLE VALUES
    if len(selected_engineer)>1:
        title = []
        for name in selected_engineer:
            name = name.replace(' (%)','')
            title.append(name)
        fig = px.scatter(new_data,
                         x = selected_engineer,
                         y = 'Admin Units',
                         title = f'Canada Distribution of {title} Types')
        for i in range(len(new_data)):
            fig.add_shape(
                type = 'line',
                x0 = new_data.loc[new_data.index[i],order_min[i]], y0 = new_data.loc[new_data.index[i],'Admin Units'],
                x1 = new_data.loc[new_data.index[i],order_max[i]], y1 = new_data.loc[new_data.index[i],'Admin Units'],
                line_color = '#cccccc')
    # FOR SINGLE VALUE
    elif len(selected_engineer)==1:
        title = ''
        if selected_engineer[0] == 'All Engineering Types (%)':
            title = f'Canada Total Distribution of {selected_engineer[0]}'
        else:
            title = f'Canada Distribution of {selected_engineer[0]} Type'
        fig = px.scatter(new_data,
                         x = selected_engineer,
                         y = 'Admin Units',
                         title = title.replace('(%)',''))
        for i in range(len(new_data)):
            fig.add_shape(
                type = 'line',
                x0 = 0, y0 = new_data.loc[new_data.index[i],'Admin Units'],
                x1 = new_data.loc[new_data.index[i],selected_engineer[0]], y1 = new_data.loc[new_data.index[i],'Admin Units'],
                line_color = '#cccccc')
    fig.update_traces(marker_size = 15)
    fig.update_layout(
        title_x = 0.5,
        xaxis_title = 'Human Resources Distribution (%)',
        yaxis_title = 'Provinces/Territories',
    )
    return fig

def update_v4(selected_field,selected_unit):
    data = pd.read_csv('data.csv')
    occupation_col = data.columns[2]
    gender_col = data.columns[3]

    # filtering for total data only (disregarding gender)
    total_data = data[data[gender_col]=='Total - Gender']
    
    single_digits = ('1 ','2 ','3 ','4 ','5 ','6 ','7 ','8 ','9 ')
    admin_units = ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick', 'Newfoundland and Labrador', 'Nova Scotia', 'Northwest Territories', 'Nunavut', 'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan', 'Yukon']
    
    canada_regions = {
        'All':admin_units,
        'Atlantic Region':['Newfoundland and Labrador','Prince Edward Island','Nova Scotia','New Brunswick'],
        'Central Canada and West Coast':['Quebec','Ontario','British Columbia'],
        'Prairie Provinces':['Manitoba','Saskatchewan','Alberta'],
        'North':['Nunavut','Northwest Territories','Yukon']
        }


    filtered_occupation = total_data[total_data[occupation_col].str.startswith(selected_field[:2])]
    all_occupations = total_data[total_data[occupation_col].str.startswith(single_digits)]

    chosen_provinces = canada_regions[selected_unit]
    percentages = []
    # calculating the percentages of the people working in the fields and creating a new data
    for admin in chosen_provinces:
        occupation_val = filtered_occupation[filtered_occupation['GEO']==admin]['VALUE'].iloc[0]
        all_occupations_total = all_occupations[all_occupations['GEO']==admin]['VALUE'].sum()
        percentages.append(round((occupation_val/all_occupations_total)*100,2))

    # changing last value for geojson data
    admin_units[-1] = 'Yukon Territory'
    canada_regions['All'] = admin_units

    new_data = pd.DataFrame({
        'Admin Units':chosen_provinces,
        'Percentages':percentages
    })

    # creating geojson graph
    with open('canada.geojson') as f:
        geojson_data = json.load(f)
    fig = go.Figure(go.Choropleth(
        geojson = geojson_data,
        locations = new_data['Admin Units'],
        z = new_data['Percentages'],
        featureidkey = 'properties.name',
        colorscale = 'Greens',
        colorbar_tickprefix = '% ',
        colorbar_title = f'% Human Resources'
    ))
    fig.update_geos(showcountries=True, showcoastlines=True, showland=True, fitbounds="geojson")
    fig.update_layout(
        title = f'Canada Human Resource in {selected_field} Essential Service',
        title_x = 0.5
    )
    return fig

# call back for visualizations 1 and 2 
@callback(
    Output('first-fig','figure'),
    Output('second-fig','figure'),
    Input('canada-regions1','value'),
    Input('noc-occupations','value')
)

def update_graphs12(selected_region,selected_occupation):
    return [update_v1(selected_region),update_v2(selected_occupation)]

# call back for visualization 3
@callback(
    Output('tabs-content','children'),
    Input('tabs-input','value')
)

def render_content(tab):
    if tab == 'tab-1':
        return dcc.Graph(figure = update_v3(['All Engineering Types (%)']))
    elif tab == 'tab-2':
        return html.Div([
            html.Label('Select Engineer Type(s):'),
            dcc.Checklist(
                id = 'engineer-check', # input for checklist
                options = [
                    {'label':'Computer','value':'Computer (%)'},
                    {'label':'Mechanical','value':'Mechanical (%)'},
                    {'label':'Electrical','value':'Electrical (%)'}
                ],
                value = ['Computer (%)','Mechanical (%)','Electrical (%)'],
                inline = True
            ),
            dcc.Graph(id = 'third-fig') # output for checklist
        ])

# call back for visualization 3
@callback(
    Output('third-fig','figure'),
    Input('engineer-check','value')
)

def update_graph3(selected_engineer):
    return update_v3(selected_engineer)

# call back for visualization 4
@callback(
    Output('fourth-fig','figure'),
    Input('noc-field','value'),
    Input('canada-regions2','value')
)

def update_graph4(selected_field,selected_unit):
    return update_v4(selected_field,selected_unit)

if __name__ == '__main__':
    app.run(debug = True)
