from util import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import roc_curve, auc, precision_recall_curve
from sklearn.metrics import classification_report
from matplotlib import pyplot as plt
from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
import numpy as np
import pandas as pd


def label_reviews(data, text='review_text', label='review_rating'):
    """
    label reviews by rating percentile, 0 for low, 1 for high
    """
    # filter the reviews do not have the label value
    data = data[data[label].notnull()]
    label_based_col = data[label]
    data['label'] = pd.qcut(label_based_col, [0, 1 / 2, 1], labels=False)
    # data['label'] = np.where(data['review_rating'] >= 8.3, 1, 0)
    # only keep the review text and label
    data = data[[text, 'label']]
    # reassigned the number of the dataframe
    data = data.reset_index(drop=True)
    return data


def get_tfidf(data):
    tfidf_vect = TfidfVectorizer()
    dtm = tfidf_vect.fit_transform(data['review_text'])
    voc_lookup = {tfidf_vect.vocabulary_[word]: word for word in tfidf_vect.vocabulary_}
    doc0 = dtm[0].toarray()[0]
    top_words = doc0.argsort(doc0)[::-1][0:10]
    print("top words for document")
    for i in top_words:
        print("{0}:\t{1:.3f}".format(voc_lookup[i], doc0[i]))
    x_train, x_test, y_train, y_test = train_test_split(dtm, data["label"], test_size=0.3, random_state=0)


def create_model(x_train, y_train, x_test, y_test,
                 model_type="svm", min_df=1, stop_words=None,
                 print_result=True, algorithm_para=1.0):
    # vectorize the train and test data
    tfidf_vect = TfidfVectorizer(stop_words=stop_words, min_df=min_df)
    x_train_tfidf = tfidf_vect.fit_transform(x_train)

    if model_type == "svm":
        model = svm.LinearSVC(C=algorithm_para)
        clf = model.fit(x_train_tfidf, y_train)
    elif model_type == "nb":
        model = MultinomialNB(alpha
                              =algorithm_para)
        clf = model.fit(x_train_tfidf, y_train)
    else:
        print("Please input correct model type")
        return None

    x_transformed = tfidf_vect.transform(x_test)
    predict_p = clf.predict_proba(x_transformed) if model_type == "nb" \
        else clf.decision_function(x_transformed)
    predict = clf.predict(x_transformed)

    if print_result:
        print(classification_report(y_test, predict))
    precision, recall, fscore, support = precision_recall_fscore_support(y_test, predict, average='binary')

    # plot the roc and prc curve

    fpr, tpr, thresholds = roc_curve(y_test, predict_p) if model_type == "svm" \
        else roc_curve(y_test, predict_p[:, 1])
    precision, recall, thresholds = precision_recall_curve(y_test, predict_p) if model_type == "svm" \
        else precision_recall_curve(y_test, predict_p[:, 1])
    prc_score = auc(recall, precision)
    auc_score = auc(fpr, tpr)

    if print_result:
        print("AUC : {:.2%}".format(auc_score) + "  PRC : {:.2%}".format(prc_score))
        plt.plot(fpr, tpr)
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        if model_type == "svm":
            plt.title('SVM-AUC')
        elif model_type == "nb":
            plt.title('nb-AUC')
        # plt.title('ROC curve')
        # plt.legend(loc="lower right")
        plt.show()

        plt.plot(recall, precision)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        if model_type == "svm":
            plt.title('SVM-PRC')
        elif model_type == "nb":
            plt.title('nb-PRC')
        # plt.legend(loc="lower right")
        plt.show()

    return auc_score, prc_score


def search_para(docs, y):
    # define the pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', svm.LinearSVC())
    ])
    parameters = {'tfidf__min_df': [1, 2, 5, 10],
                  'tfidf__stop_words': [None, "english"],
                  'clf__C': [0.5, 1.0, 2.0],
                  }
    # define the grid search
    grid_search = GridSearchCV(pipeline, param_grid=parameters, cv=5, scoring='f1_macro')
    # fit the grid search
    grid_search.fit(docs, y)
    # report the best configuration
    print(grid_search.best_params_)
    print(grid_search.best_score_)


def sample_size_impact(docs, y):
    svm_aucs = []
    nb_aucs = []
    for i in [float(i) / 10 for i in range(1, 9)]:
        x_train, x_test, y_train, y_test = train_test_split(docs, y, test_size=1 - i, random_state=0)
        for mt in ['svm', 'nb']:
            auc_score, prc_socre = create_model(x_train, y_train, x_test, y_test,
                                                model_type=mt, stop_words='english', print_result=False)
            if mt == 'svm':
                svm_aucs.append(auc_score)
            else:
                nb_aucs.append(auc_score)

    # plot a line chart show the relationship between sample size and the AUC score.
    plt.plot([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], svm_aucs, label='svm')
    plt.plot([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], nb_aucs, label='nb')
    plt.xlabel('Sample Size')
    plt.ylabel('AUC Score')
    plt.legend()
    plt.show()


def get_helpfulness_rate(data):
    upvote = data['review_helpfulness_upvote']
    total = data['review_helpfulness_total']
    data['helpfulness_rate'] = upvote / total
    return data
