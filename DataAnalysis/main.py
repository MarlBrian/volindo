from analysis.handlers import DataAnalysis

if __name__ == '__main__':
    da = DataAnalysis()
    da.read_csv(r"C:\Users\pc\Downloads\adult_50k.csv")
    da.df = da.question_mark_cleanup()
    print("First Insight for categorical vs continuous fields --------------------")
    for r in da.continuous_or_categorical():
        print(r)
    print("Second Insight for imbalance ------------------------------------------")
    for r in da.imbalance_insight():
        print(r)
    da.oversampler()
