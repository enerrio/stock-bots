import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bot import post

if __name__ == "__main__":
    post.run()
