from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid

from resume_parser.parser import extract_text_from_pdf
from resume_parser.section_splitter import split_resume_sections
from ai_engine.resume_extractor import extract_resume_data
from ai_engine.question_generator import generate_questions
from models.interview import InterviewSession, Answer
from ai_engine.answer_evaluator import evaluate_answer
from ai_engine.adaptive_question import generate_adaptive_question
from ai_engine.feedback_generator import (
    build_interview_context,
    generate_personalized_feedback
)
from ai_engine.performance_report import (
    calculate_performance_scores,
    generate_performance_report
)


app = FastAPI(title="IntelliInterview API")


# Allow the React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Temporary in-memory storage for interview sessions
interview_sessions = {}


@app.get("/")
def home():
    return {
        "message": "Welcome to IntelliInterview!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "project": "IntelliInterview"
    }


@app.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)):

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        resume_text = extract_text_from_pdf(file_path)

        sections = split_resume_sections(resume_text)

        resume_data = extract_resume_data(
            resume_text,
            sections
        )

        return resume_data.model_dump()

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@app.post("/interview/start")
async def start_interview(file: UploadFile = File(...)):

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:

        # Step 1: Extract resume text
        resume_text = extract_text_from_pdf(
            file_path
        )

        # Step 2: Split resume into sections
        sections = split_resume_sections(
            resume_text
        )

        # Step 3: Extract structured resume data
        resume_data = extract_resume_data(
            resume_text,
            sections
        )

        # Step 4: Generate initial interview questions
        questions_text = generate_questions(
            resume_data
        )

        # Step 5: Extract individual questions
        questions = []

        for line in questions_text.splitlines():

            line = line.strip()

            if not line:
                continue

            if line[0].isdigit():

                parts = line.split(".", 1)

                if len(parts) == 2:

                    question = parts[1].strip()

                    if question:
                        questions.append(question)

        # Step 6: Create a unique session ID
        session_id = str(
            uuid.uuid4()
        )

        # Step 7: Create interview session
        session = InterviewSession(
            session_id=session_id,
            questions=questions,
            current_question_index=0,
            status="in_progress"
        )

        # Step 8: Store session
        interview_sessions[session_id] = session

        # Step 9: Return session information
        return {
            "session_id": session.session_id,
            "status": session.status,
            "total_questions": len(
                session.questions
            ),
            "current_question": (
                session.questions[0]
                if session.questions
                else None
            )
        }

    finally:

        if os.path.exists(file_path):
            os.remove(file_path)


@app.get("/interview/{session_id}/question")
async def get_current_question(
    session_id: str
):

    # Check whether the session exists
    if session_id not in interview_sessions:

        raise HTTPException(
            status_code=404,
            detail="Interview session not found"
        )

    # Get the interview session
    session = interview_sessions[session_id]

    # Check whether the interview is completed
    if session.status == "completed":

        return {
            "session_id": session_id,
            "status": "completed",
            "message": "Interview has already been completed."
        }

    # Get current question index
    current_index = (
        session.current_question_index
    )

    # Check whether questions are available
    if current_index >= len(session.questions):

        session.status = "completed"

        return {
            "session_id": session_id,
            "status": "completed",
            "message": "No more questions available."
        }

    # Get the current question
    current_question = session.questions[
        current_index
    ]

    return {
        "session_id": session_id,
        "status": session.status,
        "question_number": current_index + 1,
        "total_questions": len(
            session.questions
        ),
        "question": current_question
    }


@app.post("/interview/{session_id}/answer")
async def submit_answer(
    session_id: str,
    answer: str
):

    # Check whether the session exists
    if session_id not in interview_sessions:

        raise HTTPException(
            status_code=404,
            detail="Interview session not found"
        )

    # Get the interview session
    session = interview_sessions[session_id]

    # Check whether the interview is completed
    if session.status == "completed":

        raise HTTPException(
            status_code=400,
            detail="Interview has already been completed"
        )

    # Get the current question index
    current_index = session.current_question_index

    # Check whether questions are available
    if current_index >= len(session.questions):

        session.status = "completed"

        raise HTTPException(
            status_code=400,
            detail="No more questions available"
        )

    # Get the current question
    current_question = session.questions[
        current_index
    ]

    # ----------------------------------------
    # STEP 1: Evaluate candidate answer
    # ----------------------------------------

    evaluation = evaluate_answer(
        current_question,
        answer
    )

    # ----------------------------------------
    # STEP 2: Store candidate answer
    # ----------------------------------------

    answer_record = Answer(
        question_number=current_index + 1,
        question=current_question,
        answer=answer,
        evaluation=evaluation
    )

    session.answers.append(
        answer_record
    )

    # ----------------------------------------
    # STEP 3: Build interview context
    # ----------------------------------------

    interview_context = build_interview_context(
        session.answers
    )

    # ----------------------------------------
    # STEP 4: Generate adaptive question
    # ----------------------------------------

    adaptive_question = generate_adaptive_question(
        current_question,
        answer,
        evaluation,
        interview_context
    )

    # ----------------------------------------
    # STEP 5: Move to next question
    # ----------------------------------------

    session.current_question_index += 1

    # Add adaptive question to the interview
    session.questions.append(
        adaptive_question
    )

    # ----------------------------------------
    # STEP 6: Return evaluation + next question
    # ----------------------------------------

    next_question_number = (
        session.current_question_index + 1
    )

    return {
        "session_id": session_id,
        "message": "Answer evaluated successfully",
        "question_number": current_index + 1,
        "evaluation": evaluation,
        "next_question_number": next_question_number,
        "next_question": adaptive_question,
        "status": session.status
    }


@app.post("/interview/{session_id}/feedback")
async def get_personalized_feedback(
    session_id: str
):

    # Check whether the session exists
    if session_id not in interview_sessions:

        raise HTTPException(
            status_code=404,
            detail="Interview session not found"
        )

    # Get the interview session
    session = interview_sessions[session_id]

    # Check whether the candidate has answered
    # at least one question
    if not session.answers:

        raise HTTPException(
            status_code=400,
            detail="No interview answers available for feedback"
        )

    # ----------------------------------------
    # STEP 1: Build interview context
    # ----------------------------------------

    interview_context = build_interview_context(
        session.answers
    )

    # ----------------------------------------
    # STEP 2: Generate personalized feedback
    # ----------------------------------------

    personalized_feedback = (
        generate_personalized_feedback(
            interview_context
        )
    )

    # ----------------------------------------
    # STEP 3: Calculate performance scores
    # ----------------------------------------

    performance_scores = (
        calculate_performance_scores(
            session.answers
        )
    )

    # ----------------------------------------
    # STEP 4: Generate final performance report
    # ----------------------------------------

    performance_report = (
        generate_performance_report(
            interview_context,
            personalized_feedback,
            performance_scores
        )
    )

    # ----------------------------------------
    # STEP 5: Return complete results
    # ----------------------------------------

    return {
        "session_id": session_id,
        "message": "Interview performance report generated successfully",
        "performance_scores": performance_scores,
        "personalized_feedback": personalized_feedback,
        "performance_report": performance_report
    }