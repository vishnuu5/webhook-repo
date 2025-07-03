# GitHub Actions Webhook Receiver

This project is a minimal full-stack application that receives GitHub webhook events (Push, Pull Request, Merge), stores them in MongoDB, and displays them in a clean UI that polls for updates every 15 seconds.

## Features
- Receives GitHub webhook events (Push, Pull Request, Merge)
- Stores event data in MongoDB
- Minimal HTML5 frontend displays latest actions
- Polls backend every 15 seconds for updates

## Tech Stack
- Backend: Python, Flask
- Database: MongoDB
- Frontend: HTML5, CSS, JavaScript

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/vishnuu5/webhook-repo.git
cd webhook-repo
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure MongoDB
- Create a `.env` file in the project root with your MongoDB URI:
  ```
  MONGO_URI=your_mongodb_connection_string
  ```

### 4. Start the Flask server
```bash
python app.py
```

### 5. Expose your local server to the internet (for GitHub webhooks)
- [Download ngrok](https://ngrok.com/download)
- In a new terminal, run:
  ```bash
  ngrok http 5000
  ```
- Copy the HTTPS URL provided by ngrok (e.g., `https://xxxx.ngrok.io`)

### 6. Configure GitHub Webhook
- Go to your GitHub repo (action-repo) > Settings > Webhooks > Add webhook
- **Payload URL:** `https://xxxx.ngrok.io/webhook`
- **Content type:** `application/json`
- **Events:** Select "Let me select individual events" and check:
  - Pushes
  - Pull requests
- Save the webhook

## Testing the Application

### 1. Push Event
- Make a change in your action-repo and push:
  ```bash
  git add .
  git commit -m "Test push event"
  git push
  ```
- The UI will show: `<author> pushed to <branch> on <timestamp>`

### 2. Pull Request Event
- Create a new branch and push:
  ```bash
  git checkout -b test-pr
  git add .
  git commit -m "Test PR event"
  git push --set-upstream origin test-pr
  ```
- Open a Pull Request from `test-pr` to `master` on GitHub.
- The UI will show: `<author> submitted a pull request from <from_branch> to <to_branch> on <timestamp>`

### 3. Merge Event
- Merge the Pull Request on GitHub.
- The UI will show: `<author> merged branch <from_branch> to <to_branch> on <timestamp>`

- On GitHub:
- Go to your open pull request for test-pr.
- Click “Merge pull request” and confirm.
-  In your browser:
- Go to your UI (ngrok URL).
- Wait up to 15 seconds.
- You should see a message like:
- yourusername merged branch test-pr to main on ...

## Notes
- The UI auto-refreshes every 15 seconds.
- Do not visit `/webhook` in your browser; it is for GitHub POST requests only.
- Visit the root URL (e.g., `http://localhost:5000/` or your ngrok URL) to see the UI.

## License
MIT 
