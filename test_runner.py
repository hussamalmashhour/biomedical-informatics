"""
Test Runner for Bioinformática Exercises
==========================================

Automatically tests your exercise solutions against the evaluation system.

Features:
- Run individual exercises
- Run all exercises in a session
- Run all exercises in the workspace
- Track attempts and results
- Save test history

Usage Examples:
    # Test a single exercise
    python test_runner.py --session 1 --exercise 4 --response "ACGGTC"
    
    # Test by folder name
    python test_runner.py --folder "skew_min_skew_tema1_eje4" --response "42"
    
    # Test by running a Python file and using its output
    python test_runner.py --folder "gccontent_tema1_eje3" --run
    
    # Check your score
    python test_runner.py --score
    
    # Check ranking
    python test_runner.py --ranking
"""

import requests
import argparse
import json
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path
import urllib3
import ast

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Import configuration
from config import (
    STUDENT_ID, API_OPERATIONS, EXERCISE_MAP,
    build_test_url, build_calificacion_url, build_ranking_url,
    format_response, get_exercise_info, validate_config
)

# ============================================================================
# TEST HISTORY MANAGEMENT
# ============================================================================

HISTORY_FILE = "test_history.json"

def load_history():
    """Load test history from file."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"tests": []}
    return {"tests": []}

def save_history(history):
    """Save test history to file."""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def add_to_history(session, exercise, response, result, timestamp=None):
    """Add a test result to history."""
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    history = load_history()
    history["tests"].append({
        "timestamp": timestamp,
        "session": session,
        "exercise": exercise,
        "response": str(response),
        "result": result
    })
    save_history(history)

# ============================================================================
# API INTERACTION
# ============================================================================

def test_exercise(session, exercise, response, save_to_history=True):
    """
    Submit a test to the evaluation system.
    
    Args:
        session (int): Session number
        exercise (int): Exercise number
        response: Your answer
        save_to_history (bool): Save result to history
        
    Returns:
        dict: Result with 'success', 'message', 'raw_response'
    """
    try:
        url = build_test_url(session, exercise, response)
        print(f"\n📡 Testing: Session {session}, Exercise {exercise}")
        print(f"🔗 URL: {url}")
        print(f"📝 Response: {format_response(response)}")
        print("\nSending request...")
        
        r = requests.get(url, timeout=10, verify=False)
        result_text = r.text.strip()
        
        # Parse result: detect 'correcto' without being part of 'incorrecto'
        lower = result_text.lower()
        has_correct = ("correcto" in lower) or (" correct" in lower)
        has_incorrect = ("incorrecto" in lower) or (" incorrect" in lower)
        is_correct = has_correct and not has_incorrect
        
        result = {
            'success': is_correct,
            'message': result_text,
            'raw_response': r.text,
            'status_code': r.status_code
        }
        
        # Display result
        if is_correct:
            print("\n✅ CORRECT!")
        else:
            print("\n❌ INCORRECT")
        
        print(f"📋 Server response: {result_text}")
        
        # Save to history
        if save_to_history:
            add_to_history(session, exercise, response, result_text)
        
        return result
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Network error: {str(e)}"
        print(f"\n❌ Error: {error_msg}")
        return {
            'success': False,
            'message': error_msg,
            'raw_response': None,
            'status_code': None
        }

def get_calificacion():
    """Get your score from the evaluation system."""
    try:
        url = build_calificacion_url()
        print(f"\n📊 Fetching your scores...")
        print(f"🔗 URL: {url}")
        
        r = requests.get(url, timeout=10, verify=False)
        print("\n" + "="*60)
        print("YOUR SCORES")
        print("="*60)
        print(r.text)
        print("="*60)
        
        return r.text
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error fetching scores: {str(e)}")
        return None

def get_ranking():
    """Get the class ranking."""
    try:
        url = build_ranking_url()
        print(f"\n🏆 Fetching ranking...")
        print(f"🔗 URL: {url}")
        
        r = requests.get(url, timeout=10, verify=False)
        print("\n" + "="*60)
        print("CLASS RANKING")
        print("="*60)
        print(r.text)
        print("="*60)
        
        return r.text
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error fetching ranking: {str(e)}")
        return None

# ============================================================================
# EXERCISE EXECUTION
# ============================================================================

def find_python_file(folder_path):
    """Find the main Python file in an exercise folder."""
    folder_path = Path(folder_path)
    
    if not folder_path.exists():
        return None
    
    # Look for Python files (excluding __pycache__)
    py_files = [f for f in folder_path.glob("*.py") 
                if not f.name.startswith("_") and f.name != "mutations.py"]
    
    if len(py_files) == 1:
        return py_files[0]
    elif len(py_files) > 1:
        # Try to find the main one based on naming
        for pf in py_files:
            if folder_path.name.startswith(pf.stem):
                return pf
        return py_files[0]  # Return first one if can't determine
    
    return None

def run_exercise_file(file_path, args=None):
    """
    Run a Python exercise file and capture its output.
    
    Args:
        file_path (Path): Path to Python file
        
    Returns:
        str: Output from the program
    """
    try:
        print(f"\n▶️  Running: {file_path.name}")
        # Convert to absolute path
        abs_path = file_path.resolve()
        cmd = [sys.executable, str(abs_path)]
        if args:
            cmd.extend(args)
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(abs_path.parent),
            timeout=30
        )
        
        output = result.stdout.strip()
        
        if result.returncode != 0:
            print(f"⚠️  Program had errors:")
            print(result.stderr)
        
        # For programs with verbose output, get the last non-empty line
        if output:
            lines = [line for line in output.split('\n') if line.strip()]
            if lines:
                last_line = lines[-1].strip()
                print(f"📤 Output: {output}")
                print(f"📤 Last line (used as answer): {last_line}")
                return last_line
        
        print(f"📤 Output: {output}")
        return output
        
    except subprocess.TimeoutExpired:
        print("⚠️  Program execution timed out (30s)")
        return None
    except Exception as e:
        print(f"❌ Error running file: {str(e)}")
        return None

def test_by_folder(folder_name, response=None, auto_run=False):
    """
    Test an exercise by folder name.
    
    Args:
        folder_name (str): Name of exercise folder
        response: Your answer (if None and auto_run=True, will run the file)
        auto_run (bool): Automatically run the Python file
        
    Returns:
        dict: Test result
    """
    # Get exercise info
    ex_info = get_exercise_info(folder_name)
    if not ex_info:
        print(f"❌ Unknown folder: {folder_name}")
        print("Available folders:")
        for name in sorted(EXERCISE_MAP.keys()):
            print(f"  - {name}")
        return None
    
    session, exercise, description = ex_info
    print(f"\n📚 Exercise: {description}")
    print(f"   Session: {session}, Exercise: {exercise}")
    
    # If auto_run, find and execute the file
    if auto_run and response is None:
        # Find folder path - search recursively
        folder_path = None
        workspace_root = Path(".")
        
        # Try to find the folder in tema directories
        for tema_dir in workspace_root.glob("tema*"):
            potential_path = tema_dir / folder_name
            if potential_path.exists():
                folder_path = potential_path
                break
        
        # If not found, search the entire workspace
        if not folder_path:
            for match in workspace_root.rglob(folder_name):
                if match.is_dir():
                    folder_path = match
                    break
        
        if not folder_path:
            print(f"❌ Could not find folder: {folder_name}")
            return None
        
        # Find Python file
        py_file = find_python_file(folder_path)
        if not py_file:
            print(f"❌ No Python file found in {folder_path}")
            return None
        
        # Determine optional input arguments (e.g., FASTA files)
        run_args = None
        fasta = None
        for ext in ("*.fa", "*.fasta", "*.fas"):
            matches = list(folder_path.glob(ext))
            if matches:
                fasta = matches[0]
                break
        if fasta:
            # Pass the file name (relative to script directory)
            run_args = [fasta.name]

        # Run it
        response = run_exercise_file(py_file, run_args)
        if response is None:
            print("❌ Could not get output from program")
            return None

        # Try to parse the response into proper Python types
        if isinstance(response, str):
            parsed = None
            try:
                parsed = ast.literal_eval(response)
            except Exception:
                # If not a Python literal, try converting to float
                try:
                    parsed = float(response.strip())
                except Exception:
                    parsed = response  # keep as string
            response = parsed
    
    if response is None:
        print("❌ No response provided. Use --response or --run")
        return None
    
    # Submit test
    return test_exercise(session, exercise, response)

# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Test runner for Bioinformática exercises",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Test with explicit session/exercise:
    python test_runner.py -s 1 -e 4 -r "ACGGTC"
  
  Test by folder name:
    python test_runner.py -f "skew_min_skew_tema1_eje4" -r "42"
  
  Run Python file and auto-submit:
    python test_runner.py -f "gccontent_tema1_eje3" --run
  
  Check your score:
    python test_runner.py --score
  
  Check class ranking:
    python test_runner.py --ranking
        """
    )
    
    parser.add_argument('-s', '--session', type=int, help='Session number')
    parser.add_argument('-e', '--exercise', type=int, help='Exercise number')
    parser.add_argument('-r', '--response', help='Your answer/response')
    parser.add_argument('-f', '--folder', help='Exercise folder name')
    parser.add_argument('--run', action='store_true', help='Run Python file and use its output')
    parser.add_argument('--score', action='store_true', help='Check your score')
    parser.add_argument('--ranking', action='store_true', help='Check class ranking')
    parser.add_argument('--list', action='store_true', help='List all exercises')
    parser.add_argument('--history', action='store_true', help='Show test history')
    
    args = parser.parse_args()
    
    # Validate configuration
    issues = validate_config()
    if issues:
        print("⚠️  Configuration Issues:")
        for issue in issues:
            print(f"  {issue}")
        print("\nPlease update config.py before testing.\n")
        return 1
    
    # Handle different commands
    if args.score:
        get_calificacion()
        return 0
    
    if args.ranking:
        get_ranking()
        return 0
    
    if args.list:
        print("\n📚 Available Exercises:")
        print("="*60)
        current_session = None
        for folder_name in sorted(EXERCISE_MAP.keys(), 
                                  key=lambda x: EXERCISE_MAP[x][:2]):
            session, exercise, description = EXERCISE_MAP[folder_name]
            if session != current_session:
                print(f"\n--- SESSION {session} ---")
                current_session = session
            print(f"  {exercise:2d}. {description:30s} ({folder_name})")
        print("="*60)
        return 0
    
    if args.history:
        history = load_history()
        print("\n📜 Test History:")
        print("="*60)
        for test in history["tests"][-20:]:  # Show last 20
            timestamp = test['timestamp'][:19]
            result_icon = "✅" if "correcto" in test['result'].lower() else "❌"
            print(f"{result_icon} {timestamp} | S{test['session']}E{test['exercise']} | {test['response'][:30]}")
        print("="*60)
        return 0
    
    # Test an exercise
    if args.folder:
        result = test_by_folder(args.folder, args.response, args.run)
        return 0 if result and result['success'] else 1
    
    if args.session and args.exercise:
        if not args.response:
            print("❌ --response is required when using --session and --exercise")
            return 1
        result = test_exercise(args.session, args.exercise, args.response)
        return 0 if result['success'] else 1
    
    # No command provided
    parser.print_help()
    return 0

if __name__ == "__main__":
    sys.exit(main())
