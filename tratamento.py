import numpy as np
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

# for i in range(len(df)):
#     img = cv2.imread('cocomelon/thumbnails/{}.jpg'.format(df.loc[i, 'id']),3)
#     crop_img = img[45:315,:] # Take off Black Borders
#     cv2.imwrite('cocomelon/thumbnails_ready/{}.jpg'.format(df.loc[i, 'id']), crop_img)

# Adding values to contraste
for i in range(len(df)):
    img = cv2.imread('cocomelon/thumbnails_ready/{}.jpg'.format(df.loc[i, 'id']),0)
    df.loc[i, 'contrast'] = img.std()

# Saving new data base
df.to_csv('cocomelon/cocomelon_stats_ready.csv')
print(df.head(5))