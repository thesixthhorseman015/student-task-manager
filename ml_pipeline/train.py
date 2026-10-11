import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score

def train():
    mlflow.set_experiment("Task_Priority_Prediction")

    with mlflow.start_run(run_name="LogisticRegression_v1"):
        # 1. Hyperparameters
        c_param = 1.0
        max_iter = 200
        random_state = 42

        # Log parameters
        mlflow.log_param("C", c_param)
        mlflow.log_param("max_iter", max_iter)
        mlflow.log_param("model_type", "LogisticRegression")

        # 2. Dataset
        data = load_iris()
        X_train, X_test, y_train, y_test = train_test_split(
            data.data, data.target, test_size=0.2, random_state=random_state
        )

        # 3. Model Training
        clf = LogisticRegression(C=c_param, max_iter=max_iter, random_state=random_state)
        clf.fit(X_train, y_train)

        # 4. Evaluation
        preds = clf.predict(X_test)
        acc = accuracy_score(y_test, preds)
        prec = precision_score(y_test, preds, average="macro")

        # Log metrics
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("precision", prec)

        # 5. Log Model Artifact using standard serialization
        mlflow.sklearn.log_model(
            sk_model=clf,
            name="task_classifier_model",
            serialization_format="cloudpickle"
        )

        print(f"Success! Accuracy: {acc:.4f}, Precision: {prec:.4f}")

if __name__ == "__main__":
    train()