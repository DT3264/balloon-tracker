# Description
This client fetches data from the balloon-tracker-server and displays it.
Allows to see the status of the problems solved by each team and mark a problem from state 1 to state 2
- 1 -> Problem solved but no balloon given
- 2 -> Problem solved and balloon given

# Usage
This app requires vite to run, after that you run
```
# Install dependencies
npm install
# Run the app
npm run dev
```

To convert it to plain javascript for updating the index.html use
```
npx babel src --out-dir dist
```
And only replace the
```
function App(){
  // Code to replace
}
```

# Note
In the [getUrl function](https://github.com/DT3264/balloon-tracker/blob/main/balloon-tracker-client/src/main.jsx#L13) be sure to change the base address depending whether you're testing the client or serving the file from the server
