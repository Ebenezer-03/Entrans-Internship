# 🚀 Quick Start Guide - NLP/NLU 3-Day Project

## Step-by-Step Instructions for Beginners

Follow these steps **one by one** to get started with the NLP/NLU project.

---

## ✅ Prerequisites Check

Before starting, make sure you have:
- [ ] Python 3.10 or higher installed
- [ ] At least 4GB RAM available
- [ ] ~2GB free disk space
- [ ] Internet connection (for downloading models)

**Check Python version:**
```bash
python --version
```
Should show: Python 3.10.x or higher

---

## 📝 Step-by-Step Setup (Already Completed ✅)

### Step 1: Navigate to Project Directory ✅
```bash
cd "c:\Artificial Intelligence and Data Science\Task - 04"
```

### Step 2: Install Dependencies ✅
```bash
pip install -r requirements.txt
```
**Status:** ✅ DONE (20+ packages installed)

### Step 3: Download spaCy Model ✅
```bash
python -m spacy download en_core_web_sm
```
**Status:** ✅ DONE (en_core_web_sm v3.8.0 installed)

### Step 4: Download Sample Data ✅
```bash
python data/download_data.py
```
**Status:** ✅ DONE (5 datasets downloaded)

### Step 5: Run Smoke Test ✅
```bash
python tests/test_smoke_model.py
```
**Status:** ✅ PASSED (100% accuracy)

---

## 🎓 Learning Path - Start Here!

### **Day 1: Learn NLP Basics (Start with these)**

#### Demo 1: Tokenization (5 minutes)
**What you'll learn:** How to break text into words, remove stopwords, lemmatize

```bash
python nlp_day1/day1_tokenization_spacy.py
```

**What to observe:**
- How sentences are split into words (tokens)
- Difference between "running" → "run" (lemmatization)
- Which words are stopwords ("the", "is", "a")

#### Demo 2: Named Entity Recognition (5 minutes)
**What you'll learn:** How to extract names, places, organizations from text

```bash
python nlp_day1/day1_ner_rulebased.py
```

**What to observe:**
- Entities like "Apple Inc." (ORG), "New York" (GPE)
- Pattern matching for emails, phone numbers
- Output file: `examples/outputs/ner_visualization.html` (open in browser!)

---

### **Day 2: Feature Engineering & Classification**

#### Demo 3: Bag of Words & TF-IDF (10 minutes)
**What you'll learn:** How to convert text into numbers for ML

```bash
python nlp_day2/bow_tfidf.py
```

**What to observe:**
- How text becomes a matrix of numbers
- Which words are most important (TF-IDF scores)
- Visualization: `examples/outputs/tfidf_features.png`

#### Demo 4: Sentiment Analysis (15 minutes)
**What you'll learn:** How to classify movie reviews as positive/negative

```bash
python nlp_day2/sentiment_spacy_project.py
```

**What to observe:**
- Model accuracy: ~85% (pretty good!)
- Confusion matrix showing predictions
- Comparison of different approaches

#### Demo 5: Topic Classification (15 minutes)
**What you'll learn:** How to classify news into categories

```bash
python nlp_day2/topic_classification.py
```

**What to observe:**
- 4 categories: World, Sports, Business, Sci/Tech
- Which words are important for each topic
- Model accuracy: ~88%

---

### **Day 3: Modern Transformers & Deep Learning**

#### Demo 6: BERT Embeddings (15 minutes)
**What you'll learn:** How modern AI understands word meanings

```bash
python nlu_day3/embeddings_experiments.py
```

**What to observe:**
- Semantic similarity (finding similar sentences)
- t-SNE visualization of word meanings
- How BERT is better than BOW/TF-IDF

#### Demo 7: Text Summarization (10 minutes)
**What you'll learn:** How AI summarizes long articles

```bash
python nlu_day3/summarization_demo.py
```

**What to observe:**
- Long article → short summary
- ROUGE scores (how good is the summary?)
- Different summary lengths

#### Demo 8: Evaluation Metrics (5 minutes)
**What you'll learn:** How to measure NLP model quality

```bash
python nlu_day3/evaluation_metrics.py
```

**What to observe:**
- ROUGE scores for summarization
- BLEU scores for translation
- When to use which metric

---

## 🎯 Recommended Learning Order

