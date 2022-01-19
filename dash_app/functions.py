# Done by Muhammad Mustaffa and Farhan Basir 'Ul Elmi
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json


class Graph:
    def __init__(self):
        self.pathlist = []

    def minDistance(self, dist, queue):
        minimum = float("Inf")
        min_index = -1

        for i in range(len(dist)):
            if dist[i] < minimum and i in queue:
                minimum = dist[i]
                min_index = i
        return min_index

    def printPath(self, parent, j):
        if parent[j] == -1:
            print(j)
            return
        self.printPath(parent, parent[j])
        print(j)
        self.pathlist.append(j)

    def printSolution(self, dist, parent, src, end):

        print("Vertex \t\tDistance from Source\tPath")
        # for i in range(1, len(dist)):
        #     print("\n%d --> %d \t\t%d \t\t\t\t\t" % (src, i, dist[i])),
        #     self.printPath(parent, i)
        print("\n%d --> %d \t\t%d \t\t\t\t\t" % (src, end, dist[end])),
        self.printPath(parent, end)

    def dijkstra(self, graph, src, end):
        self.pathlist.append(src)
        row = len(graph)
        col = len(graph[0])

        dist = [float("Inf")] * row

        parent = [-1] * row

        dist[src] = 0

        queue = []
        for i in range(row):
            queue.append(i)

        while queue:
            u = self.minDistance(dist, queue)
            queue.remove(u)

            for i in range(col):
                if graph[u][i] and i in queue:
                    if dist[u] + graph[u][i] < dist[i]:
                        dist[i] = dist[u] + graph[u][i]
                        parent[i] = u
        self.printSolution(dist, parent, src, end)


def AreaList(mean):
    """''' Generating a list of tube stations for Dash Dropdown '''"""
    data = pd.ExcelFile('../data/Tube_and_Bus_Route_Stops.xls')
    sheet = 'Bus Regions Simplified'
    if 'Tube' in mean:
        sheet = 'Tube Regions Simplified'
    return pd.read_excel(data, sheet_name=sheet, skiprows=1)


def ConvertNavigationVariables(mean, start, end):
    df = AreaList(mean)
    # Create dataframe from dataset
    df = df[{'Group stations', 'Number'}].set_index('Group stations')
    start_number = df.loc[start, 'Number']
    end_number = df.loc[end, 'Number']

    return start_number, end_number


