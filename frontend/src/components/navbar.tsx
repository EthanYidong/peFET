import { createSignal, Show } from "solid-js";
import { Link } from "solid-app-router";

import { useToken } from "@/lib/api";

export default function Navbar() {
  const [token, _setToken, _clearToken] = useToken();

  const [isActive, setIsActive] = createSignal(false);

  return (
    <nav class="navbar">
      <div class="container">
        <a role="button" class="navbar-burger" classList={{"is-active": isActive()}} onClick={() => setIsActive(!isActive())}>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
        <div class="navbar-menu" classList={{"is-active": isActive()}}>
          <div class="navbar-start">
            <Link class="navbar-item" href="/">Home</Link>
            <Show when={token()}>
              <Link class="navbar-item" href="/dashboard">
                Dashboard
              </Link>
            </Show>
          </div>

          <div class="navbar-end">
            <div class="navbar-item">
              <div class="buttons">
                <Show
                  when={token()}
                  fallback={() => (
                    <>
                      <Link class="button is-dark" href="/login">
                        Login
                      </Link>
                      <Link class="button is-primary" href="/signup">
                        Sign Up
                      </Link>
                    </>
                  )}
                >
                  <Link class="button" href="/logout">
                    Logout
                  </Link>
                </Show>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
