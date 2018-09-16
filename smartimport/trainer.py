#!/usr/bin/env python

import os
import pickle
import importlib
import itertools

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import cross_validate, train_test_split
from sklearn.metrics import confusion_matrix

from smartimport import settings, str2features, types

# from visualization.confusion_matrix import plot_confusion_matrix

MK_PURPLE = (87 / 255, 68 / 255, 96 / 255)
MK_GREEN = (175 / 255, 177 / 255, 63 / 255)
MK_BLUE = (30 / 255, 135 / 255, 104 / 255)
MK_GRAY = (32 / 255, 28 / 255, 27 / 255)


def plot_confusion_matrix(cm, classes, title="Confusion matrix", cmap=plt.cm.Purples):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
    plt.imshow(cm, interpolation="nearest", cmap=cmap)
    plt.title(title, color=MK_GREEN, fontweight="bold")
    plt.colorbar()
    tick_marks = np.arange(len(classes))

    plt.xticks(tick_marks, classes, rotation=90, fontsize=8)
    plt.yticks(tick_marks, classes, fontsize=8)
    fmt = ".1f"
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(
            j,
            i,
            format(cm[i, j], fmt),
            horizontalalignment="center",
            color="white" if cm[i, j] > thresh else "black",
            fontsize=8,
        )

    plt.tight_layout()
    plt.ylabel("True label", color=MK_GREEN, fontweight="bold")
    plt.xlabel("Predicted label", color=MK_GREEN, fontweight="bold")


def prepare_for_learning(df, algo):
    """ Prepare data for learning purpose """
    df = df.copy()

    # Convert text to feature
    df["data"] = df["data"].apply(lambda x: algo.convert(x))

    # Convert to 1D vector
    features = np.ndarray((df.shape[0], algo.nb_features()), dtype=np.int8)

    # store in numpy array (can't be done directly with apply method of DataFrame)
    for idx, feature in enumerate(df["data"].values):
        features[idx] = feature

    guessable_types = types.get_all_guessable_types()

    df["type"] = df["type"].apply(lambda x: guessable_types[x].label)

    return features, df.type.values


def train(display_confusion_matrix=False, save_model=True):
    """ Actually train the model from the given data file """

    model_path, options = settings.TRAINING_MODEL

    model_module_path, _, clazz = model_path.rpartition(
        "."
    )  # Get module and class to load
    model_module = importlib.import_module(model_module_path)  # Load module

    model = getattr(model_module, clazz)(**options)  # Create model instance with option

    print(
        f"Use {model_path} module for training with "
        f"str2feature algo {settings.STR2FEATURES_CONF['algo']}"
    )

    # get algo to compute features
    conf = dict(settings.STR2FEATURES_CONF)
    algo_features = getattr(str2features, conf.pop("algo"))(**conf)

    training_data = pd.read_csv(settings.TRAINING_DATA_PATH, dtype="str")

    # features, labels, nb_labels, labels_names = prepare_for_learning(training_data, algo_features)
    features, labels = prepare_for_learning(training_data, algo_features)

    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.33
    )

    model.fit(X_train, y_train)  # Train model

    scores = cross_validate(model, features, labels, cv=5)  # Cross validate

    print(
        "Accuracy: %0.2f (+/- %0.2f)"
        % (scores["test_score"].mean(), scores["test_score"].std() * 2)
    )
    print("Time : %0.2f seconds" % (scores["fit_time"].mean()))

    if display_confusion_matrix:
        y_pred = model.predict(X_test)  # Try to predict

        # labels_names = [t.label for t in types.get_all_guessable_types()
        all_types = types.get_all_guessable_types()
        labels = [(c.label, k) for k, c in all_types.items()]
        labels.sort()

        # Compute confusion matrix
        cnf_matrix = confusion_matrix(y_test, y_pred)

        # plot normalized confusion matrix
        plt.figure(figsize=(20, 10))
        plot_confusion_matrix(
            cnf_matrix, classes=[e[1] for e in labels], title="Confusion matrix"
        )
        plt.show()

    if save_model:  #  Save model as pickle file
        with open(os.path.join(settings.MODEL_PATH), "wb") as model_file:
            pickle.dump(model, model_file)
