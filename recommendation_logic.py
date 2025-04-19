# import pandas as pd
# from sklearn.preprocessing import LabelEncoder
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.model_selection import StratifiedShuffleSplit
# from sklearn.preprocessing import LabelEncoder, StandardScaler
# import joblib

# # Load the dataset
# dataframe = pd.read_csv(r"F:/College Recommendation System/College Recommendation System/Be_project1/mht_cet2.csv")

# # Data Preprocessing
# dataframe.replace(to_replace='^', value='Admitted to Institute', inplace=True)
# dataframe.replace(to_replace='~', value='No Change', inplace=True)
# dataframe.replace(to_replace='*', value='Betterment in Choice Code', inplace=True)
# dataframe.replace(to_replace='@', value='Betterment in Seat Type', inplace=True)
# dataframe.replace(to_replace='&', value='Newly Allotted', inplace=True)
# dataframe.replace(to_replace='GOPENS', value='General Open State Level', inplace=True)
# dataframe.replace(to_replace='LOPENS', value='Ladies Open State Level', inplace=True)

# # Encode categorical variables
# label_encoder_category = LabelEncoder()
# label_encoder_gender = LabelEncoder()
# label_encoder_branch = LabelEncoder()
# # Encode college_name (Target column)
# label_encoder_college = LabelEncoder()
# dataframe['college_encoded'] = label_encoder_college.fit_transform(dataframe['college_name'])

# dataframe['category_encoded'] = label_encoder_category.fit_transform(dataframe['category'])
# dataframe['gender_encoded'] = label_encoder_gender.fit_transform(dataframe['gender'])
# dataframe['branch_encoded'] = label_encoder_branch.fit_transform(dataframe['branch'])

# # Train the KNN model
# # features = ['rank', 'percentile', 'category', 'gender']
# # x = dataframe[features]
# # y = dataframe['college_name']
# # knn = KNeighborsClassifier(n_neighbors=10)
# # knn.fit(x, y)
# features = ['rank', 'percentile', 'category_encoded', 'gender_encoded', 'branch_encoded']
# X = dataframe[features]
# y = dataframe['college_encoded']  # Target

# # Stratified split
# split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
# for train_index, test_index in split.split(X, y):
#     X_train, X_test = X.iloc[train_index], X.iloc[test_index]
#     y_train, y_test = y.iloc[train_index], y.iloc[test_index]

# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)
# knn = KNeighborsClassifier(n_neighbors=30)
# knn.fit(X_train_scaled, y_train)




# # Save the model and encoders
# joblib.dump(knn, 'knn_model.pkl')
# joblib.dump(scaler, 'scaler.pkl')  # Don't forget the scaler!
# joblib.dump(label_encoder_category, 'label_encoder_category.pkl')
# joblib.dump(label_encoder_gender, 'label_encoder_gender.pkl')
# joblib.dump(label_encoder_branch, 'label_encoder_branch.pkl')
# joblib.dump(label_encoder_college, 'label_encoder_college.pkl')

# print("Model and encoders saved successfully!")

import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score
import joblib

# Load the dataset
dataframe = pd.read_csv(r"F:/College Recommendation System/College Recommendation System/Be_project1/mht_cet2.csv")

# Clean symbolic data
dataframe.replace(to_replace='^', value='Admitted to Institute', inplace=True)
dataframe.replace(to_replace='~', value='No Change', inplace=True)
dataframe.replace(to_replace='*', value='Betterment in Choice Code', inplace=True)
dataframe.replace(to_replace='@', value='Betterment in Seat Type', inplace=True)
dataframe.replace(to_replace='&', value='Newly Allotted', inplace=True)
dataframe.replace(to_replace='GOPENS', value='General Open State Level', inplace=True)
dataframe.replace(to_replace='LOPENS', value='Ladies Open State Level', inplace=True)

# Label encode categorical columns
label_encoder_category = LabelEncoder()
label_encoder_gender = LabelEncoder()
label_encoder_branch = LabelEncoder()
label_encoder_college = LabelEncoder()

dataframe['category_encoded'] = label_encoder_category.fit_transform(dataframe['category'])
dataframe['gender_encoded'] = label_encoder_gender.fit_transform(dataframe['gender'])
dataframe['branch_encoded'] = label_encoder_branch.fit_transform(dataframe['branch'])
dataframe['college_encoded'] = label_encoder_college.fit_transform(dataframe['college_name'])  # target encoding

# Select features and target
features = ['rank', 'percentile', 'category_encoded', 'gender_encoded', 'branch_encoded']
X = dataframe[features]
y = dataframe['college_encoded']

# Train/test split
split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in split.split(X, y):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model
knn = KNeighborsClassifier(n_neighbors=30)
knn.fit(X_train_scaled, y_train)

# Save the model and encoders
joblib.dump(knn, 'knn_model.pkl')
joblib.dump(scaler, 'scaler.pkl')  # Don't forget the scaler!
joblib.dump(label_encoder_category, 'label_encoder_category.pkl')
joblib.dump(label_encoder_gender, 'label_encoder_gender.pkl')
joblib.dump(label_encoder_branch, 'label_encoder_branch.pkl')
joblib.dump(label_encoder_college, 'label_encoder_college.pkl')

print("Model and encoders saved successfully!")
y_pred = knn.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")