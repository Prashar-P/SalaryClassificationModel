import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def data_analysis(df):
    print(df.shape)
    print(df.info())
    print(df.describe())
    print(df.nunique())
    print(df.isnull().sum())
    print(df.duplicated().sum())
    print(df.head(30))


def data_preprocessing(df):
    """
    Aims to preprocess the data so that is in the correct format for training:
    This includes:
    - removing spaces
    - removing null data
    - removing  duplicate data
    - converting categorical data to numerical
    - handling of outliers
    """
    print("PRE-PROCESSING")
    #data_analysis(df)
    remove_spaces(df)
    feature_selection(df)
    remove_null_values(df)
    remove_duplicates(df)
    convert_categorical_to_numerical(df)
    # plt_data(df)
    handle_outliers(df)
    print(df.size)


def train_data():
    """
    Trains  data in order to make predictions based on the data provided.
    """
    print("training")


def remove_null_values(df):
    """
    Remove any null values. Null values are represented as '?' in the salary dataset used.
    """
    # set  ? to be null values
    df.replace("?", pd.NA, inplace=True)
    null_values = df.isnull().sum().sum()
    if (null_values) > 0:
        print("Null Values are present... removing relevant data samples")
        df.dropna(inplace=True)
    return df


def remove_duplicates(df):
    """
    Remove all duplicate entries in the dataset
    """
    duplicate_values = df.duplicated().sum()
    if duplicate_values > 0:
        print("Duplicate data was found. Removing duplicate data...")
        df.drop_duplicates(keep="first", inplace=True)
    return df


def remove_spaces(df):
    """
    Remove spaces found in the dataset
    """
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].map(str.strip)
    return df


def convert_categorical_to_numerical(df):
    """
    Converts all categorical data to numerical
    """
    # <=50K = 0 >=50K = 1
    from sklearn import preprocessing

    le = preprocessing.LabelEncoder()
    categorical_columns = df.select_dtypes(include="object").columns
    for col in categorical_columns:
        df[col] = le.fit_transform(df[col].astype(str))
    return df


def handle_outliers(df):
    """
    Removes any outliers found in df.
    """
    print("handling outliers .. ")
    from scipy import stats
    from scipy.stats import zscore

    df = df[(np.abs(stats.zscore(df)) < 3).all(axis=1)]
    return df


def feature_selection(df):
    """
    Plot data for comparisons as a boxplot/scatter and heatmap
    """
    df.drop(['fnlwgt', 'marital-status', 'relationship'], axis=1, inplace=True)
    return df



def plt_data(df):
    """
    Plot data for comparisons as a boxplot/scatter and heatmap
    """
    #https://stackoverflow.com/questions/61526812/boxplot-for-all-data-in-dataframe-error-numpy-ndarray-object-has-no-attribut

    columns = list(df.columns)
    print(len(columns)/5)
    f, axs = plt.subplots(round(len(columns)/6), 6, figsize=(20,15))
    f.suptitle("salary: 0 = <50k , 1 = >50k")
    a = 0
    for col in columns:    
        i, j = divmod(a, 6)
        sns.boxplot(data=df, y=col, x="salary", ax=axs[i,j]).set_title(("Outliers in category " + col))
        a = a + 1
    plt.tight_layout()

    # sns.boxplot(data=df, y=col, x="salary").set_title("Outliers in the age category")
    sns.catplot(data=df, y="occupation", hue="salary", kind="count", palette="pastel")
    plt.figure(figsize=(15, 10))
    sns.heatmap(df.corr(), annot=True)
    plt.title('Correlation matrix for salary predictions')

 