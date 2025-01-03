import traceback
import argparse
from logger import LOGGER
import os
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--shell-num', type=int)
args = parser.parse_args()
shell = args.shell_num

def merging():
    # Define the directory path where the result_i directories are located
    directory_path = "/yopo-artifact/WebGraph/result_adflush_{}".format(shell)

    # Initialize empty DataFrames for each type
    merged_features = pd.DataFrame()
    merged_graph = pd.DataFrame()
    merged_labelled = pd.DataFrame()

    # Iterate over the result_i directories
    for i in range(16):
        print(i)
        result_dir = os.path.join(directory_path, f"result_{i}")
        
        # Read the CSV files for each type
        features_file = os.path.join(result_dir, "features.csv")
        graph_file = os.path.join(result_dir, "graph.csv")
        labelled_file = os.path.join(result_dir, "labelled.csv")
        
        # Read CSV files into DataFrames
        features_df = pd.read_csv(features_file)
        graph_df = pd.read_csv(graph_file)
        labelled_df = pd.read_csv(labelled_file)
        
        # Merge DataFrames for each type
        merged_features = pd.concat([merged_features, features_df])
        merged_graph = pd.concat([merged_graph, graph_df])
        merged_labelled = pd.concat([merged_labelled, labelled_df])

    # Save the merged DataFrames to new CSV files
    merged_features.to_csv("/yopo-artifact/WebGraph/result_adflush_{}/merged_features.csv".format(shell), index=False)
    merged_graph.to_csv("/yopo-artifact/WebGraph/result_adflush_{}/merged_graph.csv".format(shell), index=False)
    merged_labelled.to_csv("/yopo-artifact/WebGraph/result_adflush_{}/merged_labelled.csv".format(shell), index=False)
    
def merging_unmod():
    # Define the directory path where the result_i directories are located
    directory_path = "/yopo-artifact/WebGraph/result"

    # Initialize empty DataFrames for each type
    merged_features = pd.DataFrame()
    merged_graph = pd.DataFrame()
    merged_labelled = pd.DataFrame()

    for i in range(16):
        result_dir = os.path.join(directory_path, f"result_adflush_{i}")
        
        # Read the CSV files for each type
        features_file = os.path.join(result_dir, "features.csv")
        graph_file = os.path.join(result_dir, "graph.csv")
        labelled_file = os.path.join(result_dir, "labelled.csv")
        
        # Read CSV files into DataFrames
        features_df = pd.read_csv(features_file)
        graph_df = pd.read_csv(graph_file)
        labelled_df = pd.read_csv(labelled_file)
        
        # Merge DataFrames for each type
        merged_features = pd.concat([merged_features, features_df])
        merged_graph = pd.concat([merged_graph, graph_df])
        merged_labelled = pd.concat([merged_labelled, labelled_df])

    # Save the merged DataFrames to new CSV files
    merged_features.to_csv("/yopo-artifact/WebGraph/result/merged_features.csv", index=False)
    merged_graph.to_csv("/yopo-artifact/WebGraph/result/merged_graph.csv", index=False)
    merged_labelled.to_csv("/yopo-artifact/WebGraph/result/merged_labelled.csv", index=False)

def add_label():
    df_a = pd.read_csv('/yopo-artifact/WebGraph/result_adflush_{}/merged_features.csv'.format(shell))
    df_b = pd.read_csv('/yopo-artifact/WebGraph/result_adflush_{}/merged_labelled.csv'.format(shell))

    # Merge the two dataframes on 'visit_id' and 'name'
    df_c = pd.merge(df_a, df_b[['name', 'label', 'top_level_url']], on=['name'], how='left').drop_duplicates(subset='name', keep='first')

    df_c.drop(columns=['Unnamed: 0'], inplace=True)
    df_c = df_c.dropna(subset=["label"])
    
    specific_column = df_c['top_level_url']
    df_c = df_c.drop(columns=['top_level_url'])
    df_c.insert(0, 'top_level_url', specific_column)
    
    # Drop any duplicated rows based on all columns
    # df_c.drop_duplicates(keep='first', inplace=True)
    
    df_c.rename(columns={'label': 'CLASS'}, inplace=True)
    
    # Save the merged dataframe to a new CSV file c.csv
    df_c.to_csv('/yopo-artifact/WebGraph/result_adflush_{}/merged_features_with_labelled.csv'.format(shell), index=False)

def add_label_unmod():
    df_a = pd.read_csv('/yopo-artifact/WebGraph/result/merged_features.csv'.format(shell))
    df_b = pd.read_csv('/yopo-artifact/WebGraph/result/merged_labelled.csv'.format(shell))

    # Merge the two dataframes on 'visit_id' and 'name'
    df_c = pd.merge(df_a, df_b[['name', 'label', 'top_level_url']], on=['name'], how='left').drop_duplicates(subset='name', keep='first')

    df_c.drop(columns=['Unnamed: 0'], inplace=True)
    df_c = df_c.dropna(subset=["label"])
    
    specific_column = df_c['top_level_url']
    df_c = df_c.drop(columns=['top_level_url'])
    df_c.insert(0, 'top_level_url', specific_column)
    
    # # Drop any duplicated rows based on all columns
    # df_c.drop_duplicates(keep='first', inplace=True)
    
    df_c.rename(columns={'label': 'CLASS'}, inplace=True)
    
    # Save the merged dataframe to a new CSV file c.csv
    df_c.to_csv('/yopo-artifact/WebGraph/result/merged_features_with_labelled_adflush.csv'.format(shell), index=False)

merging()
add_label()

# merging_unmod()
# add_label_unmod()
