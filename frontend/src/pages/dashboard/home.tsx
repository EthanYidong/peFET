import { createSignal, createResource, runWithOwner } from "solid-js";
import { useRouteData, useNavigate } from "solid-app-router";

import date from "date-and-time";

import { customFormHandler } from "@/lib/directives";
import { API_URL, useToken } from "@/lib/api";
import { withOwner } from "@/lib/helpers";
import Errors from "@/components/errors";

async function submitReq(data, { owner }) {
  const [token, _setToken, _eraseToken] = useToken(owner);
  const routeData: any = runWithOwner(owner, useRouteData);
  const navigate = runWithOwner(owner, useNavigate);

  const fetchResp = await fetch(`${API_URL}/api/event/create`, {
    method: "POST",
    headers: {
      Authorization: "Bearer " + token(),
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const fetchJSON = await fetchResp.json();

  if (fetchResp.ok) {
    routeData.refetchEvents();
    navigate(`/dashboard/event/${fetchJSON.id}`);
    return fetchJSON;
  } else {
    return Promise.reject(fetchJSON);
  }
}

export default function Home() {
  const [formData, setFormData] = createSignal();
  const [fetchData] = createResource(formData, withOwner(submitReq));

  const minDate = new Date();
  const maxDate = date.addYears(minDate, 1);

  function onFormSubmit(data) {
    setFormData(data);
  }

  return (
    <>
      <Errors errors={fetchData.error?.errors}></Errors>
      <div class="box">
        <h4 class="title is-4">Create a New Event</h4>
        <form use:customFormHandler={onFormSubmit}>
          <div class="field">
            <label class="label">Event Name</label>
            <div class="control">
              <input class="input" type="text" name="name" />
            </div>
          </div>
          <div class="field">
            <label class="label">Event Date</label>
            <div class="control">
              <input
                class="input"
                type="date"
                name="date"
                min={date.format(minDate, "YYYY-MM-DD")}
                max={date.format(maxDate, "YYYY-MM-DD")}
              />
            </div>
          </div>
          <div class="field">
            <div class="control">
              <button
                class="button is-primary"
                classList={{ "is-loading": fetchData.loading }}
                type="submit"
              >
                Create
              </button>
            </div>
          </div>
        </form>
      </div>

      <div class="box">
        <h4 class="title is-4">Instructions</h4>
        <p>
          For CSV upload, there should be only two columns with no headers.
          The leftmost column should have the names, and the other the emails of your participants.
        </p>
      </div>
    </>
  );
}
