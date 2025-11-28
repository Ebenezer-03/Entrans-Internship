import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import pandas as pd
import numpy as np

class NLUClassifier:
    def __init__(self, model_name='distilbert-base-uncased', num_labels=5):
        self.tokenizer = DistilBertTokenizer.from_pretrained(model_name)
        self.model = DistilBertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def compute_metrics(self, pred):
        labels = pred.label_ids
        preds = pred.predictions.argmax(-1)
        precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='weighted', zero_division=0)
        acc = accuracy_score(labels, preds)
        return {
            'accuracy': acc,
            'f1': f1,
            'precision': precision,
            'recall': recall
        }

    def train_and_evaluate(self, df, text_col='clean_text', label_col='label'):
        # Map labels to integers
        unique_labels = df[label_col].unique()
        label_map = {label: i for i, label in enumerate(unique_labels)}
        df['label_id'] = df[label_col].map(label_map)
        
        # Update model num_labels if different
        if len(unique_labels) != self.model.config.num_labels:
            self.model.num_labels = len(unique_labels)
            # Re-init classification head (simplified for this snippet)
            pass

        train_texts, val_texts, train_labels, val_labels = train_test_split(
            df[text_col].tolist(), df['label_id'].tolist(), test_size=0.2, random_state=42
        )

        train_encodings = self.tokenizer(train_texts, truncation=True, padding=True, max_length=128)
        val_encodings = self.tokenizer(val_texts, truncation=True, padding=True, max_length=128)

        class NewsDataset(torch.utils.data.Dataset):
            def __init__(self, encodings, labels):
                self.encodings = encodings
                self.labels = labels

            def __getitem__(self, idx):
                item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
                item['labels'] = torch.tensor(self.labels[idx])
                return item

            def __len__(self):
                return len(self.labels)

        train_dataset = NewsDataset(train_encodings, train_labels)
        val_dataset = NewsDataset(val_encodings, val_labels)

        training_args = TrainingArguments(
            output_dir='./results',
            num_train_epochs=1, # Low for demo speed
            per_device_train_batch_size=8,
            per_device_eval_batch_size=16,
            warmup_steps=10,
            weight_decay=0.01,
            logging_dir='./logs',
            logging_steps=10,
            evaluation_strategy="epoch",
            save_strategy="no", # Save space
            use_cpu=not torch.cuda.is_available()
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            compute_metrics=self.compute_metrics
        )

        print("Training DistilBERT...")
        trainer.train()
        
        print("Evaluating DistilBERT...")
        eval_result = trainer.evaluate()
        
        # Format results to match traditional output
        return {
            "DistilBERT": {
                "accuracy": eval_result['eval_accuracy'],
                "precision": eval_result['eval_precision'],
                "recall": eval_result['eval_recall'],
                "f1": eval_result['eval_f1']
            }
        }
