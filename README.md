# 🧠 GradeWise – AI-Powered Essay Grading System

A **FastAPI + React** application that automates the essay grading process.  
It’s designed to help educators save time by delegating long and time-consuming grading tasks to artificial intelligence — allowing them to focus on higher-value areas of their work.

---

## 🎯 Problem Statement

After conducting multiple surveys and speaking directly with educators, several recurring problems and challenges were identified:

- ⏰ **Time-consuming manual grading**
- 📚 **Overload during exam seasons**
- ⚖️ **Inconsistent scoring among educators**

---

## 💡 How GradeWise Solves These Challenges

| Challenge | Solution |
|------------|-----------|
| Manual grading takes hours | Automates essay evaluation, reducing grading time from hours to minutes. |
| Overload during exams | Handles large volumes of essays simultaneously through asynchronous processing. |
| Inconsistent scoring | Ensures uniform and objective grading by applying consistent rubrics and AI-based evaluation. |

---

## 🛠 Tech Stack

<p align="center">
  <img src="https://skillicons.dev/icons?i=react,tailwind,python,fastapi,mysql,aws,docker,githubactions" alt="Tech Stack Icons" />
</p>

**Frontend:** React, TailwindCSS  
**Backend:** Python, FastAPI  
**Database:** MySQL  
**Third-Party Platforms:** Google Cloud Vision API, OpenAI, Amazon SQS  
**Deployment:** Docker, AWS, GitHub Actions  

---

## 🧩 System Architecture
> _Insert architecture diagram here_

![System Architecture](docs/system-architecture.png)

---

## 🗃️ Database Schema
> _Insert database schema screenshot here_

![Database Schema](docs/database-schema.png)

---

## 🧠 Lessons Learned

- Initially processed essays **synchronously**, which caused server timeouts. Learned to move grading tasks to **Celery workers** for better scalability.
- **Overlooked prompt engineering** led to inaccurate and unstructured model responses. Learned to craft clear, concise prompts to extract better and more consistent outputs from the LLM.

---

## 🚀 Future Improvements

- Add analytics dashboard for student performance tracking.  
- Implement support for multiple grading rubrics per course.  
- Introduce multilingual essay evaluation support.

---

### 👤 Author
**GradeWise Project**  
Built with ❤️ using FastAPI, React, and AI technologies.
