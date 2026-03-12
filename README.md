
---------------------------------------
🧠 GTA (Graph Topology Ablation) Challenge
---------------------------------------

This repository hosts the official evaluation system for the Graph Topology Ablation (GTA) challenge.
Participants submit predictions for ideal and perturbed topology settings.

All submissions are encrypted, automatically evaluated, and ranked on a public leaderboard.

Repository hosted on GitHub.

-------------------------------------------------------------------------------------------------------------
🏆 View Live Leaderboard: [Open leaderboard](https://idrees11.github.io/GTA-Graph-Topology-Ablation_-GTA-/)
--------------------------------------------------------------------------------------------------------------
---------------
🎯 Objective
---------------

Participants must generate predictions for two settings: 
```
✅ Ideal graph topology
✅ Perturbed graph topology
```
------------------------------
**⚙️ Perturbation Mechanism**
------------------------------
Two types of feature corruption are applied:
```
1️ Distribution Shift
    A constant offset is added to node features:
    x ← x + δ
    where δ = feature_shift (default 0.3)

    This simulates systematic measurement bias or domain shift.

2️ Gaussian Noise Injection
    Random noise is added to each feature:
    x ← x + ϵ,   ϵ ~ N(0, σ²)
    where σ = noise_std (default 0.05)

    This simulates noisy feature extraction.
```
--------------------------------
**Purpose of This Perturbation**
--------------------------------
```
This setup evaluates whether a GNN:

✔ relies on exact feature values
✔ generalizes under feature distribution shift
✔ remains stable under noisy topological descriptors

The model is trained on clean features and evaluated under corrupted features to measure robustness.
```

----------------------
📌Dataset Description
----------------------
```
We have used MUTAG Dataset: 

MUTAG is a classic benchmark dataset for graph classification originating from chemical informatics research.
It consists of molecular graphs representing small chemical compounds, with labels indicating whether each compound
exhibits mutagenic effects on a specific bacterium.

```

**🔗 Official Source**

The dataset is part of the TU Dortmund University graph kernel benchmark collection and can be downloaded from the official TU Dortmund repository:

📥 https://ls11-www.cs.tu-dortmund.de/people/morris/graphkerneldatasets/MUTAG.zip

**📊 Core Statistics**
```
Property                Value

Task                    Binary graph classification

Domain	                Chemical compounds (mutagenic vs non-mutagenic)

# of Graphs      	    188 graphs (benchmark size)

Avg. Nodes per Graph	~18 nodes
Avg. Edges per Graph	~40 edges
Node/Atom Features	    Categorical atom labels (interpreted as features)

# Classes	            2 (mutagenic / non-mutagenic)
```

Each graph represents a molecule:

Nodes correspond to atoms

Edges correspond to chemical bonds

Graph label indicates whether the molecule is mutagenic to Salmonella typhimurium or not.

---

## Data Split (Train/Test)
The dataset is split into **70/30** with **stratification by class**:

- `data/train/` : labeled graphs (70%)
- `data/test/`  : unlabeled graphs (30%)

Training labels are provided in:
- `data/train_labels.csv` with columns:
  - `filename`
  - `target`

---

-----------------------
**📊 Evaluation metrics:**
----------------------

In GTA (Graph Topology Ablation), model performance is evaluated using the F1 score rather than simple accuracy.

The F1 score is used because it balances:

correct predictions

false positives

false negatives

This provides a more reliable measure of classification performance than accuracy alone.

**Each submission is evaluated under two conditions:**

F1 Score (Ideal)     — performance on clean topological features

F1 Score (Perturbed) — performance on corrupted topological features

To measure stability, we compute:

Robustness Gap = |F1 Ideal − F1 Perturbed|

A smaller robustness gap indicates a more stable and reliable model.

🏁 Ranking Priority
```
1️⃣ Highest Perturbed F1 Score
2️⃣ Lowest Robustness Gap
3️⃣ Most recent submission
```
--------------------------
📂 Repository Structure
--------------------------
```
gnn-topology-ablation/
│
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── leaderboard.md
│
├── .github/
│   ├── scripts/
│   │   └── process_submission.py
│   └── workflows/
│       └── process_submission.yml
│
├── data/
│   └── MUTAG/
│       ├── test.csv
│       └── train.csv
│
├── docs/
│   ├── index.html
│   ├── leaderboard.css
│   ├── leaderboard.csv
│   ├── leaderboard.js
│   └── readme
│
├── encryption/
│   ├── __init__.py
│   ├── decrypt.py
│   ├── encrypt.py
│   ├── generate_keys.py
│   └── public_key.pem
│
├── leaderboard/
│   ├── __init__.py
│   ├── calculate_scores.py
│   ├── hidden_labels_reader.py
│   ├── render_leaderboard.py
│   ├── score_submission.py
│   └── update_leaderboard.py
│
├── starter_code/
│   ├── baseline.py
│   └── requirements.txt
│
└── submissions/

```
--------------------
⚙️ Getting Started
--------------------

---

## Environment setup

Before training or submitting, set up a Python environment and install dependencies.

### 1. Create a virtual environment

### 2. Install dependencies
From the **project root** (where `requirements.txt` is):
```

## What You Need To Do (Participant)

### Step 1: Train
Train your model using:
- graphs in `data/train/`
- labels in `data/train.csv`

### Step 2: Predict
Predict labels for every graph in:
- `data/test.csv/`

### Step 3: Prepare your submission file
Create a CSV with columns `filename` and `prediction` (same format as `submissions/<team_name>/ideal_submission.csv`):
Create a CSV with columns `filename` and `prediction` (same format as `submissions/<team_name>/Perturbed_submission.csv`):

**Note:** `.csv` files in `submissions/` are git-ignored, so your raw submission will not be pushed. You will submit an **encrypted** version instead.

### Step 4: Encrypt your submission
From the project root, run the encryption script so it can find your CSVs and the encryption key:

```cmd
cd submissions
python encrypt_submissions.py
cd ..
```

This creates a `.enc` files next to each `.csv` in `submissions/<Team_name>/` (e.g. `ideal_submission.csv.enc`). Only `.enc` files are tracked by git; your `.csv` stays local.

### Step 5: Push your encrypted submission
Commit and push the new `.enc` file(s) to the repository (e.g. open a Pull Request or push to the main branch, as per the challenge rules). The automated pipeline will decrypt and score the **latest** `.enc` file in `submissions/` and update the leaderboard.

**Format of these files should be**

```
graph_index,label

160,1
62,0
48,0
173,1
109,1
129,0
.....
```

-------------------------
🚀 Submission Procedure
-------------------------
```
1️⃣ Fork the repository
2️⃣ Place encrypted files inside submissions/<Team_Name>/
3️⃣ Create a new branch
4️⃣ Commit ONLY .enc files
5️⃣ Open a Pull Request
```
Submissions are evaluated automatically.


-----------------------
🏆 Leaderboard System
-----------------------
It maintains:
```
✔ Best score per participant
✔ Public ranking based on Perturbed submission perfromance
```

**📊 Leaderboard Ranking Logic**

For each submission the system records:
```
✔Participant name
✔F1 Ideal
✔F1 Perturbed
✔Robustness Gap
✔Timestamp
```

**Track Live leaderboard:** [Open leaderboard](https://idrees11.github.io/GTA-Graph-Topology-Ablation_-GTA-/)
----------------------
🔒 Security Guarantee
---------------------
```
✔ Predictions encrypted locally
✔ AES key encrypted using RSA public key
✔ Only organiser can decrypt
✔ Files visible but unreadable
✔ Ensures blind evaluation
```
----------------
📜 License
----------------

Released under the MIT License.
-----------------------------------------------------------------------------------------------------------------------

