import { useEffect } from "react";
import * as firebaseui from "firebaseui";
import "firebaseui/dist/firebaseui.css";
import { GoogleAuthProvider } from "firebase/auth";
import { auth } from "./firebaseInit";

const ui = new firebaseui.auth.AuthUI(auth);

const SsoWidget = () => {
  useEffect(() => {
    ui.start("#firebaseui-auth-container", {
      signInFlow: "popup",
      signInOptions: [
        {
          provider: GoogleAuthProvider.PROVIDER_ID,
          scopes: ["https://www.googleapis.com/auth/drive"],
        },
      ],
    });
  }, []);

  return <div id="firebaseui-auth-container" />;
};

export default SsoWidget;
