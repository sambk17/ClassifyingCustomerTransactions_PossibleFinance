import pandas as pd

def one_hot_get_dummies_train(X, column_selection, column_names=None):
    X_column = pd.DataFrame(X, columns=column_names)[column_selection]
    one_hot_df = pd.get_dummies(X_column[column_selection[0]].values.reshape(-1,).astype(str),
                                        drop_first=True,
                                        prefix='%s_' % column_selection[0])
    all_categories = {}
    all_categories[0] = one_hot_df.columns
    for num in range(1,len(column_selection)):
        cat_get_dummies = pd.get_dummies(X_column[column_selection[num]].values.reshape(-1,).astype(str),
                                        drop_first=True,
                                        prefix='%s_' % column_selection[num])
        one_hot_df = pd.concat([one_hot_df, cat_get_dummies], axis=1)
        all_categories[num] = cat_get_dummies.columns
    return all_categories, one_hot_df





def one_hot_get_dummies_test(X, all_categories, column_selection, column_names=None):
    X_column = pd.DataFrame(X, columns=column_names)[column_selection]
    one_hot_df = pd.get_dummies(X_column[column_selection[0]].values.reshape(-1,).astype(str),
                                        drop_first=True,
                                        prefix='%s_' % column_selection[0]).reindex(columns = all_categories[0], fill_value=0)
    for num in range(1,len(column_selection)):
        cat_get_dummies = pd.get_dummies(X_column[column_selection[num]].values.reshape(-1,).astype(str),
                                        drop_first=True,
                                        prefix='%s_' % column_selection[num]).reindex(columns = all_categories[num], fill_value=0)
        one_hot_df = pd.concat([one_hot_df, cat_get_dummies], axis=1)
    return one_hot_df