from matplotlib.backends.qt_compat import QtWidgets, QtCore
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class LdaAnalyze( QtWidgets.QMainWindow ):

    def __init__(self , newDataFrame):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)

        self.data = newDataFrame

        # Create a Figure object and a canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Set the canvas as the central widget
        self.setCentralWidget(self.canvas)

        self.ldaAlgorithm()

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def ldaAlgorithm(self):

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

        colors = ['red', 'green', 'blue']  # Customize colors for different classes
        for color, label in zip(colors, np.unique(y_train)):
            ax.scatter(X_train_pca[y_train == label, 0], X_train_pca[y_train == label, 1], c=color, label=label)

        ax.set_xlabel('LDA Component 1')
        ax.set_ylabel('LDA Component 2')
        ax.legend()

        self.canvas.draw()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("LDA", "LDA Analyze"))
