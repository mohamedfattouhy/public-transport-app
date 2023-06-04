"""This file contains functions for loading
   and pre-processing data."""

# MANAGE ENVIRONNEMENT
import pandas as pd
import base64


def load_data(url: str) -> pd.DataFrame:
    """Load data from url"""

    data = pd.read_csv(url, sep=';')
    data = data.drop(['stop_id', 'stop_code', 'dest_ar_code',
                     'route_short_name', 'course_sae'], axis='columns')

    return data


def create_column_text(df: pd.DataFrame) -> pd.DataFrame:
    """create a text column for display on the graph"""

    list_text = []

    for i in range(df.shape[0]):

        if df['delay_min'][i] < 60:
            text = 'Departure: ' + \
                    df['departure'][i] + \
                    '<br>Delay : ' + str(df["delay_min"][i]) + ' mins'
            list_text.append(text)

        else:
            text = 'Departure: ' + \
                    df['departure'][i] + \
                    '<br>Delay : ' + str(df["delay_hour"][i])\
                    + ' hour(s) ' + 'and ' + \
                    str(df["delay_remain_mins"][i]) + ' mins'
            list_text.append(text)

    df['text_hover'] = list_text

    return df


def render_svg(svg_file: str) -> str:
    """Manage svg to display them in the application"""

    with open(svg_file, "r") as f:
        lines = f.readlines()
        svg = "".join(lines)

        # Renders the given svg string
        b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
        html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64

        return html
