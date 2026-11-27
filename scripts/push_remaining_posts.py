import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)

sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "my_account"))

from recreate_all_upcoming_posts import VERSATILE_PIPELINE, RAW_BASE
from buffer_publisher import schedule_buffer_post

p9 = VERSATILE_PIPELINE[8]
p10 = VERSATILE_PIPELINE[9]

print("Scheduling Post 9...")
r9 = schedule_buffer_post(post_text=p9['text'], due_at=p9['due_at'])
print("Post 9 scheduled:", r9.get("id") if r9 else r9)

print("Scheduling Post 10...")
r10 = schedule_buffer_post(
    post_text=p10['text'],
    due_at=p10['due_at'],
    document_url=f"{RAW_BASE}/{p10['pdf_name']}",
    document_title=p10['doc_title'],
    thumbnail_url=f"{RAW_BASE}/{p10['cover_name']}"
)
print("Post 10 scheduled:", r10.get("id") if r10 else r10)
