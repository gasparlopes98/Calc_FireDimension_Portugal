import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cv2

df = pd.read_csv('cocomelon/cocomelon_stats.csv')

# Removing irrelevant data
df.pop('title')
df.pop('description')
df.pop('localizations.en.description')
df.pop('snippet.tags')
df.pop('kind_stats')
df.pop('contentDetails.dimension')
df.pop('topicDetails.topicCategories')
df.pop('snippet.defaultLanguage')
df.pop('localizations.en.title')
df.pop('commentCount')
df.pop('contentDetails.duration')
df.pop('thumbnails.medium.height')
df.pop('thumbnails.high.width')
df.pop('thumbnails.high.height')
df.pop('thumbnails.medium.width')
df.pop('thumbnails.default.height')
df.pop('thumbnails.default.width')
df.pop('thumbnails.default.url')
df.pop('thumbnails.medium.url')
df.pop('thumbnails.high.url')

# Creating new Column
df['contrast'] = 0
df['hue'] = 0
df['saturation'] = 0
df['brightness'] = 0

######################
# Cut Black Borders
######################
# for i in range(len(df)):
#     img = cv2.imread('cocomelon/thumbnails/{}.jpg'.format(df.loc[i, 'id']),3)
#     crop_img = img[45:315,:] # Take off Black Borders
#     cv2.imwrite('cocomelon/thumbnails_ready/{}.jpg'.format(df.loc[i, 'id']), crop_img)

# Adding values to contrast
for i in range(len(df)):
    img = cv2.imread('cocomelon/thumbnails_ready/{}.jpg'.format(df.loc[i, 'id']),0)
    df.loc[i, 'contrast'] = round(img.std(),3)
    
# Adding values to saturation
for i in range(len(df)):
    img = cv2.imread('cocomelon/thumbnails_ready/{}.jpg'.format(df.loc[i, 'id']))
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    df.loc[i, 'saturation'] = round(img_hsv[:, :, 1].mean())
    
######################
# Dominant Colors
######################
# dominant_colors=[]
# # Adding values to dominant_color
# for i in range(len(df)):
#     img = cv2.imread('cocomelon/thumbnails_ready/{}.jpg'.format(df.loc[i, 'id']))
#     height, width, _ = np.shape(img)

#     data = np.reshape(img, (height * width, 3))
#     data = np.float32(data)

#     number_clusters = 3
#     criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
#     flags = cv2.KMEANS_RANDOM_CENTERS
#     _, _, centers = cv2.kmeans(data, number_clusters, None, criteria, 10, flags)
#     dominant_colors.append(centers.astype(int))
    
# print(dominant_colors)
# # with open('cocomelon/dominant_color.npy', 'wb') as f:
# #     np.save(f, dominant_colors)

# Adding values to hue  
for i in range(len(df)):
    img = cv2.imread('cocomelon/thumbnails_ready/{}.jpg'.format(df.loc[i, 'id']),cv2.COLOR_RGB2HSV) # open as HSV color space
    df.loc[i, 'hue'] = round(np.mean(img[0]))
 
# Saving new data base
df.to_csv('cocomelon/cocomelon_stats_ready.csv')
print(df.head(5))