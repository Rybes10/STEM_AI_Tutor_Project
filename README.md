# STEM AI Tutor

A chatbot that helps you learn STEM. You can ask it questions, and you can take quizzes. It runs as a small website, and it also has a version for the terminal.

It uses **Python**, **Flask**, and the **OpenAI API**.

**Live demo:** https://stem-ai-tutor-chatbot.onrender.com

> The demo runs on a free plan. It goes to sleep when nobody visits. The first visit can take about a minute to wake it up. Please wait.

> This was a team project. See [Credits](#credits).

## What It Can Do

- **Ask questions.** Pick a subject and ask anything. The tutor answers like a teacher for that subject.
- **Take quizzes.** Choose how many questions you want. The AI makes each question. The app checks your answer and gives your score at the end.
- **Nice formatting.** The tutor's answers show lists, bold text, and code blocks.
- **Four subjects.** Each subject has its own tutor style:

| Mode | Subject | What the tutor focuses on |
| --- | --- | --- |
| `math` | Mathematics | Step-by-step solutions and practice problems |
| `science` | Science | Physics, chemistry, and biology with real-world examples |
| `tech` | Technology and computer science | Programming ideas with code examples |
| `engineering` | Engineering | Applied math, physics, and design |

## What You Need

- Python 3.8 or newer
- An [OpenAI API key](https://platform.openai.com/api-keys) with some credit on the account
- The packages in `requirements.txt`

## Setup

### 1. Get the code

```bash
git clone https://github.com/Rybes10/STEM_AI_Tutor_Project.git
cd STEM_AI_Tutor_Project
```

### 2. Make a virtual environment

```bash
python -m venv venv
```

Turn it on:

```bash
venv\Scripts\activate           # Windows
source venv/bin/activate        # Mac or Linux
```

### 3. Install the packages

```bash
pip install -r requirements.txt
```

This project uses the older OpenAI package (`openai==0.28.1`). It is already listed in `requirements.txt`.

### 4. Add your API key

The app reads your key from an environment variable. **Never put your key in the code.**

Windows (PowerShell):

```powershell
$env:OPENAI_API_KEY="your-key-here"
```

Mac or Linux:

```bash
export OPENAI_API_KEY="your-key-here"
```

**Optional:** Choose a different model. The default is `gpt-5.6-terra`.

```powershell
$env:OPENAI_MODEL="model-name-here"
```

OpenAI turns off old models from time to time. If the tutor says a model is "deprecated," set `OPENAI_MODEL` to a newer one. Check the [OpenAI deprecations page](https://platform.openai.com/docs/deprecations).

## Run the Website

```bash
python app.py
```

Open your browser and go to **http://127.0.0.1:5000**.

## Run the Terminal Version

```bash
python ai_tutor.py
```

These commands work in the terminal:

| Command | What it does |
| --- | --- |
| `mode <subject>` | Change the subject. Example: `mode science` |
| `quiz start` | Start a quiz |
| `quiz stop` | Stop the quiz and show your score |
| `exit` | Close the program |

Anything else you type is sent to the tutor as a question.

## Put It Online (Render)

1. Push your code to GitHub.
2. On [Render](https://render.com), make a new **Web Service** and connect your repo.
3. Use these settings:

| Setting | Value |
| --- | --- |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |

4. In **Environment**, add `OPENAI_API_KEY` with your key.
5. Deploy. Render gives you a link that ends in `onrender.com`.

## Project Files

| File or folder | What it does |
| --- | --- |
| `app.py` | The Flask website. It has the routes and talks to OpenAI. |
| `ai_tutor.py` | The terminal version of the tutor. |
| `templates/index.html` | The web page and its JavaScript. |
| `requirements.txt` | The list of Python packages. |
| `.gitignore` | Tells Git to skip `venv/`, `.env`, and other files that should stay private. |
| `static/` | Old files from an earlier project. The current page does not use them. |
| `topic_prompts/`, `templ` | Empty placeholder files. |
| `.devcontainer/`, `.vscode/` | Settings for coding tools. |

## How It Works

1. You pick a subject and type a question.
2. The page sends it to the `/ask` route.
3. Flask adds a **system prompt** for your subject. This tells the AI how to act, like "You are a mathematics tutor."
4. Flask sends the prompt and your question to the OpenAI model.
5. The AI's answer comes back. The page turns its Markdown into clean, safe HTML.

### Quiz Flow

1. You say how many questions you want. The app calls `/start_quiz`.
2. The AI makes one question as JSON. It has a `question`, a `correct_answer`, and an `explanation`.
3. You type an answer. The app calls `/check_answer`.
4. The app compares your answer to the correct one. It shows ✅ or ❌ and the explanation.
5. After the last question, you see your score as a percentage.

### Routes

| Route | Method | What it does |
| --- | --- | --- |
| `/` | GET | Shows the main page |
| `/ask` | POST | Sends a question to the tutor |
| `/start_quiz` | POST | Starts a quiz and returns the first question |
| `/check_answer` | POST | Checks an answer and returns the next question |

## Known Limits

This is a school-style project. Here are the things that are not finished yet:

- **The quiz score is shared by everyone.** The quiz data lives in global variables. Two people using the site at once will mix up each other's quizzes.
- **Answers must match exactly.** "4" is right, but "four" is marked wrong.
- **The website does not remember the chat.** Each question is sent on its own. The terminal version does remember.
- **Math symbols can look raw.** The AI sometimes writes math in LaTeX. The page does not draw it as nice math yet.
- **The AI can be wrong.** Always check important answers.
- **Quiz questions can fail.** Sometimes the AI does not return clean JSON.
- **Debug mode is on in `app.py`.** It only matters when you run `python app.py`. Turn it off before you host the app a different way.

## Security Notes

- Keep your API key in an environment variable. Do not commit it.
- If a key is ever committed to GitHub, delete it in your OpenAI account and make a new one. Removing it from the code is not enough, because it stays in the Git history.
- Set a monthly spending limit in your OpenAI account. Anyone with the link to a live demo can use your credit.

## Ideas for the Future

- [ ] Keep quiz scores per user with Flask sessions
- [ ] Accept answers that are close, like "four" and "4"
- [ ] Add chat memory to the website
- [ ] Move to the newer OpenAI Python package
- [ ] Add more subjects

## Credits

This was a team project. Thank you to:

- **Reeddhiman Pradhan**
- **Akoi Mariik**
- **Gavin Lee Hyugh**
