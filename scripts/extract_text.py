import os
from scripts.parser import extract_text_from_html_folder


def extract_text(batch_folder):
    html_source_folder = os.path.join(batch_folder, 'resume')
    text_resume_folder = os.path.join(batch_folder, 'resume_text')
    os.makedirs(text_resume_folder, exist_ok=True)
    extract_text_from_html_folder(html_source_folder, text_resume_folder)
