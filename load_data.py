# MANAGE ENVIRONNEMENT
import pandas as pd
import base64


def load_data(url: str) -> pd.DataFrame:
    """Load data from url"""

    data = pd.read_csv(url, sep=';')
    data = data.drop(['stop_id', 'stop_code', 'dest_ar_code',
                     'route_short_name', 'course_sae'], axis='columns')

    return data


def render_svg(svg_file: str) -> str:
    """Manage svg to display them in the application"""

    with open(svg_file, "r") as f:
        lines = f.readlines()
        svg = "".join(lines)

        # Renders the given svg string
        b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
        html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64

        return html
