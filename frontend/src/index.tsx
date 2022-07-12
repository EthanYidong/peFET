/* @refresh reload */
import { render } from "solid-js/web";
import { Router } from "solid-app-router";

import App from "./app";
import { StorageProvider } from "@/lib/storage";
import { ShepherdProvider } from "@/lib/shepherd";
import { tourOptions, steps } from "@/lib/tour";
import "./index.sass";
//import "./mirage";

render(
  () => (
    <StorageProvider>
      <Router>
        <ShepherdProvider tourOptions={tourOptions}>
          <App />
        </ShepherdProvider>
      </Router>
    </StorageProvider>
  ),
  document.getElementById("root") as HTMLElement
);
