import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cv2



df = pd.read_csv('cocomelon/cocomelon_stats_ready.csv')
  
# Contrast  
fig, ax = plt.subplots()
plt.yscale("log")
plt.plot(df['saturation'], df['viewCount'], 'o')
plt.xlabel("saturation")
plt.ylabel("Views")
plt.show()
