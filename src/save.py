import pandas as pd

def save_to_csv(data, output_path):
    """
    Save the DataFrame to a CSV file.
    
    Parameters:
    data (pd.DataFrame): The DataFrame to save.
    output_path (str): The path where the CSV file will be saved.
    """
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Data saved to {output_path}")