def FindPath(mean, start, end):
    start_number, end_number = ConvertNavigationVariables(mean, start, end)

    data = pd.read_excel('../data/multi-year-station-entry-and-exit-figures.xls',
                         sheet_name='2017 Entry & Exit (Zone 1)', skiprows=6)

    df = pd.DataFrame(data)
    df1 = pd.DataFrame(index=range(23), columns=['total']).fillna(0)
    df2 = df['Group Alphabet'].drop_duplicates().dropna().reset_index()

    for x, poo in df1.iterrows():
        for y, lines in df.iterrows():
            if x == lines['Group Number']:
                poo['total'] += lines['million']

    df3 = pd.concat([df1, df2['Group Alphabet']], axis=1, join='inner')

    # entry/exit for each station

    A = df3.iloc[0]['total']
    B = df3.iloc[1]['total']
    C = df3.iloc[2]['total']
    D = df3.iloc[3]['total']
    E = df3.iloc[4]['total']
    F = df3.iloc[5]['total']
    G = df3.iloc[6]['total']
    H = df3.iloc[7]['total']
    I = df3.iloc[8]['total']
    J = df3.iloc[9]['total']
    K = df3.iloc[10]['total']
    L = df3.iloc[11]['total']
    M = df3.iloc[12]['total']
    N = df3.iloc[13]['total']
    O = df3.iloc[14]['total']
    P = df3.iloc[15]['total']
    Q = df3.iloc[16]['total']
    R = df3.iloc[17]['total']
    S = df3.iloc[18]['total']
    T = df3.iloc[19]['total']
    U = df3.iloc[20]['total']
    V = df3.iloc[21]['total']
    W = df3.iloc[22]['total']

    g = Graph()

    #            0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22
    #            A  B  C  D  E  F  G  H  I  J  K  L  M  N  O  P  Q  R  S  T  U  V  W
    tube_map = [[0, A, A, A, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # A 0
                [B, 0, B, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # B 1
                [C, C, 0, C, 0, C, C, C, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, C, 0, 0, 0, 0],  # C 2
                [D, 0, D, 0, D, D, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # D 3
                [0, 0, 0, E, 0, E, 0, 0, E, E, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, E],  # E 4
                [0, 0, F, F, F, 0, F, 0, F, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # F 5
                [0, 0, G, 0, 0, G, 0, G, G, 0, G, 0, 0, 0, 0, 0, 0, 0, G, 0, 0, 0, 0],  # G 6
                [0, 0, H, 0, 0, 0, H, 0, 0, 0, H, 0, 0, 0, 0, 0, 0, H, H, 0, 0, 0, 0],  # H 7
                [0, 0, 0, 0, I, I, I, 0, 0, I, I, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # I 8
                [0, 0, 0, 0, J, 0, 0, 0, J, 0, J, J, 0, J, 0, 0, 0, 0, 0, 0, 0, 0, J],  # J 9
                [0, 0, 0, 0, 0, 0, K, K, K, K, 0, 0, 0, K, K, 0, 0, K, 0, 0, 0, 0, 0],  # K 10
                [0, 0, 0, 0, 0, 0, 0, 0, 0, L, 0, 0, L, L, 0, 0, 0, 0, 0, 0, L, L, L],  # L 11
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, M, 0, M, 0, 0, 0, 0, 0, M, M, 0, 0],  # M 12
                [0, 0, 0, 0, 0, 0, 0, 0, 0, N, N, N, N, 0, N, 0, 0, 0, 0, N, 0, 0, 0],  # N 13
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, O, 0, 0, O, 0, O, O, O, 0, O, 0, 0, 0],  # O 14
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, P, 0, P, 0, 0, P, 0, 0, 0],  # P 15
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, Q, Q, 0, Q, 0, 0, 0, 0, 0],  # Q 16
                [0, 0, 0, 0, 0, 0, 0, R, 0, 0, R, 0, 0, 0, R, 0, R, 0, R, 0, 0, 0, 0],  # R 17
                [0, 0, S, 0, 0, 0, 0, S, 0, 0, 0, 0, 0, 0, 0, 0, 0, S, 0, 0, 0, 0, 0],  # S 18
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, T, T, T, T, 0, 0, 0, 0, 0, 0, 0],  # T 19
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, U, U, 0, 0, 0, 0, 0, 0, 0, 0, U, 0],  # U 20
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, V, 0, 0, 0, 0, 0, 0, 0, 0, V, 0, V],  # V 21
                [0, 0, 0, 0, W, 0, 0, 0, 0, W, 0, W, 0, 0, 0, 0, 0, 0, 0, 0, 0, W, 0]]  # W 22

    #           0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17
    #           A  B  C  D  E  F  G  H  I  J  K  L  M  N  O  P  Q  R
    bus_map = [[0, A, A, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # A 0
               [B, 0, 0, B, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # B 1
               [C, 0, 0, C, 0, 0, C, 0, C, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # C 2
               [0, D, D, 0, D, 0, D, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # D 3
               [0, 0, 0, E, 0, E, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # E 4
               [0, 0, 0, 0, F, 0, F, F, 0, 0, 0, 0, 0, 0, 0, 0, 0, F],  # F 5
               [0, 0, G, G, 0, G, 0, G, G, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # G 6
               [0, 0, 0, 0, 0, H, H, 0, H, H, H, 0, 0, H, 0, 0, H, 0],  # H 7
               [0, 0, I, 0, 0, 0, I, I, 0, I, 0, 0, 0, 0, 0, 0, 0, 0],  # I 8
               [0, 0, 0, 0, 0, 0, 0, J, J, 0, J, J, 0, 0, 0, 0, 0, 0],  # J 9
               [0, 0, 0, 0, 0, 0, 0, K, 0, K, 0, K, 0, K, 0, 0, 0, 0],  # K 10
               [0, 0, 0, 0, 0, 0, 0, 0, 0, L, L, 0, L, L, 0, 0, 0, 0],  # L 11
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, M, 0, M, M, 0, 0, 0],  # M 12
               [0, 0, 0, 0, 0, 0, 0, N, 0, 0, N, N, N, 0, N, N, N, 0],  # N 13
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, O, O, 0, O, 0, 0],  # O 14
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, P, P, 0, P, P],  # P 15
               [0, 0, 0, 0, 0, 0, 0, Q, 0, 0, 0, 0, 0, Q, 0, Q, 0, Q],  # Q 16
               [0, 0, 0, 0, 0, R, 0, 0, 0, 0, 0, 0, 0, 0, 0, R, R, 0]]  # R 17

    mean_map = bus_map
    if 'Tube' in mean:
        mean_map = tube_map

    print(mean_map, start_number, end_number)
    g.dijkstra(mean_map, start_number, end_number)
    path = g.pathlist
    return path


def GeojsonLoader(mean):
    # Setting the json for appropriate mean and opening the file
    json_file = '../data/bus_areas_simplified.json'
    if 'Tube' in mean:
        json_file = '../data/tube_areas_simplified.json'
    with open(json_file) as jsonfile:
        return json.load(jsonfile)


def CreateBorders(mean, start, end):
    """ Inserting the transportation mode as mean, start point and end point and returning the """
    geojson = GeojsonLoader(mean)
    if start is None:
        start = ''
    if end is None:
        end = ''

    # Create dataframe from dataset
    df = AreaList(mean)[{'Group stations'}].set_index('Group stations')
    df["Status"] = np.nan
    df.loc[start, 'Status'] = 'Start'
    df.loc[end, 'Status'] = 'End'
    df = df.reset_index().dropna()
    return RenderNavigationMap(df, geojson)


def CreateBordersWithPath(mean, start, end):
    """ Inserting the transportation mode as mean, start point and end point and returning the """
    geojson = GeojsonLoader(mean)
    path = FindPath(mean, start, end)

    # Create dataframe from dataset
    df = AreaList(mean)[{'Group stations', 'Number'}].set_index('Group stations')
    df["Status"] = np.nan
    df = df.reset_index().set_index('Number')

    j = 0
    for i in path:
        df.loc[i, 'Status'] = j
        j += 1

    df = df.reset_index().dropna()
    return RenderNavigationMap(df, geojson), path


def RenderNavigationMap(df, geojson):
    mapbox_access_token = "pk.eyJ1IjoiYmFkcnVsbXVzdGFmZmEiLCJhIjoiY2ttMzE1cXgzNGJ0dzJ1bnc0Z3hkZnBpbSJ9." \
                          "GEDuGnidtzWvTiXPCGIX4w"
    fig = px.choropleth_mapbox(df, geojson=geojson, locations='Group stations',
                               color='Status',
                               color_discrete_map={'Start': 'blue', 'End': 'red', 'Intermediate': 'yellow'},
                               color_continuous_scale='Bluered',
                               mapbox_style="open-street-map",
                               featureidkey="properties.id",
                               opacity=1, labels={'Status': 'Legend'})

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 10},
                      autosize=True,
                      showlegend=False,
                      coloraxis_showscale=False,
                      mapbox=go.layout.Mapbox(
                          dict(accesstoken=mapbox_access_token),
                          zoom=11, center={"lat": 51.5087, "lon": -0.1346},
                          layers=[{'sourcetype': 'geojson',
                                   'source': geojson,
                                   'type': 'line'}]
                      ), mapbox_style="streets"
                      )
    return fig


def BusDataframe(path):
    data1 = pd.read_excel('../data/Tube_and_Bus_Route_Stops.xls',
                          sheet_name='Bus Regions', skiprows=1)

    raw = pd.DataFrame(data1)
    raw = raw[['Number', 'Day Routes']]

    data2 = pd.read_excel('../data/Tube_and_Bus_Route_Stops.xls',
                          sheet_name='Bus Regions Simplified', skiprows=1)

    bus_data = pd.DataFrame(data2).iloc[:, 1:]
    bus_data['Day Routes'] = 0

    for x, poo in bus_data.iterrows():
        for y, lines in raw.iterrows():
            if x == lines['Number']:
                bus_data.loc[x, 'Day Routes'] = lines['Day Routes']

    data3 = pd.read_excel('../data/bus-service-usage-18-19.xls', sheet_name='2017-2018', skiprows=2)
    stops = [0] * len(bus_data['Day Routes'])

    for x in path:
        stops[x] = bus_data.loc[x, 'Day Routes']

    stops = [i for i in stops if i != 0]
    stops_again = []

    for y in range(len(stops)):
        if isinstance(stops[y], str):
            li = list(stops[y].split(","))
        else:
            li = str(stops[y])
        stops_again.append(li)

    bus_entries = pd.DataFrame(index=range(18), columns=['Usage']).fillna(0)
    bus_data['Usage'] = 0

    for x, find in bus_data.iterrows():
        if isinstance(find['Day Routes'], str):
            current_line = list(find['Day Routes'].split(","))
        for r in current_line:
            r = int(r)
            for s, finding in data3.iterrows():
                if r == finding['Route']:
                    find['Usage'] += finding['Usage recorded: 2017/18']
        bus_entries.iloc[x]['Usage'] = find['Usage']

    bus_entries['Group Alphabet'] = bus_data['Alphabet']
    bus_entries_again = pd.concat([bus_data['Number'], bus_entries], axis=1, join='inner')
    df3 = bus_entries_again.drop(columns=['Number']).iloc[path]
    return df3


def TubeDataframe(path):
    data = pd.read_excel('../data/multi-year-station-entry-and-exit-figures.xls',
                         sheet_name='2017 Entry & Exit (Zone 1)', skiprows=6)
    df = pd.DataFrame(data)
    df1 = pd.DataFrame(index=range(23), columns=['Usage']).fillna(0)
    df2 = df['Group Alphabet'].drop_duplicates().dropna().reset_index()

    for x, poo in df1.iterrows():
        for y, lines in df.iterrows():
            if x == lines['Group Number']:
                poo['Usage'] += lines['million']

    df3 = pd.concat([df1, df2['Group Alphabet']], axis=1, join='inner')
    df3 = df3.iloc[path, :2]
    return df3


def RenderUsageGraph(df3, title):
    fig = px.bar(df3, x="Group Alphabet", y="Usage", title="{} as of today".format(title))
    return fig


def CreateTableDataframe(mean, df3):
    data = pd.ExcelFile('../data/Tube_and_Bus_Route_Stops.xls')
    sheet = 'Tube Regions Simplified'
    if 'Bus' in mean:
        sheet = 'Bus Regions Simplified'
    df = pd.read_excel(data, sheet_name=sheet, skiprows=1)
    df = df[{'Alphabet', 'Group stations'}].rename(columns={"Group stations": "Group Stations"})
    df3 = df3.merge(df, left_on='Group Alphabet', right_on='Alphabet').drop(columns=['Alphabet', 'Usage'])
    return df3
