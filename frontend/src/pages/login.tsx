import { createSignal, createResource, createEffect } from "solid-js";
import { useNavigate } from "solid-app-router";

import { customFormHandler } from "@/lib/directives";
import { API_URL, useToken } from "@/lib/api";
import Errors from "@/components/errors";
import Navbar from "@/components/navbar";

async function submitReq(data) {
  const fetchResp = await fetch(API_URL + "/api/account/login", {
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

export default function Login() {
  const [formData, setFormData] = createSignal(null);
  const [fetchData] = createResource(formData, submitReq);
  const [token, setToken, _clearToken] = useToken();
  const navigate = useNavigate();

  function onFormSubmit(data) {
    setFormData(data);
  }

  createEffect(() => {
    if (fetchData()) {
      setToken(fetchData().token);
    }
  });

  createEffect(() => {
    if (token()) {
      navigate("/dashboard");
    }
  });

  return (
    <>
      <Navbar />
      <div class="columns is-vcentered is-centered fullheight-with-navbar">
        <div class="column is-6 box">
          <div class="m-4">
            <h1 class="title">Login</h1>
            <Errors errors={fetchData.error?.errors} />
            <form use:customFormHandler={onFormSubmit}>
              <div class="field">
                <label class="label">Email</label>
                <div class="control">
                  <input class="input" type="text" name="email" />
                </div>
              </div>
              <div class="field">
                <label class="label">Password</label>
                <div class="control">
                  <input class="input" type="password" name="password" />
                </div>
              </div>
              <div class="field">
                <div class="control">
                  <button class="button is-primary">Login</button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </>
  );
}
