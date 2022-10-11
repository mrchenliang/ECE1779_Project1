import base64
from io import BytesIO
from matplotlib.figure import Figure

def prepare_graph(rows):
    x_data = {'x-axis': [] }
    y_data = { 'miss_count': [], 'hit_count': [], 'request_count': [], 'cache_size': [], 'cache_count': []}
    for row in rows:
        x_data['x-axis'].append(row['created_at'])
        y_data['request_count'].append(row['request_count'])
        y_data['miss_count'].append(row['miss_count'])
        y_data['hit_count'].append(row['hit_count'])
        y_data['cache_size'].append(row['cache_size'])
        y_data['cache_count'].append(row['key_count'])
    return (x_data, y_data)


def plot_graph(data_x_axis, data_y_axis, y_label):
    fig = Figure(tight_layout=True)
    ax = fig.subplots()
    ax.plot(data_x_axis, data_y_axis)
    ax.set(xlabel='Date-Time', ylabel=y_label)
    buf = BytesIO()
    fig.autofmt_xdate()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data