import altair as alt
import pandas as pd

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
    title="Figure for ablation study in Table 7"
).interactive()

chart.save('/home/sf/Documents/larq/visualization/results.html')