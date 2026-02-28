import pandas as pd
import pickle
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import os
import numpy as np

def train_model():
    # Try to load the spam.csv dataset first
    spam_csv_path = '../../spam.csv'
    data_path = '../data/phishing_dataset.csv'
    
    if os.path.exists(spam_csv_path):
        print("Loading spam.csv dataset...")
        # Load spam.csv with proper column names
        df = pd.read_csv(spam_csv_path, encoding='latin-1')
        # Use only first two columns and rename them
        df = df.iloc[:, :2]
        df.columns = ['label', 'text']
        # Convert ham/spam to 0/1 (ham=0, spam=1)
        df['label'] = df['label'].map({'ham': 0, 'spam': 1})
        # Remove any NaN values
        df = df.dropna()
        print(f"✓ Loaded spam.csv dataset")
    elif os.path.exists(data_path):
        print("Loading phishing_dataset.csv...")
        df = pd.read_csv(data_path)
        print(f"✓ Loaded phishing_dataset.csv")
    else:
        print("No dataset found. Creating sample dataset...")
        create_sample_dataset()
        df = pd.read_csv(data_path)
    
    print(f"\nDataset Statistics:")
    print(f"Total samples: {len(df)}")
    print(f"Spam/Phishing emails: {sum(df['label'] == 1)} ({sum(df['label'] == 1)/len(df)*100:.1f}%)")
    print(f"Ham/Safe emails: {sum(df['label'] == 0)} ({sum(df['label'] == 0)/len(df)*100:.1f}%)")
    
    # Prepare data
    X = df['text']
    y = df['label']
    
    # Split data with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTraining set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    
    # Enhanced TF-IDF Vectorization
    vectorizer = TfidfVectorizer(
        max_features=10000,  # Increased features
        stop_words='english',
        ngram_range=(1, 3),  # Unigrams, bigrams, and trigrams
        min_df=2,  # Minimum document frequency
        max_df=0.95,  # Maximum document frequency
        sublinear_tf=True,  # Use sublinear term frequency scaling
        strip_accents='unicode',
        lowercase=True
    )
    
    print("\nVectorizing text...")
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    print(f"Feature matrix shape: {X_train_vec.shape}")
    print(f"Vocabulary size: {len(vectorizer.vocabulary_)}")
    
    # Train multiple models for ensemble
    print("\n" + "="*60)
    print("Training Models...")
    print("="*60)
    
    # Logistic Regression with optimized parameters
    print("\n1. Training Logistic Regression...")
    lr_model = LogisticRegression(
        max_iter=2000,
        random_state=42,
        class_weight='balanced',
        C=1.0,  # Regularization strength
        solver='liblinear'
    )
    lr_model.fit(X_train_vec, y_train)
    print("   ✓ Logistic Regression trained")
    
    # Multinomial Naive Bayes
    print("\n2. Training Naive Bayes...")
    nb_model = MultinomialNB(alpha=0.1)
    nb_model.fit(X_train_vec, y_train)
    print("   ✓ Naive Bayes trained")
    
    # Random Forest
    print("\n3. Training Random Forest...")
    rf_model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight='balanced',
        max_depth=20,
        min_samples_split=5,
        n_jobs=-1  # Use all CPU cores
    )
    rf_model.fit(X_train_vec, y_train)
    print("   ✓ Random Forest trained")
    
    # Create ensemble voting classifier
    print("\n4. Creating Ensemble Model...")
    ensemble_model = VotingClassifier(
        estimators=[
            ('lr', lr_model),
            ('nb', nb_model),
            ('rf', rf_model)
        ],
        voting='soft',  # Use probability voting
        weights=[2, 1, 2]  # Give more weight to LR and RF
    )
    ensemble_model.fit(X_train_vec, y_train)
    print("   ✓ Ensemble model created")
    
    
    # Evaluate all models
    print("\n" + "="*60)
    print("Model Evaluation")
    print("="*60)
    
    # Logistic Regression evaluation
    print("\n📊 LOGISTIC REGRESSION")
    print("-" * 60)
    y_pred_lr = lr_model.predict(X_test_vec)
    y_proba_lr = lr_model.predict_proba(X_test_vec)
    accuracy_lr = accuracy_score(y_test, y_pred_lr)
    
    print(f"Accuracy: {accuracy_lr * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred_lr, target_names=['Safe/Ham', 'Spam/Phishing']))
    cm_lr = confusion_matrix(y_test, y_pred_lr)
    print("\nConfusion Matrix:")
    print(cm_lr)
    print(f"True Negatives: {cm_lr[0][0]}, False Positives: {cm_lr[0][1]}")
    print(f"False Negatives: {cm_lr[1][0]}, True Positives: {cm_lr[1][1]}")
    
    # Naive Bayes evaluation
    print("\n📊 NAIVE BAYES")
    print("-" * 60)
    y_pred_nb = nb_model.predict(X_test_vec)
    accuracy_nb = accuracy_score(y_test, y_pred_nb)
    print(f"Accuracy: {accuracy_nb * 100:.2f}%")
    
    # Random Forest evaluation
    print("\n📊 RANDOM FOREST")
    print("-" * 60)
    y_pred_rf = rf_model.predict(X_test_vec)
    accuracy_rf = accuracy_score(y_test, y_pred_rf)
    print(f"Accuracy: {accuracy_rf * 100:.2f}%")
    
    # Ensemble evaluation
    print("\n📊 ENSEMBLE MODEL")
    print("-" * 60)
    y_pred_ensemble = ensemble_model.predict(X_test_vec)
    accuracy_ensemble = accuracy_score(y_test, y_pred_ensemble)
    print(f"Accuracy: {accuracy_ensemble * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred_ensemble, target_names=['Safe/Ham', 'Spam/Phishing']))
    
    # Cross-validation score for best model
    print("\n📊 CROSS-VALIDATION (5-fold)")
    print("-" * 60)
    cv_scores = cross_val_score(lr_model, X_train_vec, y_train, cv=5, scoring='accuracy')
    print(f"CV Scores: {[f'{score:.4f}' for score in cv_scores]}")
    print(f"Mean CV Accuracy: {cv_scores.mean() * 100:.2f}% (+/- {cv_scores.std() * 2 * 100:.2f}%)")
    
    # Test probability predictions
    print("\n📊 SAMPLE PREDICTIONS")
    print("-" * 60)
    sample_indices = np.random.choice(len(X_test), min(5, len(X_test)), replace=False)
    for idx in sample_indices:
        text = X_test.iloc[idx]
        proba = y_proba_lr[idx]
        pred = y_pred_lr[idx]
        actual = y_test.iloc[idx]
        correct = "✓" if pred == actual else "✗"
        print(f"\n{correct} Text: {text[:80]}...")
        print(f"   Actual: {'SPAM' if actual == 1 else 'SAFE'} | Predicted: {'SPAM' if pred == 1 else 'SAFE'}")
        print(f"   Spam Probability: {proba[1] * 100:.2f}% | Confidence: {max(proba) * 100:.2f}%")
    
    # Save the best model (choose based on performance)
    accuracies = {
        'Logistic Regression': accuracy_lr,
        'Naive Bayes': accuracy_nb,
        'Random Forest': accuracy_rf,
        'Ensemble': accuracy_ensemble
    }
    
    best_model_name = max(accuracies, key=accuracies.get)
    best_accuracy = accuracies[best_model_name]
    
    # Select the best model
    model_map = {
        'Logistic Regression': lr_model,
        'Naive Bayes': nb_model,
        'Random Forest': rf_model,
        'Ensemble': ensemble_model
    }
    best_model = model_map[best_model_name]
    
    print("\n" + "="*60)
    print("SAVING BEST MODEL")
    print("="*60)
    print(f"\n🏆 Best Model: {best_model_name}")
    print(f"🎯 Accuracy: {best_accuracy * 100:.2f}%")
    print(f"\nAll Model Accuracies:")
    for name, acc in sorted(accuracies.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {name}: {acc * 100:.2f}%")
    
    with open('phishing_model.pkl', 'wb') as f:
        pickle.dump(best_model, f)
    
    with open('vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    
    print("\n✅ Model and vectorizer saved successfully!")
    print(f"✅ Training complete with {best_accuracy * 100:.2f}% accuracy")
    print("="*60)

def create_sample_dataset():
    # Sample phishing and legitimate messages
    data = {
        'text': [
            'Your account has been suspended. Click here to verify immediately.',
            'Urgent: Your payment is overdue. Update your credit card now.',
            'Congratulations! You won $1000. Claim your prize here.',
            'Your package delivery failed. Confirm your address to reschedule.',
            'Meeting scheduled for tomorrow at 3pm. Please confirm attendance.',
            'Your monthly report is ready for review.',
            'Thank you for your purchase. Your order will arrive in 3-5 days.',
            'Reminder: Team meeting on Friday at 10am.',
            'Your subscription renewal is coming up next month.',
            'Project deadline extended to next week.',
            'ALERT: Suspicious activity detected. Reset password immediately!',
            'You have inherited $5 million. Contact us to claim.',
            'Your tax refund is ready. Click to download.',
            'Security breach detected. Verify your identity now.',
            'Free gift card waiting for you. Click to redeem.',
            'Your email will be closed. Reactivate now.',
            'Invoice attached for your recent purchase.',
            'Welcome to our newsletter. Unsubscribe anytime.',
            'Your appointment is confirmed for next Tuesday.',
            'System maintenance scheduled for this weekend.',
        ],
        'label': [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
    }
    
    df = pd.DataFrame(data)
    os.makedirs('../data', exist_ok=True)
    df.to_csv('../data/phishing_dataset.csv', index=False)
    print("Sample dataset created!")

if __name__ == '__main__':
    train_model()
