/* @refresh reload */
import { render } from "solid-js/web";
import { Router } from "solid-app-router";

import App from "./app";
import { StorageProvider } from "@/lib/storage";
import "./index.sass";
import "./mirage";

render(
  () => (
    <StorageProvider>
      <Router>
        <App />
      </Router>
    </StorageProvider>
  ),
  document.getElementById("root") as HTMLElement
);
