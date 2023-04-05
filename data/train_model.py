import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler

FILENAME = "preprocessed_data.csv"

def main():
    data = pd.read_csv(FILENAME)

    # Split the DataFrame into features and target based on column names
    X = data.loc[:, data.columns != 'P_HABITABLE']
    X = X.drop(["P_NAME", "S_NAME"], axis=1)
    y = data['P_HABITABLE']

    # Resample the training set
    over_sampler = RandomOverSampler(sampling_strategy={1: sum(y == 0), 2: sum(y == 0)})
    under_sampler = RandomUnderSampler(sampling_strategy={0: sum(y == 0)})

    X_resampled, y_resampled = over_sampler.fit_resample(X, y)
    X_resampled, y_resampled = under_sampler.fit_resample(X_resampled, y_resampled)

    # Print the shapes of the resulting DataFrames
    print("Features shape:", X.shape)
    print("Target shape:", y.shape)

    # Show minimum and maximum values for all columns
    print("Minimum and maximum values for all columns:")
    for column_name in X_resampled.columns:
        if X_resampled[column_name].dtype in [int, float]:
            print(f"{column_name}: min = {X_resampled[column_name].min()}, max = {X_resampled[column_name].max()}")
    print()

    # Normalize the features using the z-score normalization
    scaler = StandardScaler()
    X_resampled = scaler.fit_transform(X_resampled)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

    # Print the shapes of the training and testing sets
    print("Training set shapes:")
    print("X_train_resampled:", X_train.shape)
    print("y_train_resampled:", y_train.shape)
    print("Testing set shapes:")
    print("X_test:", X_test.shape)
    print("y_test:", y_test.shape)

    # Create and train the XGBoost classifier
    xgb_clf = XGBClassifier(objective='multi:softmax', num_class=3, use_label_encoder=False, eval_metric='mlogloss')
    xgb_clf.fit(X_train, y_train)

    # Predict the class labels for the test set
    y_pred = xgb_clf.predict(X_test)

    # Save the model
    xgb_clf.save_model('xgboost_model.bin')

    # Print the classification report
    print(classification_report(y_test, y_pred))
    # Calculate and print the confusion matrix
    print("Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    cm = plot_confusion_mat(y_test, y_pred)


def plot_confusion_mat(ytest, ypred):
    # Create  a confusion matrix, which compares the y_test and prediction made
    conf_mat = confusion_matrix(ytest, ypred)

    # Create a dataframe for a array-formatted Confusion matrix,so it will be easy for plotting.
    # Assign corresponding names to labels
    confusion_mat_df = pd.DataFrame(conf_mat,
                                    index=['Inhabitable', 'Consevatively Habitable', 'Optimistically Habitable'],
                                    columns=['Inhabitable', 'Consevatively Habitable', 'Optimistically Habitable'])

    # Plot the confusion matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(confusion_mat_df, annot=True)
    plt.title('Habitability Confusion Matrix')
    plt.ylabel('Actual Values')
    plt.xlabel('Predicted Values')
    plt.show()

    return conf_mat

if __name__ == "__main__":
    main()
