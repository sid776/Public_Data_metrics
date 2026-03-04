"""Run the Streamlit Document Intelligence UI."""
import subprocess
import sys

if __name__ == "__main__":
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--server.port=8501"],
        cwd=__file__ and __import__("pathlib").Path(__file__).parent or ".",
    )
