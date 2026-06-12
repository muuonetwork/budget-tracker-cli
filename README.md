# 💰 Budget Tracker CLI

A command-line tool to manage personal budgets for multiple users. Built with Python using `argparse` for the CLI and `rich` for beautiful terminal output.

---

## 📁 Project Structure

```
budget_tracker/
├── main.py                  # Entry point
├── requirements.txt         # Dependencies
├── data/                    # JSON persistence files
│   ├── users.json
│   ├── categories.json
│   └── transactions.json
├── models/                  # OOP data models
│   ├── user.py
│   ├── category.py
│   └── transaction.py
├── cli/                     # CLI command handlers
│   ├── user_commands.py
│   ├── category_commands.py
│   ├── transaction_commands.py
│   └── report_commands.py
├── utils/                   # Helpers (storage + display)
│   ├── storage.py
│   └── display.py
└── tests/                   # Pytest unit tests
    ├── test_models.py
    └── test_storage.py
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd budget_tracker
```

### 2. Create and activate a virtual environment
```bash
# Create the virtual environment
python -m venv venv

# Activate it (Mac/Linux)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### Users
```bash
# Add a user
python main.py add-user --name "Alex" --email "alex@example.com"

# List all users
python main.py list-users

# Delete a user
python main.py delete-user --name "Alex"
```

### Categories (Budget Categories per User)
```bash
# Add a category (optionally with a monthly budget limit)
python main.py add-category --user "Alex" --name "Food" --limit 5000

# List all categories
python main.py list-categories

# Filter by user
python main.py list-categories --user "Alex"

# Edit a category's budget limit
python main.py edit-category --user "Alex" --name "Food" --limit 6000
```

### Transactions (Income & Expenses)
```bash
# Add an expense
python main.py add-transaction --user "Alex" --category "Food" --title "Lunch" --amount 350

# Add an income
python main.py add-transaction --user "Alex" --category "Salary" --title "Monthly pay" --amount 50000 --type income

# Add with a specific date
python main.py add-transaction --user "Alex" --category "Food" --title "Dinner" --amount 800 --date 2025-06-10

# List transactions for a user
python main.py list-transactions --user "Alex"

# Filter by category
python main.py list-transactions --user "Alex" --category "Food"

# Mark a transaction as completed/reconciled
python main.py complete-transaction --id <transaction_id>

# Delete a transaction
python main.py delete-transaction --id <transaction_id>
```

### Reports
```bash
# Income vs expense summary
python main.py summary --user "Alex"

# Per-category spending breakdown
python main.py category-report --user "Alex"
```

---

## 🧪 Running Tests

```bash
pytest tests/
```

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `rich` | Colorful tables and styled terminal output |
| `pytest` | Unit testing framework |

---

## 🗂 Data Relationships

```
User (1)
 └── Category (many)
      └── Transaction (many)
```

- One user can have many budget categories (Food, Transport, Rent, etc.)
- One category can have many transactions (individual expenses or income entries)
- Transactions can be marked as "completed" (reconciled)
