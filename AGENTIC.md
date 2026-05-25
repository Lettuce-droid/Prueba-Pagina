# Agentic Coding Process

## 1. Tools Used

- **Claude (claude.ai):** Used as the primary AI assistant throughout the entire
  project. Guided me through project structure, code generation, debugging, and
  explanations. Every file in this project was built through a conversation with
  Claude where I asked for explanations before moving forward.

## 2. My Approach

My programming background before this project was limited — I had worked with
HTML for visual/aesthetic purposes and had some knowledge of databases in theory,
but had never implemented a backend API or connected a database to a web application.

My approach was to learn and build at the same time:

- I asked Claude to explain every concept before implementing it
- For each file, I requested line-by-line explanations instead of just copying code
- I deliberately tried to apply changes myself by looking at the differences in
  the code rather than copy-pasting directly — this caused some bugs but helped
  me understand what each line actually does
- When something was unclear, I asked follow-up questions until it made sense

I did not use Claude as a code generator. I used it as a teacher that also writes
code, and I made sure I understood each piece before moving on.

## 3. Key Prompts

### Prompt 1: Understanding the database connection
**What I asked:** I asked Claude to explain line by line how database.py connects
the application to SQLite, because after the first explanation I was still confused.

**What it generated:** A detailed analogy comparing the database to a restaurant
storage room, the engine to the door, and the session to a waiter that opens and
closes for each request.

**What I did:** Used the analogy to understand the concept, then re-read the code
until it clicked. This was one of the concepts I struggled with the most.

### Prompt 2: Changing the domain from books to image posts
**What I asked:** I asked Claude to migrate the entire application from a book
catalog to an image sharing platform similar to Imgur, where users can upload
images with a title and description.

**What it generated:** Updated models.py, schemas.py, a new routers/posts.py,
and an updated main.py with static file serving for uploaded images.

**What I did:** Used it with modifications. I changed the app name myself to
"Imagenes Chistosas" and tried to apply some changes manually by reading the
diffs rather than copy-pasting, which caused some bugs we had to debug together.

### Prompt 3: Fixing the mobile connection issue
**What I asked:** I reported that the frontend was hardcoding the IP address
192.168.1.7, which would not work for other users since their IP would be different.

**What it generated:** The fix using window.location.origin instead of a hardcoded
IP, so the frontend always connects to whatever server it was loaded from.

**What I did:** I identified the problem myself as a user/developer — I noticed
that hardcoding my local IP meant nobody else could use the app. Claude provided
the fix, which I understood and applied.

## 4. Critical Evaluation

### The frontend (index.html)

**What Claude got right:**
- The overall structure and dark theme styling worked well on first try
- The modal system for login, register, and post creation was clean
- The responsive CSS for mobile worked correctly

**What I had to fix or improve:**
- The API URL was hardcoded to localhost and then to my local IP — I caught the
  IP issue myself and we fixed it with window.location.origin
- The file input was nested inside a label tag which caused getElementById to
  fail silently — this took several debugging steps to find
- The description overflow required multiple iterations to work correctly because
  the word-break behavior was different for text without spaces

**Security issues identified:**
- SECRET_KEY is hardcoded in auth.py — this is a known limitation and should be
  moved to an environment variable in production
- No file type validation on uploads beyond the accept attribute in the HTML,
  which can be bypassed

**How I verified it works:**
- Manually tested registration, login, post creation, deletion, and the ownership
  restriction from two different accounts
- Tested on both desktop and mobile (connected via local network)
- Ran the automated test suite which covers all core behaviors

### The authentication system (auth.py)

**What Claude got right:**
- Correct use of bcrypt for password hashing
- JWT token creation and validation pattern is clean and reusable
- The get_current_user dependency works correctly across all protected endpoints

**What went wrong:**
- The initial bcrypt version had a bug with password length validation that threw
  a 500 error even for short passwords — we fixed it by downgrading to bcrypt==4.0.1

### Security improvements I implemented after initial generation

**Environment variables:**
After the initial project was working, I asked Claude to move the SECRET_KEY
out of the source code and into a .env file using python-dotenv. I understood
why this matters — if the key is hardcoded and pushed to GitHub, anyone can
read it and forge JWT tokens to impersonate any user.

**File validation:**
I asked Claude to add validation so only image files under 5MB can be uploaded.
I tested this myself by temporarily lowering the limit to 10KB and verifying
that the API correctly rejected larger files with a 400 error.

**Logging:**
I added logging to record when users attempt to upload invalid files, and when
posts are created successfully. This creates an app.log file that helps detect
suspicious behavior without exposing sensitive information.

## 5. What I Learned

- **How a backend API works:** Before this project I did not know what an API was
  beyond the word. Now I understand that it is a server that receives HTTP requests
  (GET, POST, PUT, DELETE) and responds with data, and that the frontend and backend
  are two separate things that communicate through those requests.

- **How databases connect to applications:** I understood databases in theory but
  not in practice. I learned how SQLAlchemy acts as a bridge between Python and
  SQLite, and how models define the structure of the data while schemas validate
  what comes in and goes out.

- **How authentication works:** I learned that passwords should never be stored
  in plain text, that bcrypt hashes them in a one-way process, and that JWT tokens
  are signed strings that carry the user's identity without needing to query the
  database on every request.

- **How to debug:** I learned to read error messages in the terminal, use the
  browser's Network and Console tabs to trace what is happening, and narrow down
  problems by testing small pieces instead of guessing.

- **Separation of concerns:** I learned why it matters to keep database logic,
  business rules, and routing in separate files — it makes the code easier to
  read, modify, and test.

- **Git as a habit:** I learned to commit frequently with meaningful messages
  instead of doing everything in one commit, and why that matters for tracking
  changes over time.