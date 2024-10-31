import time 
from RATypeInfer.core.utils.data_processing import *
if __name__ == '__main__':
   #file_path = 'generated_data_1GB.csv'  
    file_path = 'err.csv'
    #file_path = 'generated_data.csv'  
    start_time_serial = time.time()
    df_serial = load_and_process(file_path)
    print(df_serial.info())
    end_time_serial = time.time()
    duration_serial = end_time_serial - start_time_serial