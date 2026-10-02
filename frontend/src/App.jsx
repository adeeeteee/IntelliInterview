import { useRef, useState } from "react";
import "./App.css";

function App() {
  const fileInputRef = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [resumeData, setResumeData] = useState(null);

  const [loading, setLoading] = useState(false);
  const [startingInterview, setStartingInterview] = useState(false);
  const [submittingAnswer, setSubmittingAnswer] = useState(false);
  const [finishingInterview, setFinishingInterview] = useState(false);

  const [error, setError] = useState("");

  const [interviewSession, setInterviewSession] = useState(null);

  const [currentQuestion, setCurrentQuestion] = useState("");
  const [currentQuestionNumber, setCurrentQuestionNumber] = useState(1);

  const [answer, setAnswer] = useState("");
  const [evaluation, setEvaluation] = useState("");

  const [performanceReport, setPerformanceReport] = useState(null);

  const handleUploadClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = async (event) => {
    const file = event.target.files[0];

    if (!file) {
      return;
    }

    setError("");
    setResumeData(null);
    setInterviewSession(null);
    setEvaluation("");
    setAnswer("");
    setPerformanceReport(null);

    if (file.type !== "application/pdf") {
      setSelectedFile(null);
      setError("Please select a PDF resume.");
      return;
    }

    setSelectedFile(file);

    const formData = new FormData();

    formData.append("file", file);

    try {
      setLoading(true);

      const response = await fetch(
        "http://127.0.0.1:8000/resume/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Resume upload failed.");
      }

      const data = await response.json();

      setResumeData(data);
    } catch {
      setError(
        "Could not connect to the IntelliInterview backend."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleStartInterview = async () => {
    if (!selectedFile) {
      setError("Please upload a resume first.");
      return;
    }

    setError("");

    const formData = new FormData();

    formData.append("file", selectedFile);

    try {
      setStartingInterview(true);

      const response = await fetch(
        "http://127.0.0.1:8000/interview/start",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error(
          "Interview could not be started."
        );
      }

      const data = await response.json();

      setInterviewSession(data);

      setCurrentQuestion(
        data.current_question
      );

      setCurrentQuestionNumber(1);

      setAnswer("");
      setEvaluation("");
      setPerformanceReport(null);
    } catch {
      setError("Could not start the interview.");
    } finally {
      setStartingInterview(false);
    }
  };

  const handleSubmitAnswer = async () => {
    if (!answer.trim()) {
      setError(
        "Please enter an answer before submitting."
      );
      return;
    }

    if (!interviewSession) {
      setError(
        "Please start the interview first."
      );
      return;
    }

    setError("");

    try {
      setSubmittingAnswer(true);

      const response = await fetch(
        `http://127.0.0.1:8000/interview/${interviewSession.session_id}/answer?answer=${encodeURIComponent(
          answer
        )}`,
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        throw new Error(
          "Answer submission failed."
        );
      }

      const data = await response.json();

      setEvaluation(data.evaluation);

      setCurrentQuestion(
        data.next_question
      );

      setCurrentQuestionNumber(
        data.next_question_number
      );

      setAnswer("");
    } catch {
      setError(
        "Could not submit your answer."
      );
    } finally {
      setSubmittingAnswer(false);
    }
  };

  const handleFinishInterview = async () => {
    if (!interviewSession) {
      setError(
        "Please start the interview first."
      );
      return;
    }

    setError("");

    try {
      setFinishingInterview(true);

      const response = await fetch(
        `http://127.0.0.1:8000/interview/${interviewSession.session_id}/feedback`,
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        throw new Error(
          "Performance report could not be generated."
        );
      }

      const data = await response.json();

      setPerformanceReport(data);
    } catch {
      setError(
        "Could not generate the performance report."
      );
    } finally {
      setFinishingInterview(false);
    }
  };

  return (
    <div className="app">

      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <span className="logo-icon">AI</span>

            <div>
              <h1>IntelliInterview</h1>
              <p>AI-Powered Interview Preparation</p>
            </div>
          </div>
        </div>
      </header>


      {/* Main Content */}
      <main className="main-container">

        {!interviewSession &&
          !performanceReport && (
            <section className="intro-section">

              <h2>
                Prepare Smarter.
                <br />
                Interview Better.
              </h2>

              <p>
                Upload your resume and practice a
                personalized AI-powered interview based
                on your skills, projects and experience.
              </p>

            </section>
          )}


        {/* Error */}
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}


        {/* Upload Section */}
        {!interviewSession &&
          !performanceReport && (

            <section className="card upload-card">

              <div className="upload-icon">
                ↑
              </div>

              <h2>
                Upload Your Resume
              </h2>

              <p>
                Upload your resume in PDF format to
                generate personalized interview questions.
              </p>

              <input
                type="file"
                accept=".pdf"
                ref={fileInputRef}
                onChange={handleFileChange}
                style={{ display: "none" }}
              />

              <button
                className="primary-button"
                onClick={handleUploadClick}
                disabled={
                  loading ||
                  startingInterview
                }
              >
                {loading
                  ? "Analyzing Resume..."
                  : "Choose Resume"}
              </button>

              {selectedFile && (
                <div className="file-name">
                  📄 {selectedFile.name}
                </div>
              )}

            </section>
          )}


        {/* Resume Result */}
        {resumeData &&
          !interviewSession &&
          !performanceReport && (

            <section className="card resume-card">

              <div className="success-icon">
                ✓
              </div>

              <h2>
                Resume Processed Successfully
              </h2>

              <p className="welcome-text">
                Welcome,{" "}
                <strong>
                  {resumeData.name}
                </strong>
              </p>

              <div className="resume-stats">

                <div className="stat-box">
                  <span className="stat-number">
                    {resumeData.skills?.length || 0}
                  </span>

                  <span className="stat-label">
                    Skills Detected
                  </span>
                </div>

                <div className="stat-box">
                  <span className="stat-number">
                    {resumeData.projects?.length || 0}
                  </span>

                  <span className="stat-label">
                    Projects Detected
                  </span>
                </div>

              </div>

              <button
                className="primary-button"
                onClick={handleStartInterview}
                disabled={startingInterview}
              >
                {startingInterview
                  ? "Starting Interview..."
                  : "Start Interview"}
              </button>

            </section>
          )}


        {/* Interview Section */}
        {interviewSession &&
          !performanceReport && (

            <section className="card interview-card">

              <div className="interview-header">

                <div>
                  <span className="section-label">
                    AI INTERVIEW
                  </span>

                  <h2>
                    Question {currentQuestionNumber}
                  </h2>
                </div>

                <div className="live-badge">
                  ● LIVE
                </div>

              </div>


              <div className="question-box">

                <span className="question-label">
                  INTERVIEW QUESTION
                </span>

                <h3>
                  {currentQuestion}
                </h3>

              </div>


              <div className="answer-section">

                <label htmlFor="answer">
                  Your Answer
                </label>

                <textarea
                  id="answer"
                  value={answer}
                  onChange={(event) =>
                    setAnswer(
                      event.target.value
                    )
                  }
                  placeholder="Type your answer here..."
                  rows={7}
                  disabled={
                    submittingAnswer ||
                    finishingInterview
                  }
                />

                <div className="button-row">

                  <button
                    className="primary-button"
                    onClick={handleSubmitAnswer}
                    disabled={
                      submittingAnswer ||
                      finishingInterview
                    }
                  >
                    {submittingAnswer
                      ? "Evaluating Answer..."
                      : "Submit Answer"}
                  </button>

                  <button
                    className="secondary-button"
                    onClick={
                      handleFinishInterview
                    }
                    disabled={
                      finishingInterview ||
                      submittingAnswer
                    }
                  >
                    {finishingInterview
                      ? "Generating Report..."
                      : "Finish Interview"}
                  </button>

                </div>

              </div>


              {/* Current Evaluation */}
              {evaluation && (

                <div className="evaluation-card">

                  <div className="evaluation-header">
                    <span className="evaluation-icon">
                      ✓
                    </span>

                    <h3>
                      AI Evaluation
                    </h3>
                  </div>

                  <div className="formatted-text">
                    {evaluation}
                  </div>

                </div>

              )}

            </section>
          )}


        {/* Performance Report */}
        {performanceReport && (

          <section className="report-container">

            <div className="report-header">

              <span className="report-icon">
                ✓
              </span>

              <h2>
                Interview Performance Report
              </h2>

              <p>
                Your personalized interview analysis
                is ready.
              </p>

            </div>


            {/* Overall Score */}
            <div className="card overall-card">

              <span className="section-label">
                OVERALL PERFORMANCE
              </span>

              <div className="overall-score">
                {
                  performanceReport
                    .performance_scores
                    ?.overall || 0
                }

                <span>
                  /10
                </span>
              </div>

              <p>
                Overall Interview Score
              </p>

            </div>


            {/* Category Scores */}
            <div className="card">

              <h3 className="card-title">
                Category Scores
              </h3>

              <div className="score-grid">

                <div className="score-item">
                  <span>
                    Relevance
                  </span>

                  <strong>
                    {
                      performanceReport
                        .performance_scores
                        ?.relevance || 0
                    }/10
                  </strong>
                </div>


                <div className="score-item">
                  <span>
                    Content Accuracy
                  </span>

                  <strong>
                    {
                      performanceReport
                        .performance_scores
                        ?.content_accuracy || 0
                    }/10
                  </strong>
                </div>


                <div className="score-item">
                  <span>
                    Completeness
                  </span>

                  <strong>
                    {
                      performanceReport
                        .performance_scores
                        ?.completeness || 0
                    }/10
                  </strong>
                </div>


                <div className="score-item">
                  <span>
                    Clarity
                  </span>

                  <strong>
                    {
                      performanceReport
                        .performance_scores
                        ?.clarity || 0
                    }/10
                  </strong>
                </div>

              </div>

            </div>


            {/* Personalized Feedback */}
            <div className="card feedback-card">

              <h3 className="card-title">
                Personalized Feedback
              </h3>

              <div className="formatted-text">
                {
                  performanceReport
                    .personalized_feedback
                }
              </div>

            </div>


            {/* Final Performance Analysis */}
            <div className="card feedback-card">

              <h3 className="card-title">
                Final Performance Analysis
              </h3>

              <div className="formatted-text">
                {
                  performanceReport
                    .performance_report
                }
              </div>

            </div>


            <div className="completion-message">
              🎉 Interview completed successfully!
            </div>

          </section>

        )}

      </main>

    </div>
  );
}

export default App;