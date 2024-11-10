from flask import Flask

app = Flask(__name__)

from flask import Flask, request

# from langchain.llms import OpenAI
#
# from langchain.chains.summarize import load_summarize_chain
# from langchain.chains.question_answering import load_qa_chain
#
# from langchain.docstore.document import Document
# import os
#
# API_KEY = os.environ.get('VITE_OPENAI_API_KEY')

app = Flask(__name__)
# model = OpenAI(openai_api_key=API_KEY, temperature=0.9)
#
# sum_chain = load_summarize_chain(model, chain_type="map_reduce")
# qna_chain = load_qa_chain(model, chain_type="stuff")
#
# @app.route("/api/docs", methods=["POST"])
# def docs():
#     docs = [Document(page_content=doc) for doc in request.json["docs"]]
#     res = qna_chain.run(input_documents = docs, question = "Summarize this document.")
#     return res
#
# @app.route("/api/qna", methods=["POST"])
# def qna():
#     docs = [Document(page_content=doc) for doc in request.json["docs"]]
#     res = qna_chain.run(input_documents = docs, question = request.json["question"])
#     return res

@app.route("/api/")
def index():
    return "shhh"

if __name__ == "__main__":
    app.run()