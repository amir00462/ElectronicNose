from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from fonts import *
from PyQt5.QtGui import QIcon
from matplotlib.backends.qt_compat import QtWidgets, QtCore
from queue import Queue
from sklearn.model_selection import train_test_split, cross_val_score
import numpy as np
from joblib import dump, load
from matplotlib.figure import Figure
import plotter_screen

class LdaAnalyze(QtWidgets.QMainWindow):

    def __init__(self, newDataFrame):
        super().__init__()
        self.resize(1050, 822)
        self.centralwidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralwidget)
        self.logs_queue = Queue(maxsize=1000)

        icon = QIcon("icon.ico")
        self.setWindowIcon(icon)

        self.data = newDataFrame
        columns = self.data.columns.tolist()
        self.columns_formatted = str(columns)
        print(self.columns_formatted)

        # - - - - - - - - - -

        self.labelColumns = QtWidgets.QLabel(self.centralwidget)
        self.labelColumns.setGeometry(QtCore.QRect(40, 40, 900, 20))
        self.labelColumns.setFont(labelFont)

        # - - - - - - - - - -

        self.labelPrediction = QtWidgets.QLabel(self.centralwidget)
        self.labelPrediction.setGeometry(QtCore.QRect(40, 90, 300, 40))
        self.labelPrediction.setFont(labelFont)

        self.textEditPrediction = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditPrediction.setGeometry(QtCore.QRect(340, 90, 670, 35))
        self.textEditPrediction.setFont(textEditFontPrediction)

        # - - - - - - - - - -

        self.labelClassification = QtWidgets.QLabel(self.centralwidget)
        self.labelClassification.setGeometry(QtCore.QRect(40, 180, 300, 40))
        self.labelClassification.setFont(labelFont)

        self.textEditClassification = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditClassification.setGeometry(QtCore.QRect(340, 190, 670, 35))
        self.textEditClassification.setFont(textEditFontPrediction)

        # - - - - - - - - - -

        self.logLda = QtWidgets.QTextBrowser(self.centralwidget)
        self.logLda.setGeometry(QtCore.QRect(40, 260, 970, 465))
        self.logLda.setFont(logFont)

        # - - - - - - - - - -

        self.solverNameEditText = QtWidgets.QTextEdit(self.centralwidget)
        self.solverNameEditText.setGeometry(QtCore.QRect(523, 730, 484, 40))
        self.solverNameEditText.setFont(textEditFontPrediction)
        self.solverNameEditText.setText("Enter Solver")
        self.solverNameEditText.setAlignment(QtCore.Qt.AlignCenter)

        self.showSolversButton = QtWidgets.QPushButton(self.centralwidget)
        self.showSolversButton.setGeometry(QtCore.QRect(40, 730, 480, 40))
        self.showSolversButton.setFont(buttonFont)
        self.showSolversButton.setAutoDefault(False)
        self.showSolversButton.clicked.connect(self.solverFinder)

        self.ldaButton = QtWidgets.QPushButton(self.centralwidget)
        self.ldaButton.setGeometry(QtCore.QRect(40, 772, 970, 40))
        self.ldaButton.setFont(buttonFont)
        self.ldaButton.setAutoDefault(False)
        self.ldaButton.clicked.connect(self.ldaAlgorithm)

        # - - - - - - - - - -

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def plotResult(self):
        fig = Figure()
        ax = fig.add_subplot(111)
        colors = ['red', 'blue']  # Customize colors for different classes
        for color, label in zip(colors, np.unique(self.Y_train)):
            ax.scatter(self.X_train_pca[self.Y_train == label, 0], self.X_train_pca[self.Y_train == label, 1], c=color,
                       label=label)
        ax.set_xlabel('LDA Component 1')
        ax.set_ylabel('LDA Component 2')
        ax.legend()

        self.plotScreen = plotter_screen.PlotterScreen(fig)
        self.plotScreen.show()

    def solverFinder(self):

        # self.add_log(self.logs_queue, Y)
        X = self.data[str(self.textEditPrediction.toPlainText()).split(',')].values
        Y = self.data[str(self.textEditClassification.toPlainText())]

        # Tunable 80-20 percent data split for train-test
        test_size = 0.2
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(X, Y, test_size=test_size,
                                                                                random_state=42)
        self.add_log(self.logs_queue, "\nWe are using 80-20 percent data split for train-test...")

        self.add_log(self.logs_queue, "\nUsing Pca with \'n_components = 2\'")
        pca = PCA(n_components=2)
        self.X_train_pca = pca.fit_transform(self.X_train)
        self.X_test_pca = pca.transform(self.X_test)

        # Tunable model with cross validation as metrics
        self.add_log(self.logs_queue, "\nFind Solver:")
        self.add_log(self.logs_queue, "Solvers = ['svd', 'lsqr', 'eigen']\n")
        solvers = ['svd', 'lsqr', 'eigen']
        cv = 4

        for solver in solvers:
            lda = LinearDiscriminantAnalysis(solver=solver, n_components=1)

            scores = cross_val_score(lda, self.X_train_pca, self.Y_train, cv=cv)
            accuracy = np.mean(scores)

            self.add_log(self.logs_queue, f'Solver: {solver}, Cross Validation Accuracy: {accuracy}')

        self.add_log(self.logs_queue, "\nSolvers Printed, Choose one of them and then tap analyze...\n")
    def ldaAlgorithm(self):
        solver = str(self.solverNameEditText.toPlainText())

        # Save the model using joblib and test the loaded model.
        self.add_log(self.logs_queue, "Using Lda with your config...")
        # feature_names = str(self.textEditPrediction.toPlainText()).split(',')
        # self.X_train_pca.columns = feature_names
        if solver == 'svd':
            lda = LinearDiscriminantAnalysis(solver=solver, shrinkage=None, priors=None, n_components=1)
        else:
            lda = LinearDiscriminantAnalysis(solver=solver, shrinkage='auto', priors=None, n_components=1)

        lda.fit(self.X_train_pca, self.Y_train)
        dump(lda, 'lda_model.joblib')

        # Load the model from the file
        self.add_log(self.logs_queue, "model trained and saved in lda_model.joblib\n")
        loaded_model = load('lda_model.joblib')

        # Make predictions on the testing data using the loaded model
        y_pred = loaded_model.predict(self.X_test_pca)

        # Calculate and print the accuracy score
        accuracy = accuracy_score(self.Y_test, y_pred)
        self.add_log(self.logs_queue, f'Accuracy: {accuracy}')
        self.add_log(self.logs_queue, "We used \'shrinkage=auto\' to make Accuracy better")

        self.plotResult()

    def enqueue(self, queue, clause):
        if queue.full():
            queue.get()

        queue.put(clause)
    def add_log(self, queue, clause):
        self.enqueue(queue, clause)
        self.logLda.setText('\n'.join(list(self.logs_queue.queue)))
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Lda", "Lda Analyze"))
        self.labelColumns.setText(_translate("Lda", "DataSet Columns : " + self.columns_formatted))
        self.labelPrediction.setText(_translate("Lda", "Prediction Columns:\nexample: S1,S2,S3,S4,S5,S6"))
        self.labelClassification.setText(_translate("Lda", "Classification Column:\nexample: class_q"))
        self.ldaButton.setText(_translate("Lda", "Lda Analyze"))
        self.showSolversButton.setText(_translate("Lda", "Find Best Solver"))
        self.add_log(self.logs_queue,
                     "1. Choose prediction and classification columns\n2. tap find best solver button\n3. write best solver name in below input\n4. tap analyze button\n 5. analyze will be plotted and trained data will save at same folder \'lda.joblib\'")
        self.textEditPrediction.setText(_translate("Lda", "S1,S2,S3,S4,S5,S6"))
        self.textEditClassification.setText(_translate("Lda", "class_q"))
