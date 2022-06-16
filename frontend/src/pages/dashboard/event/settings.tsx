// TODO: consolidate form code with create event form
import { Show, createSignal, createResource, runWithOwner } from "solid-js";
import { useRouteData } from "solid-app-router";

import date from "date-and-time";

import { customFormHandler } from "@/lib/directives";
import { API_URL, useToken } from "@/lib/api";
import { withOwner } from "@/lib/helpers";
import { useEvent } from "@/lib/event";

async function submitReq(data, { owner }) {
  const [token, _setToken, _eraseToken] = useToken(owner);
  const event: any = runWithOwner(owner, useEvent);
  const routeData: any = runWithOwner(owner, useRouteData);

  const fetchResp = await fetch(`${API_URL}/api/event/${event().id}/update`, {
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
    return fetchJSON;
  } else {
    return Promise.reject(fetchJSON);
  }
}

export default function Settings() {
  const event = useEvent();
  const [formData, setFormData] = createSignal(null);
  const [fetchData] = createResource(formData, withOwner(submitReq));

  const minDate = new Date();
  const maxDate = date.addYears(minDate, 1);

  function onFormSubmit(data) {
    setFormData({ id: event().id, ...data });
  }

  return (
    <Show when={event()}>
      <div class="box">
        <h4 class="title is-4">Settings</h4>
        <form use:customFormHandler={onFormSubmit}>
          <div class="field">
            <label class="label">Name</label>
            <input class="input" name="name" value={event().name} />
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
                value={event().date}
              />
            </div>
          </div>
          <div class="field">
            <div class="control">
              <button class="button is-primary" classList={{"is-loading": fetchData.loading}} type="submit">
                Save
              </button>
            </div>
          </div>
        </form>
      </div>
    </Show>
  );
}
