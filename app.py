import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
# Function to generate KPIs based on the provided inputs

def llm_config():
    model_name = "gemini-1.5-flash-001"
    
    genai.configure(api_key=os.getenv("api_key"))

    llm = genai.GenerativeModel(
        model_name=model_name
    )
    return llm


def generate_kpis(company_goals, department_goals, jd):
    prompt = f"""
            You are an expert in business performance metrics and KPIs. Based on the following inputs, generate Weekly, Monthly, 
            and Quarterly KPIs for a company:

            1. **Company Goals:** 
            {company_goals}

            2. **Department Goals:** 
            {department_goals}

            3. **Job Description (JD):** 
            {jd}

            ### Generate KPIs:

            - **Weekly KPIs**: Include performance metrics that can be tracked on a weekly basis related to the company's, department's,
                and the job's specific goals.

            - **Monthly KPIs**: Include metrics that evaluate the company's progress over a monthly period.
            
            - **Quarterly KPIs**: Include high-level KPIs for assessing the company and department's overall performance quarterly.

            Make sure the KPIs align with the goals and job responsibilities provided.
            """


    llm=llm_config()
    completion = llm.generate_content(prompt , generation_config={
        'temperature':0
    })
    answer= completion.text
    # answer = re.sub(r"[\`*]", "", answer)
    # answer = re.sub(r"json", "", answer)
    # answer = re.sub(r"\\n", " ", answer)
    

    return answer


st.title("KPI Generator")

# Text input fields
company_goals = st.text_area("Enter Company Goals", placeholder="Increase revenue by 15%, expand market by 20%, etc.")
department_goals = st.text_area("Enter Department Goals", placeholder="Sales goal, marketing goal, product development goal, etc.")
jd = st.text_area("Enter Job Description (JD)", placeholder="Product Manager responsibilities, sales executive duties, etc.")

# Button to generate KPIs
if st.button("Generate KPIs"):
    if company_goals and department_goals and jd:
        # Call the function to generate KPIs based on the inputs
        kpis = generate_kpis(company_goals, department_goals, jd)
        st.markdown(kpis)
    else:
        st.error("Please fill out all fields to generate KPIs.")