### **Beginner Path (Start Here):**
1. ✅ Day 1 Demo 1: Tokenization (understand basics)
2. ✅ Day 1 Demo 2: NER (see practical application)
3. Day 2 Demo 3: BOW/TF-IDF (learn feature engineering)
4. Day 2 Demo 4: Sentiment (build your first classifier)

### **Intermediate Path:**
5. Day 2 Demo 5: Topic Classification (multi-class problems)
6. Day 3 Demo 6: BERT Embeddings (modern NLP)
7. Day 3 Demo 7: Summarization (transformers in action)

### **Advanced Path:**
8. Day 3 Demo 8: Evaluation Metrics (measure quality)
9. Fine-tune transformers: `python nlu_day3/hf_classification.py --task sentiment --epochs 1 --subset 200`

---

## 📊 What Each Demo Does

| Demo | Input | Output | Time |
|------|-------|--------|------|
| Tokenization | "The cat sat" | ["The", "cat", "sat"] | 5s |
| NER | "Apple Inc. in NYC" | ORG: Apple Inc., GPE: NYC | 5s |
| BOW/TF-IDF | ["I love NLP", "NLP is great"] | Matrix of numbers | 1m |
| Sentiment | "Great movie!" | Positive (85% confident) | 2m |
| Topics | "Stock market rises" | Business (88% confident) | 2m |
| BERT | "cat" vs "dog" | Similarity: 0.65 | 1m |
| Summarization | Long article | Short summary | 30s |

---

## 🔍 Where to Find Outputs

All generated files are in `examples/outputs/`:

```
examples/outputs/
├── tfidf_features.png          ← TF-IDF visualization
├── confusion_matrix_sentiment.png  ← Sentiment results
├── confusion_matrix_topics.png     ← Topic results
├── embeddings_tsne.png         ← BERT visualization
├── ner_visualization.html      ← NER results (open in browser!)
└── generated_summary.txt       ← Summarization output
```

---

## 💡 Tips for Learning

### 1. **Start Simple**
Begin with Day 1 demos to understand basics before moving to complex transformers.

### 2. **Read the Output**
Each demo prints explanations. Read them carefully to understand what's happening.

### 3. **Modify and Experiment**
Try changing the input text in the scripts to see different results.

### 4. **Check Visualizations**
Open the PNG and HTML files to see visual results.

### 5. **Use Jupyter Notebooks** (Optional)
```bash
jupyter lab
# Open: nlp_day1/notebook_day1.ipynb
```

---

## 🆘 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'spacy'"
**Solution:** Run `pip install -r requirements.txt`

### Problem: "Can't find model 'en_core_web_sm'"
**Solution:** Run `python -m spacy download en_core_web_sm`

### Problem: Demo is slow
**Solution:** Normal on CPU. Use smaller `--subset` parameter for faster demos.

### Problem: Out of memory
**Solution:** Close other applications or use smaller datasets.

---

## 📚 Next Steps After Demos

### 1. **Try Your Own Data**
Modify the scripts to use your own text files.

### 2. **Experiment with Parameters**
Change hyperparameters in `utils/config.yaml`.

### 3. **Build a Project**
Use these techniques to build your own NLP application.

### 4. **Learn More**
- [spaCy Documentation](https://spacy.io/usage)
- [HuggingFace Tutorials](https://huggingface.co/docs/transformers)

---

## ⏱️ Time Commitment

- **Quick Tour (30 min):** Run Day 1 demos
- **Half Day (3 hours):** Complete all Day 1-2 demos
- **Full Course (6 hours):** All demos + experimentation
- **Deep Dive (2-3 days):** Modify code, try custom datasets

---

## 🎓 What You'll Learn

By the end, you'll understand:
- ✅ How to preprocess text for ML
- ✅ How to extract features from text
- ✅ How to build text classifiers
- ✅ How modern transformers work
- ✅ How to evaluate NLP models
- ✅ How to use BERT, GPT-style models

---

## 🚀 Ready to Start?

**Your first command:**
```bash
python nlp_day1/day1_tokenization_spacy.py
```

**Watch the output and learn!** 🎉

---

## 📞 Need Help?

- Check `README.md` for detailed documentation
- Review `generation_report.txt` for technical details
- Open `examples/outputs/*.html` files in browser for visualizations

**Happy Learning!** 🚀📚
