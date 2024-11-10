from langchain_openai import ChatOpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential

from models import ProblemSet

from dotenv import load_dotenv
load_dotenv()

PROMPT = "Please generate a problem set of {} MCQ questions and {} FRQ questions from the following text:\n\n{}"

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_problems(text: str, mcq_count: int, frq_count: int) -> ProblemSet:
    LLM = ChatOpenAI(model="gpt-4o-mini").with_structured_output(ProblemSet)
    return LLM.invoke(PROMPT.format(mcq_count, frq_count, text))