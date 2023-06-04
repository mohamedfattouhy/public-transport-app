# MANAGE ENVIRONNEMENT
import os
import streamlit as st
import plotly.express as px
from load_data import load_data, render_svg


url = "https://data.montpellier3m.fr/sites/default/files/ressources/TAM_MMM_TpsReel.csv"
data = load_data(url=url)

st.set_page_config(layout='centered')

# Create a sidebar to explain
# the purpose of the application
logo_sidebar_path = os.path.join('static', 'logo_sidebar.PNG')
st.sidebar.image(logo_sidebar_path)

st.sidebar.markdown('\n')
st.sidebar.markdown('\n')

st.sidebar.markdown("This application is based on real-time\
                    public transport traffic in Montpellier 🚋")
st.sidebar.markdown("Here you can find: <ol><li>Timetables for upcoming arrivals 🕑</li>\
                    <li>Graphs showing traffic trends <br> in real time 📈</li></ol>",
                    unsafe_allow_html=True)

new_names = {'trip_headsign': 'destination',
             'stop_name': 'stop',
             'departure_time': 'departure'}

data = data.rename(columns=new_names)

data['delay_min'] = data['delay_sec'] / 60
data['delay_min'] = data['delay_min'].astype(int)

# Title of the app
st.markdown("""## Real-time public transport traffic in Montpellier""")

st.markdown('\n')
st.markdown('\n')

# Page split into 4 columns
col1_img, col2_img, col3_img, col4_img = st.columns([1, 1, 0.5, 1])

with col2_img:
    svg_tram_path = os.path.join('static', 'tramway.svg')
    svg_tram = render_svg(svg_file=svg_tram_path)
    st.markdown(svg_tram, unsafe_allow_html=True)

with col3_img:
    svg_bus_path = os.path.join('static', 'bus.svg')
    svg_bus = render_svg(svg_file=svg_bus_path)
    st.markdown(svg_bus, unsafe_allow_html=True)

st.markdown('\n')
st.markdown('\n')

# Page split into 2 columns
col1, col2 = st.columns(2)

with col1:
    trip_headsigns = data['destination'].unique()
    selected_destination = st.selectbox("Select a destination", trip_headsigns)

with col2:
    stop_list = data['stop'].unique()
    selected_arret = st.selectbox("Select a stop", stop_list)

# Page split into 3 columns
col1_box, col2_box, col3_box = st.columns([1, 2, 1])

# Contenu de la colonne centrale
with col2_box:
    filtered_data = data[data['destination'] == selected_destination]
    filtered_data = filtered_data[filtered_data['stop'] == selected_arret]\
                                                         .set_index('stop')
    st.markdown('\n')
    st.write("Timetable for destination :", selected_destination)
    st.dataframe(filtered_data[['departure']], width=280)

data['text_hover'] = 'Departure: ' + data['departure'].astype(str) + \
                     '<br>Delay : ' + data["delay_min"].astype(str) + \
                     ' mins'

# Create a bar chart with Plotly
fig = px.bar(filtered_data, x='departure', y='delay_min',
             title=f'Bus delay at stop: {selected_arret}',
             color='delay_min',
             color_continuous_scale=px.colors.sequential.Blues)

fig.update_layout(xaxis_title='Departure time',
                  yaxis_title='Time to arrival (in min)')
fig.update_traces(hovertemplate=data["text_hover"])

# Change colorbar title
fig.update_coloraxes(colorbar_title='Delay (sec)')

# Display the graph in app
st.plotly_chart(fig)
