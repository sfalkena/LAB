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

def main():
    folder_name='ablation'
    # models = ['xnornet_org', 'xnornet_dw', 'brn_org', 'brn_dw', 'ran_org', 'ran_dw', 'quicknet_large', 'quicknet_org', 'quicknet_dw_sign', 'quicknet_dw', 'quicknet_new_bin']
    models = [x.split('.')[0] for x in os.listdir(f"/home/sf/Documents/larq/visualization/{folder_name}") if x.endswith('.csv')]
    # models = ['brn_org', 'brn_org_prelu', 'brn_dw_prelu', 'brn_dw_sign_prelu', 'brn_dw_sign_beta_prelu', 'brn_dw_prelu_stem']
    modelnames = ['D:', 'C:', 'B:', 'A:']
    replace_nodes = ['NOT_EQUAL', 'PRELU', 'RESHAPE', 'SOFTMAX', 'BROADCAST_TO', 'AVERAGE_POOL_2D', 'LceQuantize', 'MUL', 'ADD', 'FULLY_CONNECTED']
    print(models)
    final_df = pd.DataFrame()
    for i, model in enumerate(models):
        filename = f'/home/sf/Documents/larq/visualization/{folder_name}/{model}.csv'
        df = get_df_from_file(filename)
        df = add_name_column_to_df(df, modelnames[i])
        final_df = final_df.append(df)
    print(final_df)
    
    # final_df.replace(regex=replace_nodes, value='OTHER', inplace=True)
    # final_df.replace(regex='LceBconv2d', value='BINARY_CONV2D', inplace=True)
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
    
    text = alt.Chart(final_df).mark_text(dx=-15, dy=3, color='white').encode(
        order=alt.Order(
            'index:O',
            sort='ascending'
        ),
    x=alt.X('avg_ms:Q', stack='zero'),
    y=alt.Y('model:N'),
    text=alt.Text('avg_ms:Q', format='.1f'))
    chart = (bars ).properties(width=1250, height=300, title='Detailed version of Fig. 6 (Interactive)').interactive()    
    chart.save(f'/home/sf/Documents/larq/visualization/{folder_name}.html')



main()