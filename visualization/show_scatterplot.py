import altair as alt
import pandas as pd

'''

Example json content, used for generating a chart of Table 9:

[
    {"accuracy": 59.1, "latency": 83.7, "size": 4.68, "model": "block: 1111"},
    {"accuracy": 58.7, "latency": 68.0, "size": 4.66, "model": "block: 0111"},
    {"accuracy": 58.4, "latency": 75.3, "size": 4.64, "model": "block: 1011"},
    {"accuracy": 58.4, "latency": 79.1, "size": 4.33, "model": "block: 1110"},
    {"accuracy": 58.1, "latency": 77.1, "size": 4.61, "model": "block: 1101"},
    {"accuracy": 58.0, "latency": 63.9, "size": 4.31, "model": "block: 0110"},
    {"accuracy": 57.9, "latency": 64.9, "size": 4.58, "model": "block: 0101"},
    {"accuracy": 57.8, "latency": 60.6, "size": 4.62, "model": "block: 0011"},
    {"accuracy": 57.8, "latency": 72.9, "size": 4.29, "model": "block: 1010"},
    {"accuracy": 56.7, "latency": 58.8, "size": 4.27, "model": "block: 0010"},
    {"accuracy": 56.7, "latency": 71.1, "size": 4.57, "model": "block: 1001"},
    {"accuracy": 56.4, "latency": 75.0, "size": 4.26, "model": "block: 1100"},
    {"accuracy": 55.9, "latency": 41.4, "size": 4.54, "model": "block: 0001"},
    {"accuracy": 55.7, "latency": 47.6, "size": 4.23, "model": "block: 0100"},
    {"accuracy": 54.9, "latency": 59.9, "size": 4.22, "model": "block: 1000"},
    {"accuracy": 53.2, "latency": 54.6, "size": 4.20, "model": "block: 0000"}
]

'''

df = pd.read_json('data_results.json')

chart = alt.Chart(df).mark_circle().encode(
    x=alt.X('latency', axis=alt.Axis(title='Latency [ms]'), scale=alt.Scale(zero=False, padding=10)),
    y=alt.Y('accuracy', axis=alt.Axis(title='ImageNet validation accuracy [%]'), scale=alt.Scale(zero=False, padding=10)),
    color=alt.Color('model', legend=alt.Legend(title="Model"), scale=alt.Scale(scheme='tableau20')),
    size=alt.Size('size', legend=alt.Legend(title="Model Size (MB)"), scale=alt.Scale(domain=[4.1, 4.8])),
    tooltip=['model', 'latency', 'accuracy', 'size'],
    
).properties(
    width=600,
    height=400,
    padding=50,
    autosize=alt.AutoSizeParams(
        type='pad',
        contains='padding'
    ),
    title="Figure for ablation study in Table 9"
).interactive()

chart.save('/home/sf/Documents/larq/visualization/results.html')