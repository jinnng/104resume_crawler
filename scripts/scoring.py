import os
import csv
import logging
import re
import sys
import openai
from concurrent.futures import ThreadPoolExecutor
from typing import List
from hunter import scoring

CSV_HEADER = ['Job File', 'Resume File', 'Score_sk', 'Score_wexp', 'Score_rest', 'Shcool', 'Major', 'InList', 'invite']

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(stream_handler)
scoring.logger.addHandler(stream_handler)
scoring.logger.setLevel(logging.DEBUG)

openai.requests_timeout = 120


def get_files(folder: str) -> List[str]:
    return [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith('.txt')]


def extract_score_one_report(result: str):
    score_string = scoring.get_score_one_report(result)
    percentage_pattern = r'(\d+)%'
    percentages = re.findall(percentage_pattern, score_string)
    recommend_pattern = r'Do you recommend an invitation for an interview\?: (\w+)'
    recommendation = re.search(recommend_pattern, score_string).group(1)
    return percentages[0], percentages[1], percentages[2], recommendation


def write_report_to_file(report_folder: str, report_file: str, result: str):
    if not os.path.exists(report_folder):
        os.makedirs(report_folder)
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(result)


def match_pair(job_requirements_file: str, resume_file: str, report_folder: str):
    try:
        job_requirements_contents = open(job_requirements_file, "r", encoding='utf-8').read()
        resume_contents = open(resume_file, "r", encoding='utf-8').read()

        school, major, in_list = scoring.match_school(resume_contents)
        analysis_result = scoring.get_report_gpt_4_once(job_requirements_contents, resume_contents)
        skill_score, work_exp_score, other_score, fit_for_interview = extract_score_one_report(analysis_result)

        report_file = os.path.join(report_folder,
                                   f"{os.path.basename(resume_file)}_{os.path.basename(job_requirements_file)}_report.txt")
        write_report_to_file(report_folder, report_file, analysis_result)
        return os.path.basename(job_requirements_file), os.path.basename(resume_file), skill_score, work_exp_score, other_score, \
            school, major, in_list, fit_for_interview
    except Exception as e:
        print(f"Error: {e}")
        return os.path.basename(job_requirements_file), os.path.basename(resume_file), 0, 0, 0, "", "", str(e), ""


def generate_report(output_csv, matching_results):
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(CSV_HEADER)
        for result in matching_results:
            csv_writer.writerow(result)


def match_resumes_and_jobs_gpt4(jobs_folder: str, resumes_folder: str, num_threads: int, output_csv: str,
                                report_folder: str):
    job_requirements_files = get_files(jobs_folder)
    resume_files = get_files(resumes_folder)

    matching_results = []

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for job_requirements_file in job_requirements_files:
            for resume_file in resume_files:
                futures.append(executor.submit(match_pair, job_requirements_file, resume_file, report_folder))

        for future in futures:
            matching_results.append(future.result())

    generate_report(output_csv, matching_results)
    return matching_results
