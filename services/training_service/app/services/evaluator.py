from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


class Evaluator:
    def evaluate(self, model, X_test, y_test) -> dict:
        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        class_report = classification_report(y_test, y_pred, output_dict=True)
        conf_matrix = confusion_matrix(y_test, y_pred).tolist()

        return {
            "accuracy": accuracy,
            "classification_report": class_report,
            "confusion_matrix": conf_matrix
        }