# Testing System Setup Guide

This guide explains how to use the centralized testing system for your Bioinformática exercises.

## 📁 Files Created

1. **config.py** - Central configuration with all contest variables
2. **test_runner.py** - Automated testing utility
3. **test_history.json** - Automatically created to track your attempts

## 🚀 Quick Start

### Step 1: Configure Your Student ID

Edit `config.py` and update your student ID:

```python
STUDENT_ID = "70879303L"  # Replace with your DNI
```

### Step 2: Install Required Package

```bash
pip install requests
```

### Step 3: Test Your First Exercise

#### Method A: Manual Response
```bash
python test_runner.py --folder "complementaria_tema1_eje1" --response "ACGGTC"
```

#### Method B: Auto-Run Python File
```bash
python test_runner.py --folder "gccontent_tema1_eje3" --run
```

This will:
1. Find the Python file in that folder
2. Run it
3. Capture the output
4. Submit it to the evaluation system

#### Method C: Explicit Session/Exercise
```bash
python test_runner.py --session 1 --exercise 4 --response "42"
```

## 📋 Available Commands

### Test an Exercise
```bash
# By folder name with manual response
python test_runner.py -f "skew_min_skew_tema1_eje4" -r "42"

# By folder name with auto-run
python test_runner.py -f "gccontent_tema1_eje3" --run

# By session and exercise
python test_runner.py -s 1 -e 4 -r "ACGGTC"
```

### Check Your Score
```bash
python test_runner.py --score
```

Output example:
```
YOUR SCORES
============================================================
Session 1: Exercise 1: 3, Exercise 2: 2, Exercise 3: 5
Session 2: Exercise 1: 4
...
============================================================
```

### Check Class Ranking
```bash
python test_runner.py --ranking
```

Output example:
```
CLASS RANKING
============================================================
Tu puntuación: 22 (3º)
Mejor puntuación: 45
Peor puntuación: 10
Puntuación media: 18.4
============================================================
```

### List All Exercises
```bash
python test_runner.py --list
```

### View Test History
```bash
python test_runner.py --history
```

Shows your last 20 test attempts with timestamps and results.

## 🔧 Using in Your Python Code

You can also import and use these utilities directly in your Python scripts:

### Example 1: Test from a Script

```python
from test_runner import test_exercise

# Your code that generates the answer
result = my_algorithm()  # e.g., "ACGGTC"

# Test it
test_exercise(session=1, exercise=4, response=result)
```

### Example 2: Using Config Helpers

```python
from config import build_test_url, format_response

# Format a complex response
answer = {'casa': 2, 'perro': 4}
formatted = format_response(answer)
print(formatted)  # Output: {'casa':2,'perro':4}

# Build a test URL
url = build_test_url(session=2, exercise=3, response=['AAA', 'CCC'])
print(url)
# https://cpg3.der.usal.es/eval/test?session=2&exercise=3&response=['AAA','CCC']&id=YOUR_ID
```

### Example 3: Get Exercise Info

```python
from config import get_exercise_info

info = get_exercise_info("skew_min_skew_tema1_eje4")
session, exercise, description = info
print(f"Testing {description}: Session {session}, Exercise {exercise}")
```

## 📝 Response Formatting Rules

The system automatically formats your responses according to API requirements:

### Strings
```python
response = "ACGGTC"
# Submitted as: ACGGTC
```

### Numbers
```python
response = 56.44789
# Submitted as: 56.448 (rounded to 3 decimals)
```

### Lists
```python
response = ['AAA', 'CCC', 'GGG']
# Submitted as: ['AAA','CCC','GGG']  (single quotes!)
```

### Dictionaries
```python
response = {'casa': 2, 'perro': 4}
# Submitted as: {'casa':2,'perro':4}
```

⚠️ **Important**: The system uses **single quotes** for strings in lists/dicts, not double quotes!

## 🎯 Workflow Recommendation

### For Each Exercise:

1. **Develop your solution** in the exercise folder
2. **Test locally** with sample data
3. **Run via test_runner**:
   ```bash
   python test_runner.py -f "your_exercise_folder" --run
   ```
4. **Check result** - if incorrect, improve your code
5. **Retest** - minimize attempts to maximize score
6. **Check progress**:
   ```bash
   python test_runner.py --score
   ```

### Scoring Tips:

- ✅ Get it right the first time = maximum points
- ⚠️ Every 3 attempts = -1 point penalty
- 🏆 First person to solve = bonus points
- 🎯 Minimum score is always 1 (can't go negative)

## 📊 Exercise Map

All exercises are mapped in `config.py`:

```python
EXERCISE_MAP = {
    "complementaria_tema1_eje1": (1, 1, "Complementaria"),
    "frecuencia_tema1_eje2": (1, 2, "Frecuencia"),
    # ... etc
}
```

To add a new exercise:
1. Add it to `EXERCISE_MAP` in `config.py`
2. Use the folder name format: `description_temaN_ejeM`

## 🔍 Troubleshooting

### "Configuration Issues" Warning
```bash
⚠️  STUDENT_ID not set! Update it in config.py
```
**Solution**: Edit `config.py` and set your DNI.

### "Network error"
```bash
❌ Error: Network error: Connection timeout
```
**Solution**: Check your internet connection. The API might be down.

### "Unknown folder"
```bash
❌ Unknown folder: my_folder
```
**Solution**: Check spelling or run `python test_runner.py --list` to see available folders.

### Python File Not Found
```bash
❌ No Python file found in tema1/my_exercise
```
**Solution**: Ensure your exercise folder contains a `.py` file.

## 🔒 Academic Integrity

Remember:
- ✅ Use this tool to test YOUR OWN solutions
- ❌ Don't share your code with others
- ❌ Don't copy solutions
- ✅ Be able to explain your code
- ✅ Understand what your code does

The professor may ask you to explain your solution. If you can't explain it, you may fail the course even if tests passed.

## 📈 Advanced Usage

### Batch Testing Multiple Exercises

Create a script:

```python
from test_runner import test_by_folder

exercises = [
    ("complementaria_tema1_eje1", None, True),  # auto-run
    ("frecuencia_tema1_eje2", None, True),
    ("gccontent_tema1_eje3", None, True),
]

for folder, response, auto in exercises:
    print(f"\n{'='*60}")
    print(f"Testing {folder}")
    print('='*60)
    test_by_folder(folder, response, auto)
    input("Press Enter to continue...")
```

### Custom Response Parser

If your program outputs complex formats:

```python
import json
from test_runner import test_exercise

# Run your program
output = run_my_program()

# Parse it
if "[" in output:
    response = json.loads(output)  # Parse as list
elif "{" in output:
    response = json.loads(output)  # Parse as dict
else:
    response = output.strip()

# Submit
test_exercise(session=2, exercise=5, response=response)
```

## 📞 Support

If you encounter issues:
1. Check this guide
2. Review the original evaluation document
3. Ask in class
4. Contact the professor

---

**Good luck with your exercises! 🎓**
