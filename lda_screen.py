from PyQt5.QtGui import QIcon
from matplotlib.backends.qt_compat import QtWidgets, QtCore
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import accuracy_score
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from joblib import dump, load
from sklearn.preprocessing import LabelEncoder

class LdaAnalyze( QtWidgets.QMainWindow ):

    def __init__(self , newDataFrame):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        icon = QIcon("icon.ico")
        self.setWindowIcon(icon)

        self.data = newDataFrame

        # Create a Figure object and a canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Set the canvas as the central widget
        self.setCentralWidget(self.canvas)

        self.ldaAlgorithmNumeral()

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def ldaAlgorithmNotNumeral(self):

        # Step 2: Prepare the data for prediction
        X = self.data[['S1', 'S2', 'S3', 'S4', 'S5', 'S6']].values

        # Step 3: Prepare the target variable
        le = LabelEncoder()
        y = le.fit_transform(self.data['Class'])

        # Step 4: Create and configure the LDA model
        lda = LinearDiscriminantAnalysis(solver='eigen', shrinkage='auto', priors='prior')
        pca = PCA(n_components=2)

        # Step 5: Fit the LDA model
        X_lda = lda.fit_transform(X, y)
        X_pca = pca.fit_transform(X_lda)

        # Step 6: Plot the LDA model
        target_names = le.classes_
        colors = ['navy', 'turquoise']
        plt.figure()
        for color, i, target_name in zip(colors, [0, 1], target_names):
            plt.scatter(X_pca[y == i, 0], X_pca[y == i, 1], color=color, alpha=0.8, lw=2, label=target_name)
        plt.legend()
        plt.title('LDA')
        plt.show()

        # Step 7: Print the accuracy
        accuracy = lda.score(X, y)
        print("Accuracy:", accuracy)
    def ldaAlgorithmNumeral(self):

        # data -> dataFram from excel file
        X = self.data.iloc[:, :-1].values
        y = self.data.iloc[:, -1].values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        pca = PCA(n_components=2)
        X_train_pca = pca.fit_transform(X_train_scaled)
        X_test_pca = pca.transform(X_test_scaled)

        lda = LinearDiscriminantAnalysis(solver='eigen', shrinkage='auto', priors=None, n_components=2)
        lda.fit(X_train_pca, y_train)

        y_pred = lda.predict(X_test_pca)
        accuracy = accuracy_score(y_test, y_pred)
        print("Accuracy:", accuracy)

        self.figure.clear()  # Clear the previous plot (if any)
        ax = self.figure.add_subplot(111)

        unique_classes = np.unique(y_train)
        colors = ['red', 'green', 'blue', 'purple']  # Customize colors for different classes

        for color, label in zip(colors, unique_classes):
            ax.scatter(X_train_pca[y_train == label, 0], X_train_pca[y_train == label, 1], c=color, label=label)

        ax.set_xlabel('LDA Component 1')
        ax.set_ylabel('LDA Component 2')
        ax.legend()

        self.canvas.draw()

    def ldaAlgorithm(self):
        pass
        # sensors = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']
        # header = [*sensors, 'Temperature', 'Humidity', 'Class']
        # df = pd.DataFrame(columns=header)
        #
        # # Generate qualitative two-class labels for data based on a threshold.
        # # If the value is above threshold, the sample is contaminated.
        # # sample_threshold = 0.01
        # # self.data['class_q'] = self.data['Class'].apply(lambda x: 'non' if float(x) < sample_threshold else 'sample')
        #
        # X = self.data.iloc[:, 1:7].values  # 6-row data
        # Y = self.data['class_q']  # qualitative classes
        #
        # # Tunable 80-20 percent data split for train-test
        # test_size = 0.2
        # X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, random_state=42)
        #
        # # Optional feature in training as the data gets normalized
        # scaler = StandardScaler()
        # X_train_scaled = scaler.fit_transform(X_train)
        # X_test_scaled = scaler.transform(X_test)
        #
        # pca = PCA(n_components=2)
        # X_train_scaled_pca = pca.fit_transform(X_train_scaled)
        # X_test_scaled_pca = pca.transform(X_test_scaled)
        # X_train_pca = pca.fit_transform(X_train)
        # X_test_pca = pca.transform(X_test)
        #
        # lda_scaled = LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto', priors=None, n_components=1)
        # lda = LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto', priors=None, n_components=1)
        # lda_scaled.fit(X_train_scaled_pca, Y_train)
        # lda.fit(X_train_pca, Y_train)
        #
        # # Test accuracy
        # y_pred = lda.predict(X_test_pca)
        # y_pred_scaled = lda_scaled.predict(X_test_scaled_pca)
        # accuracy = accuracy_score(Y_test, y_pred)
        # accuracy_scaled = accuracy_score(Y_test, y_pred_scaled)
        # print("Accuracy: ", accuracy)
        # print("Accuracy with: ", accuracy_scaled)

        # Tunable model with cross validation as metrics
        # solvers = ['svd', 'lsqr', 'eigen']
        # cv = 4

        # find best accuracy ->
        # for solver in solvers:
        #     lda = LinearDiscriminantAnalysis(solver=solver, n_components=1)
        #     lda_scaled = LinearDiscriminantAnalysis(solver=solver, n_components=1)
        #
        #     # Perform cross-validation and get the accuracy scores
        #     scores = cross_val_score(lda, X_train_pca, Y_train, cv=cv)
        #     scores_scaled = cross_val_score(lda_scaled, X_train_scaled_pca, Y_train, cv=cv)
        #
        #     # Calculate the mean accuracy score and print it
        #     accuracy = np.mean(scores)
        #     accuracy_scaled = np.mean(scores_scaled)
        #     print(f'Solver: {solver}, Cross Validation Accuracy: {accuracy}')
        #     print(f'Solver: {solver}, Cross Validation Accuracy (scaled): {accuracy_scaled}')
        # Solver: svd, Cross Validation Accuracy: 0.9642857142857143
        # Solver: svd, Cross Validation Accuracy (scaled): 0.8214285714285714
        # Solver: lsqr, Cross Validation Accuracy: 0.9642857142857143
        # Solver: lsqr, Cross Validation Accuracy (scaled): 0.8214285714285714
        # Solver: eigen, Cross Validation Accuracy: 0.9642857142857143
        # Solver: eigen, Cross Validation Accuracy (scaled): 0.8214285714285714

        # draw it on canvas ->
        # fig, ax = plt.subplots()
        # colors = ['red', 'blue']  # Customize colors for different classes
        # for color, label in zip(colors, np.unique(Y_train)):
        #     ax.scatter(X_train_pca[Y_train == label, 0], X_train_pca[Y_train == label, 1], c=color, label=label)
        # ax.set_xlabel('LDA Component 1')
        # ax.set_ylabel('LDA Component 2')
        # ax.legend()
        # self.canvas.draw()
        #
        # # Save the model using joblib and test the loaded model.
        # lda = LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto', priors=None, n_components=1)
        # lda.fit(X_train_pca, Y_train)
        # dump(lda, 'lda_model.joblib')
        #
        # # Load the model from the file
        # loaded_model = load('lda_model.joblib')
        #
        # # Make predictions on the testing data using the loaded model
        # y_pred = loaded_model.predict(X_test_pca)
        #
        # # Calculate and print the accuracy score
        # accuracy = accuracy_score(Y_test, y_pred)
        # print(f'Accuracy: {accuracy}')

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("LDA", "LDA Analyze"))
