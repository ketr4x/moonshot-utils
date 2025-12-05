# Journal for Moonshot Utils
## Journal Entry #1 - 20.11.2025 - 0.5h
- I started researching the requests made by the Moonshot website
- After analyzing the shop network tab in devtools, I have found a shop endpoint: https://moonshot.hackclub.com/api/launchpad/shop/items
  ![](https://hc-cdn.hel1.your-objectstorage.com/s/v3/0a4d0320921997d550d256e8502ab8314bb10bfd_tmp_3Achat_3A2025-11-21_3Acmh5ztw4l004dp401tzedfn6i_3A817a36ef91a5c12f)
- The endpoint requires authentication via a cookie with entries like moonshot_session
- I have tested the responses with curl

## Journal Entry #2 - 21.11.2025 - 1.5h
- I have researched my possible options and frameworks, as well as decided the project structure.
- I have the project quite planned out. It will have a backend, frontend and a Slack bot to announce the price changes and quantity drops, as well as new item additions.
- For the server, I had to choose between FastAPI and Flask. Since I have previous experience with using Flask, I ultimately chose it.
- For the client, I will use Vite with React using TypeScript.
- The Slack bot will be run on the server.
- The app will be hosted on Heroku, most likely using the Basic plan with credits from GitHub Education.
- I have installed all the required software for React.
- Then, I have created the Flask server and React client and created the repository.
- Lastly, I published the repository to GitHub.