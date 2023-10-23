"""for pythonanywhere"""

# Flask
import sys

username = 'kotofos'
path = f'/home/{username}/split_sub'
if path not in sys.path:
    sys.path.insert(0, path)

from src.app import app as application  # noqa
