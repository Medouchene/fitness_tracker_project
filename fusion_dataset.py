import pandas as pd
from glob import glob

files = glob("MetaMotion/MetaMotion/*.csv")
print("There is", len(files), "files")

#extract features

data_path = "MetaMotion/MetaMotion/"

def read_data(files):

    acc_df = pd.DataFrame()
    gyr_df = pd.DataFrame()

    acc_set = 1
    gyr_set = 1

    for f in files :
        participant = f.split("-")[0].replace(data_path, "")
        label = f.split("-")[1]
        category = f.split("-")[2].rstrip("123").rstrip("_MetaWear_2019")

        df = pd.read_csv(f)
        df["participant"] = participant
        df["label"] = label
        df["category"] = category

        if "Accelerometer" in f:
            df["set"] = acc_set   
            acc_set += 1
            acc_df = pd.concat([acc_df, df]) 

        if "Gyroscope" in f:
            df["set"] = gyr_set   
            gyr_set += 1
            gyr_df = pd.concat([gyr_df, df]) 
        
    acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit = "ms")
    gyr_df.index = pd.to_datetime(gyr_df["epoch (ms)"], unit = "ms")

    del acc_df["epoch (ms)"]
    del acc_df["time (01:00)"]
    del acc_df["elapsed (s)"]    

    del gyr_df["epoch (ms)"]
    del gyr_df["time (01:00)"]
    del gyr_df["elapsed (s)"]        

    return acc_df, gyr_df


acc_df, gyr_df = read_data(files)

data = pd.concat([acc_df.iloc[:, :3], gyr_df], axis = 1)
data.to_csv('dataset_fitness_tracker.csv', index=False)
print(data.head(50))