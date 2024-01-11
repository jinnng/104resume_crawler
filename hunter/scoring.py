import logging
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from hunter.params import school_list
from hunter.prompt_templates import find_school_prompt, gpt_4_once_tot_prompt, scoring_prompt_one_report

logger = logging.getLogger(__name__)
default_model = "gpt-4-32k"


def divide_content_with_overlap(s, length, overlap):
    return [s[i: i + length] for i in range(0, len(s) - overlap, length - overlap)]


def matching_successful(school: str):
    if school == "None":
        return False
    else:
        return True


def match_school_once(resume_contents: str):
    divided_contents = divide_content_with_overlap(resume_contents, 1800, 50)
    llm = ChatOpenAI(temperature=0, model_name=default_model, request_timeout=240)
    chain = LLMChain(llm=llm, prompt=find_school_prompt)
    for r_str in divided_contents:
        result = chain.run(resume=r_str, school_list=school_list)
        result = result.split("\n")
        school, major, in_list = result[0].split(",")
        if matching_successful(school):
            return school, major, in_list
        else:
            continue
    return "None", "None", "None"


def match_school(resume_contents: str):
    # if match_school_once first result is None, then retry. max 3times
    for i in range(3):
        school, major, in_list = match_school_once(resume_contents)
        if matching_successful(school):
            return school, major, in_list
        else:
            continue
    return "None", "None", "None"


def get_report_gpt_4_once(job_requirements_contents, resume_contents, temperature=0.2, model_name=default_model):
    llm = ChatOpenAI(temperature=temperature, model_name=model_name, request_timeout=240)
    prompt = gpt_4_once_tot_prompt
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(resume=resume_contents, job_description=job_requirements_contents)


def get_score_one_report(report, temperature=0, model_name='gpt-3.5-turbo'):
    llm = ChatOpenAI(temperature=temperature, model_name=model_name, request_timeout=240)
    prompt = scoring_prompt_one_report
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(report=report)
