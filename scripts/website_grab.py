import os
import re
import json
from datetime import datetime
from scripts.scoring import match_resumes_and_jobs_gpt4
from download_resume import download_resume
from extract_text import extract_text

MAX_WORKER = 4
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
WORKSPACE = os.getenv('WORKSPACE', './')
BATCH_FOLDER = os.path.join(WORKSPACE, TIMESTAMP)
TEXT_RESUME_FOLDER = os.path.join(BATCH_FOLDER, 'resume_text')
REPORT_FOLDER = os.path.join(BATCH_FOLDER, 'report')


def load_processed_idnos(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_processed_idnos(filepath, idnos):
    with open(filepath, 'w') as f:
        json.dump(idnos, f)


def start_processing():
    try:
        # make sure batch folder exists
        os.makedirs(BATCH_FOLDER, exist_ok=True)
        processed_idnos_filepath = os.path.join(WORKSPACE, 'processed_idnos.json')
        processed_idnos = load_processed_idnos(processed_idnos_filepath)

        # Part 1 Download resume
        print('Part 1 Download resume from 104')
        download_resume(processed_idnos, BATCH_FOLDER)

        # Part 2 Extract text from HTML files
        print('Part 2 Extract text from HTML files')
        extract_text(BATCH_FOLDER)

        # Part 3 Matching
        print('Part 3 Matching')
        result = match_resumes_and_jobs_gpt4(os.path.join(WORKSPACE, 'job'), TEXT_RESUME_FOLDER,
                                             MAX_WORKER, os.path.join(BATCH_FOLDER, f"match_report_{TIMESTAMP}.csv"),
                                             REPORT_FOLDER)
        save_processed_idnos(processed_idnos_filepath, processed_idnos)

        #  Part 4 Packaging the results
        print('Part 4 Transfer data to the frontend')
        parsed_results = []

        for index, data in enumerate(result):
            person_name = re.search(r'_(?:[^_]+_){2}(.+?)\.txt', data[1]).group(1)
            school = data[5]
            major = data[6]
            is_invited = data[8]
            parse_result = {"__index": index, "person_name": person_name, "school": school, "major": major,
                            "isInvited": is_invited}
            parsed_results.append(parse_result)

        return parsed_results

    except Exception as ex:
        import traceback

        traceback.print_exc()


if __name__ == '__main__':
    start_processing()
