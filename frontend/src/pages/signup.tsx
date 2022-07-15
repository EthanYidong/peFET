import { createSignal, createResource, createEffect } from "solid-js";
import { useNavigate } from "solid-app-router";

import { customFormHandler } from "@/lib/directives";
import { API_URL, useToken } from "@/lib/api";
import Navbar from "@/components/navbar";
import Errors from "@/components/errors";

async function submitReq(data) {
  // TODO: validate password
  const fetchResp = await fetch(API_URL + "/api/account/signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const fetchJSON = await fetchResp.json();

  if (fetchResp.ok) {
    return fetchJSON;
  } else {
    return Promise.reject(fetchJSON);
  }
}

export default function Signup() {
  const [formData, setFormData] = createSignal(null);
  const [fetchData] = createResource(formData, submitReq);
  const [token, setToken, _clearToken] = useToken();
  const navigate = useNavigate();

  const [localErrors, setLocalErrors] = createSignal([]);

  function onFormSubmit(data) {
    if (data.password !== data.repeatPassword) {
      setLocalErrors(["Passwords do not match!"]);
      return;
    }
    setLocalErrors([]);
    setFormData(data);
  }

  createEffect(() => {
    if (fetchData()) {
      setToken(fetchData().token);
    }
  });

  createEffect(() => {
    if (token() && token() !== "null") {
      navigate("/dashboard");
    }
  });

  return (
    <>
      <Navbar />
      <div class="columns is-vcentered is-centered fullheight-with-navbar">
        <div class="column is-6 box">
          <div class="m-4">
            <h1 class="title">Sign Up</h1>
            <Errors
              errors={[...(fetchData.error?.errors ?? []), ...localErrors()]}
            />
            <form use:customFormHandler={onFormSubmit}>
              <div class="field">
                <label class="label">Email</label>
                <div class="control">
                  <input class="input" type="text" name="email"/>
                </div>
              </div>
              <div class="field">
                <label class="label">Password</label>
                <div class="control">
                  <input class="input" type="password" name="password"/>
                </div>
              </div>
              <div class="field">
                <label class="label">Repeat Password</label>
                <div class="control">
                  <input
                    class="input"
                    type="password"
                    name="repeatPassword"
                  />
                </div>
              </div>
              <div class="field">
                <div class="control">
                  <button class="button is-primary">Sign Up</button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </>
  );
}
