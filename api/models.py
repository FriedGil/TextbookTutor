from pydantic import BaseModel, Field

class MCQQuestion(BaseModel):
    question: str = Field(title="Question", description="The question to ask", example="What causes a segmentation fault?")
    options: list[str] = Field(title="Options", description="The options to choose from", example=["Dereferencing a NULL pointer", "Dividing by zero", "Using an uninitialized variable", "All of the above"])
    answer: int = Field(title="Answer", description="The index of the correct answer", example=3)

class FRQQuestion(BaseModel):
    question: str = Field(title="Question", description="The question to ask", example="Why is C considered a successful programming language?")

class ProblemSet(BaseModel):
    frqs: list[FRQQuestion] = Field(title="FRQs", description="The free response questions in the problem set", example=[FRQQuestion(question="Why is C considered a successful programming language?")])
    mcqs: list[MCQQuestion] = Field(title="MCQs", description="The multiple choice questions in the problem set", example=[MCQQuestion(question="What causes a segmentation fault?", options=["Dereferencing a NULL pointer", "Dividing by zero", "Using an uninitialized variable", "All of the above"], answer=3)])