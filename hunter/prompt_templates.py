from langchain.prompts import PromptTemplate


scoring_prompt_one_report = PromptTemplate(
    input_variables=["report"],
    template="""
{report}


上面 Report中的 Final Report 中 Skill matching percentage / Work experience matching percentage / Other matching percentage 的是數值為何？
以及 Final Report 中的 Do you recommend an invitation for an interview? 為何？

回覆格式:

Skill matching percentage: [score]%
Work experience matching percentage: [score]%
Other matching percentage: [score]%
Do you recommend an invitation for an interview?: [Yes/No]
""")


find_school_prompt = PromptTemplate(
    input_variables=["resume", "school_list"],
    template="""
    請幫我比對這份履歷中的學歷學校，看看是否出現在下面提供的學校列表中。


####學校列表開始
{school_list}
####學校列表結束


####履歷開始
{resume}
####履歷結束






回覆格式：
[履歷中的最高學歷學校],[科系],[是否在列表內]
如果履歷中沒有學歷資訊，回答 None

回覆範例(有學歷)：
國立台灣大學,資訊工程,Y
私立逢甲大學,企業管理,N
回覆範例(沒學歷)：
None,None,None
    """)


gpt_4_once_tot_prompt_str = """
As an AI interviewer, you are about to match between ”the skills mentioned / work experience with the job responsibilities / personal attributes and soft skills “ in the resume and skills required for the job, and provide the matching percentage(full marks are 100% represents a perfect match).

Here is the written description of the candidate:
=====start Candidate Resume======
{resume}
=====end Candidate Resume======

The job description for the position they're applying for is as follows:
====start Job Description=====
{job_description}
====end Job Description=====

Please take into consideration the following situation and adjust the matching percentage:
1. if all the skills is not mentioned in the resume, report a 0% match.
1. if the candidate's work experience is in a different domain compared to the job description, report a 0% match.


You must formulate and play the role of three interview The three experts are:
- Senior technical experts in the field: good at judging whether the skills mentioned in the resume are true and meet the needs of the position.
- Department Head: Good at assessing whether work experience and skills are authentic and meet the needs of the position.
- HR expert: good at assessing personality traits and judging the authenticity of resumes.

Experts analyze the interviewer respectively, and each expert must express opinions on the three aspects of Skill/work experience/personal attributes and soft skills and give scores according to regulations, and integrate them The opinions of three experts produced the final results.Please analyze carefully step by step.

====output format=====

[Role]:

Skill Analysis report: [Role analysis report]
Skill matching percentage: [Role matching percentage]

Work Analysis report: [Role analysis report]
Work experience matching percentage: [Role matching percentage]


Other Analysis report: [Role analysis report]
Other matching percentage: Role matching percentage]

Reasons for recommending invitation for interview evaluation: [Role analysis report]
Do you recommend an invitation for an interview? [Role decide Y/N]



Final Report:
Skill Analysis report: [analysis report]
Skill matching percentage: [matching percentage]

Work Analysis report: [analysis report]
Work experience matching percentage: [matching percentage]

Other Analysis report: [analysis report]
Other matching percentage: [matching percentage]

Reasons for recommending invitation for interview evaluation: [ analysis report]
Do you recommend an invitation for an interview?
"""

gpt_4_once_tot_prompt = PromptTemplate(
    input_variables=["resume", "job_description"],
    template=gpt_4_once_tot_prompt_str)
