from multiprocessing.pool import ThreadPool
import json
import copy

import os
import tqdm

from flask import jsonify, make_response
from flask import Flask, request
from flask_restx import Resource, Api

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from parse import parse_outlines
from gencourse import generate_problems
from models import ProblemSet

app = Flask(__name__)
api = Api(app)

@api.route('/gencourse')
class GenCourse(Resource):
    def post(self):
        if 'file' not in request.files:
            return {"message": "No file part in the request"}, 400

        uploaded_file = request.files['file']

        if uploaded_file.filename == '':
            return {"message": "No selected file"}, 400

        uploaded_file.save("temp.pdf")

        outlines = parse_outlines("temp.pdf")

        print("Parsed outlines")

        course = {}

        course["course_title"] = uploaded_file.filename.split(".")[0]
        course["chapters"] = []

        num_sections = sum(len(chapter_sections) for _, chapter_sections in outlines) + len(outlines)

        outlines = tqdm.tqdm(outlines, total=num_sections, desc="Generating course")

        def gen_problems(section):
            title, body = section
            return (title, generate_problems(body, 6, 2).model_dump())

        with ThreadPool(processes=100) as pool:
            for chapter_title, chapter_sections in outlines:
                chapter = {}
                chapter["chapter_title"] = chapter_title
                chapter["sections"] = []

                for section_title, problemset in pool.map(gen_problems, chapter_sections):
                    section = {}
                    section["section_title"] = section_title

                    section["mcqs"] = problemset["mcqs"]
                    section["frqs"] = problemset["frqs"]

                    chapter["sections"].append(section)

                    outlines.update(1)

                outlines.set_postfix_str(chapter_title)

                course["chapters"].append(chapter)
        # print(course)
        outlines.close()

        client.get_database("TextbookTutor").get_collection("Courses").insert_one(copy.copy(course))
        return {"message": "Course generated successfully", "course": course}

if __name__ == '__main__':
    client = MongoClient(os.getenv("MONGODB_URI"), server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
        print("You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    app.run(debug=True)