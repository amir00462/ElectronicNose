import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report


def main():
    # Load the data from Excel
    data = pd.read_excel("processed_data.xlsx")

    # Split the data into features and labels
    X = data.iloc[:, :-1]  # Features
    y = data.iloc[:, -1]  # Labels

    # Split the data into training and testing sets (80% training, 20% testing)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the SVM model
    svm_model = SVC()
    svm_model.fit(X_train, y_train)

    # Train the Decision Tree model
    decision_tree_model = DecisionTreeClassifier()
    decision_tree_model.fit(X_train, y_train)

    # Train the Random Forest model
    random_forest_model = RandomForestClassifier()
    random_forest_model.fit(X_train, y_train)

    # Train the KNN model
    knn_model = KNeighborsClassifier()
    knn_model.fit(X_train, y_train)

    # Train the Naive Bayes model
    naive_bayes_model = GaussianNB()
    naive_bayes_model.fit(X_train, y_train)

    # Train the Neural Network model
    neural_network_model = MLPClassifier()
    neural_network_model.fit(X_train, y_train)

    # Make predictions on the test set
    svm_predictions = svm_model.predict(X_test)
    decision_tree_predictions = decision_tree_model.predict(X_test)
    random_forest_predictions = random_forest_model.predict(X_test)
    knn_predictions = knn_model.predict(X_test)
    naive_bayes_predictions = naive_bayes_model.predict(X_test)
    neural_network_predictions = neural_network_model.predict(X_test)

    # Calculate classification reports for each algorithm
    svm_report = classification_report(y_test, svm_predictions, output_dict=True)
    decision_tree_report = classification_report(y_test, decision_tree_predictions, output_dict=True)
    random_forest_report = classification_report(y_test, random_forest_predictions, output_dict=True)
    knn_report = classification_report(y_test, knn_predictions, output_dict=True)
    naive_bayes_report = classification_report(y_test, naive_bayes_predictions, output_dict=True)
    neural_network_report = classification_report(y_test, neural_network_predictions, output_dict=True)

    # Get the evaluation metrics for each algorithm
    svm_accuracy = svm_report['accuracy']
    svm_precision = svm_report['weighted avg']['precision']
    svm_recall = svm_report['weighted avg']['recall']
    svm_f1_score = svm_report['weighted avg']['f1-score']

    decision_tree_accuracy = decision_tree_report['accuracy']
    decision_tree_precision = decision_tree_report['weighted avg']['precision']
    decision_tree_recall = decision_tree_report['weighted avg']['recall']
    decision_tree_f1_score = decision_tree_report['weighted avg']['f1-score']

    random_forest_accuracy = random_forest_report['accuracy']
    random_forest_precision = random_forest_report['weighted avg']['precision']
    random_forest_recall = random_forest_report['weighted avg']['recall']
    random_forest_f1_score = random_forest_report['weighted avg']['f1-score']

    knn_accuracy = knn_report['accuracy']
    knn_precision = knn_report['weighted avg']['precision']
    knn_recall = knn_report['weighted avg']['recall']
    knn_f1_score = knn_report['weighted avg']['f1-score']

    naive_bayes_accuracy = naive_bayes_report['accuracy']
    naive_bayes_precision = naive_bayes_report['weighted avg']['precision']
    naive_bayes_recall = naive_bayes_report['weighted avg']['recall']
    naive_bayes_f1_score = naive_bayes_report['weighted avg']['f1-score']

    neural_network_accuracy = neural_network_report['accuracy']
    neural_network_precision = neural_network_report['weighted avg']['precision']
    neural_network_recall = neural_network_report['weighted avg']['recall']
    neural_network_f1_score = neural_network_report['weighted avg']['f1-score']

    # Determine the best algorithm based on accuracy
    best_accuracy = max(svm_accuracy, decision_tree_accuracy, random_forest_accuracy, knn_accuracy,
                        naive_bayes_accuracy, neural_network_accuracy)
    best_algorithm = ''
    if best_accuracy == svm_accuracy:
        best_algorithm = 'SVM'
    elif best_accuracy == decision_tree_accuracy:
        best_algorithm = 'Decision Tree'
    elif best_accuracy == random_forest_accuracy:
        best_algorithm = 'Random Forest'
    elif best_accuracy == knn_accuracy:
        best_algorithm = 'KNN'
    elif best_accuracy == naive_bayes_accuracy:
        best_algorithm = 'Naive Bayes'
    elif best_accuracy == neural_network_accuracy:
        best_algorithm = 'Neural Network'

    # Print the evaluation metrics and the best algorithm
    print("SVM Metrics:")
    print("Accuracy:", svm_accuracy)
    print("Precision:", svm_precision)
    print("Recall:", svm_recall)
    print("F1-score:", svm_f1_score)
    print()

    print("Decision Tree Metrics:")
    print("Accuracy:", decision_tree_accuracy)
    print("Precision:", decision_tree_precision)
    print("Recall:", decision_tree_recall)
    print("F1-score:", decision_tree_f1_score)
    print()

    print("Random Forest Metrics:")
    print("Accuracy:", random_forest_accuracy)
    print("Precision:", random_forest_precision)
    print("Recall:", random_forest_recall)
    print("F1-score:", random_forest_f1_score)
    print()

    print("KNN Metrics:")
    print("Accuracy:", knn_accuracy)
    print("Precision:", knn_precision)
    print("Recall:", knn_recall)
    print("F1-score:", knn_f1_score)
    print()

    print("Naive Bayes Metrics:")
    print("Accuracy:", naive_bayes_accuracy)
    print("Precision:", naive_bayes_precision)
    print("Recall:", naive_bayes_recall)
    print("F1-score:", naive_bayes_f1_score)
    print()

    print("Neural Network Metrics:")
    print("Accuracy:", neural_network_accuracy)
    print("Precision:", neural_network_precision)
    print("Recall:", neural_network_recall)
    print("F1-score:", neural_network_f1_score)
    print()

    print("Best Algorithm:", best_algorithm)

if __name__ == '__main__':
    main()

