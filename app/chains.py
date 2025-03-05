import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0.7, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills`, `description`, and `contact_info`.
            Look for contact information in the footer, header, or contact sections.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        styles = [
            "professional and formal",
            "friendly and enthusiastic",
            "direct and value-focused",
            "consultative and solution-oriented",
            "data-driven and analytical"
        ]
        
        emails = []
        for style in styles:
            prompt_email = PromptTemplate.from_template(
                """
                ### JOB DESCRIPTION:
                {job_description}

                ### INSTRUCTION:
                You are Mohan, a business development executive at AtliQ. AtliQ is an AI & Software Consulting company dedicated to facilitating
                the seamless integration of business processes through automated tools. 
                Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
                process optimization, cost reduction, and heightened overall efficiency.
                
                Write a cold email in a {style} tone. Focus on how AtliQ can fulfill their needs.
                Add 2-3 most relevant links from: {link_list} to showcase Atliq's portfolio.
                Remember you are Mohan, BDE at AtliQ.
                
                Keep the email concise and impactful.
                Do not provide a preamble.
                ### EMAIL (NO PREAMBLE):
                """
            )
            chain_email = prompt_email | self.llm
            res = chain_email.invoke({
                "job_description": str(job), 
                "link_list": links,
                "style": style
            })
            emails.append(res.content)
        
        return emails

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))