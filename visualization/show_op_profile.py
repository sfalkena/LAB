import pandas as pd
import altair as alt
import os

['Operator-wise', ]
def get_df_from_file(file_path, type='run_order'):
    if type == 'run_order':
        start_phrase = 'Operator-wise Profiling Info for Regular Benchmark Runs:'
        end_phrase = 'Top by Computation Time'
        df = pd.read_csv(file_path, skip_blank_lines=False, header=get_line_number(file_path, start_phrase, 1)+1, 
                         nrows=get_line_number(file_path, end_phrase, 2) - get_line_number(file_path, start_phrase, 1)-4,
                         skipinitialspace=True)  
        return df

def get_line_number(file, phrase, occurances):
    cnt = 0
    with open(file) as myFile:
        for num, line in enumerate(myFile, 1):
            if phrase in line:
                cnt += 1
                if cnt == occurances:
                    return num
        return -1
    
def add_name_column_to_df(df, name):
    df['model']=name
    return df

def operator_profile_chart(folder_name, modelnames, replace_nodes=None):
    models = [x.split('.')[0] for x in os.listdir(f"visualization/{folder_name}") if x.endswith('.csv')]
    final_df = pd.DataFrame()
    for i, model in enumerate(models):
        filename = f'visualization/{folder_name}/{model}.csv'
        df = get_df_from_file(filename)
        df = add_name_column_to_df(df, modelnames[i])
        final_df = final_df.append(df)
    
    if replace_nodes:
        final_df.replace(regex=replace_nodes, value='OTHER', inplace=True)
    bars = alt.Chart(final_df).mark_bar().encode(
        order=alt.Order(
            'index:O',
            sort='ascending'
        ),
        x=alt.X('avg_ms:Q', title='Latency [ms]'),
        y=alt.X('model:N', title='Model'),
        color='node type:N',
        tooltip=['node type', 'avg_ms'],
    ).configure_legend(
        orient='bottom'
    ).configure_axis(
    labelFontSize=20,
    titleFontSize=20
)
    
    chart = (bars ).properties(width=1250, height=300, title='Detailed version of Fig. 6 (Interactive)').interactive()    
    chart.save(f'visualization/{folder_name}.html')

if __name__ == "__main__":
    folder_name = "ablation"
    # The name given to the models found in the folder.
    modelnames = ['D:', 'C:', 'B:', 'A:']
    # Use replace_nodes if you want to replace certain operations by "OTHER". Might be useful for visualization.
    replace_nodes = ['NOT_EQUAL', 'PRELU', 'RESHAPE', 'SOFTMAX', 'BROADCAST_TO', 'AVERAGE_POOL_2D', 'LceQuantize', 'MUL', 'ADD', 'FULLY_CONNECTED']
    
    operator_profile_chart(folder_name, modelnames, replace_nodes)


