from sklearn.linear_model import LogisticRegression


class Trainer:
    def train(self, X_train, y_train):
        model = LogisticRegression(random_state=42, max_iter=200)
        model.fit(X_train, y_train)
        return model