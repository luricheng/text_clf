import pandas as pd
import utils
from sklearn.decomposition import PCA
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sparse2dense import Sparse2Dense

"""
英文垃圾短信分类
"""

# todo Label==1的样本 数量过少
# todo 后续: 过采样???

OUTPUT_DIR = "./output"

pre_processing = Pipeline([
    ("tf-idf", TfidfVectorizer()),
    ('dense', Sparse2Dense()),
    ("stand", StandardScaler()),
    ("pca", PCA(n_components=148, random_state=1)),
])

models = [
    XGBClassifier(random_state=1, n_estimators=100, n_jobs=4),
    RandomForestClassifier(random_state=1, n_estimators=100, n_jobs=4),
    SVC(random_state=1, kernel='rbf', class_weight='balanced'),
    SGDClassifier(random_state=1, n_jobs=4)
]

if __name__ == '__main__':
    csv_data = pd.read_csv('./data/train.csv', usecols=[0, 1])
    csv_data.loc[csv_data.Label == 'spam', 'Label'] = 1
    csv_data.loc[csv_data.Label == 'ham', 'Label'] = 0
    print("csv_data:\n", csv_data.head())

    train, test = utils.df2train_test_set(csv_data, "Text", "Label", 0.7, pre_processing)

    utils.train(train, test, models, OUTPUT_DIR)
