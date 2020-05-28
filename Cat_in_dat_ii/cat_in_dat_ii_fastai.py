# -*- coding: utf-8 -*-
"""Cat_in_dat_II.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1s1_p651ph8g5EzTB7wgd6YrriWffI8-v
"""

from google.colab import files
files.upload()

!mkdir -p ~/.kaggle/
!cp kaggle.json ~/.kaggle

!chmod 600 ~/.kaggle/kaggle.json

!kaggle competitions download -c cat-in-the-dat-ii

import zipfile
files = ['train.csv','test.csv']
for f in files:
  with zipfile.ZipFile(f'/content/{f}.zip') as zip_ref:
    zip_ref.extractall('/content/')

import pandas as pd
from fastai.tabular import *

df = pd.read_csv('/content/train.csv',index_col='id')
df_test = pd.read_csv('/content/test.csv',index_col = 'id')
df.head()

df.shape

cat_names =['bin_0', 'bin_1', 'bin_2', 'bin_3', 'bin_4', 'nom_0', 'nom_1', 'nom_2',
       'nom_3', 'nom_4', 'nom_5', 'nom_6', 'nom_7', 'nom_8', 'nom_9', 'ord_0',
       'ord_1', 'ord_2', 'ord_3', 'ord_4', 'ord_5', 'day', 'month']
cont_names = []
dep_var = 'target'
procs = FillMissing,Categorify,Normalize
FillMissing.fill_strategy= 'MEAN'

test = TabularList.from_df(df_test,cat_names=cat_names,cont_names=cont_names)

data = TabularList.from_df(df,cat_names=cat_names,cont_names=cont_names,procs=procs).split_by_idx(valid_idx= range(len(df)-12000,len(df))).label_from_df(cols=dep_var).add_test(test).databunch()

data.show_batch()

learn = tabular_learner(data,layers = [200,100],metrics=[accuracy,FBeta(average='weighted')])

learn.lr_find()
learn.recorder.plot()

learn.fit_one_cycle(4,1e-02)

a = df.iloc[10]
b = learn.predict(a)
b

b[2][1]

preds = learn.get_preds(ds_type=DatasetType.Test)[0][:,1].numpy()

preds

submission1 = pd.DataFrame({'id':df_test.index,'target':preds})
submission1.to_csv('/content/sub1.csv', header=True, index=False)

"""Kaggle score is 0.78352
The winning score is 0.78820

To Be done next


*   encode binary features to 0 and 1
*   encode ordinal features to 1-hot
*   Convert day and month to date-time series
*   Feed to the model
"""