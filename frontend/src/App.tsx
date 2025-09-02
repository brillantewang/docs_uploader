import { useState, useEffect } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";

import { onAuthStateChanged, signOut } from "firebase/auth";
import SsoWidget from "./SsoWidget";
import { auth } from "./firebaseInit";

function App() {
  const [count, setCount] = useState(0);
  const [signedIn, setSignedIn] = useState(false);

  useEffect(() => {
    const unregisterAuthObserver = onAuthStateChanged(auth, (user) => {
      console.log(user, "user");
      setSignedIn(!!user);
    });
    return () => unregisterAuthObserver();
  }, []);

  if (!signedIn) {
    return <SsoWidget />;
  }

  return (
    <>
      <div>
        <div>
          <button onClick={() => signOut(auth)}>Sign out</button>
        </div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  );
}

export default App;
