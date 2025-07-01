import pandas as pd

def read_excel_file(file_path):

    df = pd.read_excel(file_path, header=None)

    fixed_images = [str(x) if pd.notna(x) else '' for x in df.iloc[0, 1:]]
    fixed_count = len(fixed_images) - (1 if '' in fixed_images else 0)

    moving_images = []
    for i in range(1, len(df)):
        row = [str(x) for x in df.iloc[i, 1:] if pd.notna(x) and str(x).strip() != '']
        if row:
            moving_images.append(row)
    moving_count = len(moving_images)

    return fixed_count, moving_count, fixed_images, moving_images