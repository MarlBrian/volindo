import pandas as pd
import numpy as np
from collections import Counter
from imblearn.over_sampling import SMOTENC
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, roc_auc_score
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


class BaseDataHandler:
    def __init__(self):
        self.df = pd.DataFrame()

    def read_csv(self, file):
        self.df = pd.read_csv(file)


class DataCleaner(BaseDataHandler):
    def question_mark_cleanup(self) -> pd.DataFrame:
        return self.df.replace('?', np.nan)


class DataAnalysis(DataCleaner):
    def imbalance_insight(self) -> list:
        insight_box = []
        for column in self.df:
            insight = f"{column} - "
            col_values = self.df[column].dropna()
            col_unique = col_values.nunique()
            if col_values.dtype == 'object':
                insight += f"categorical - {self.imbalance_analysis(col_values, col_unique)}"
            else:
                if col_unique > 10:
                    insight += f"continuous - balanced"
                else:
                    insight += f"categorical - {self.imbalance_analysis(col_values, col_unique)}"
            insight_box.append(insight)
        return insight_box

    def continuous_or_categorical(self) -> list:
        insight_box = []
        for column in self.df:
            insight = f"{column} - "
            col_values = self.df[column].dropna()
            col_unique = col_values.nunique()
            if col_values.dtype == 'object':
                insight += f"categorical - {col_unique} values - {', '.join(col_values.unique().tolist())}"
            else:
                if col_unique > 10:
                    insight += f"continuous - {col_unique} values - {self.get_num_range(col_values)}"
                else:
                    insight += f"categorical - {col_unique} values - {', '.join(col_values.unique().tolist())}"
            insight_box.append(insight)
        return insight_box

    @staticmethod
    def get_num_range(df_data: pd.DataFrame) -> str:
        return f"{df_data.min()} to {df_data.max()}"

    @staticmethod
    def imbalance_analysis(col_values: pd.DataFrame, unique_values: int) -> str:
        imbalance_str = ''
        imbalanced = False
        min_occurrence = 100 / unique_values / 10
        imb_percentages = col_values.value_counts(normalize=True)*100
        for name, p in imb_percentages.items():
            if p < min_occurrence:
                imbalanced = True
            imbalance_str += f"{name} {p:.2f}%, "
        return f"{'balanced' if not imbalanced else 'imbalanced'} - {min_occurrence:.2f}% min ocurrence - {imbalance_str[:-2]}"

    def balance_dataframe(self):
        self.df = self.df.dropna()
        X = self.df.iloc[:, :]
        y = self.df.iloc[:, 4]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)
        print("Before oversampling: ", Counter(y_train))
        smt = SMOTENC([1,3,4,5,6,7,8,10,12])
        X_train_SMOTE, y_train_SMOTE = smt.fit_resample(X_train, y_train)
        print("After oversampling: ", Counter(y_train_SMOTE))
        model = SVC()
        clf_SMOTE = model.fit(X_train_SMOTE, y_train_SMOTE)
        pred_SMOTE = clf_SMOTE.predict(X_test)
        print("ROC AUC score for oversampled SMOTE data: ", roc_auc_score(y_test, pred_SMOTE))
        return