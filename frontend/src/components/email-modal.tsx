import {
  For,
  createSignal,
  createResource,
  runWithOwner,
  createEffect,
  on,
} from "solid-js";
import { useRouteData } from "solid-app-router";
import { FaSolidTimes } from "solid-icons/fa";

import { API_URL, useToken } from "@/lib/api";
import { withOwner } from "@/lib/helpers";
import { clickOutside, customFormHandler } from "@/lib/directives";

async function emailReq(data, { owner }) {
  const routeData: any = runWithOwner(owner, () => useRouteData());
  const [token, _setToken, _eraseToken] = useToken(owner);
  const fetchResp = await fetch(
    `${API_URL}/session/${
      routeData.session().session.slug
    }/functions/send_emails`,
    {
      method: "POST",
      headers: {
        Authorization: "Bearer " + token(),
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }
  );

  const fetchJSON = await fetchResp.json();

  if (fetchResp.ok) {
    return fetchJSON;
  } else {
    return Promise.reject(fetchJSON);
  }
}

export default function EmailModal(props) {
  const routeData: any = useRouteData();

  const [formData, setFormData] = createSignal(null);
  const [emailData] = createResource(formData, withOwner(emailReq));

  function onEmailFormSubmit(data) {
    setFormData({
      participants: props
        .selectedParticipants()
        .map((participant) => participant["_id"]),
      dry_run: data.dry_run === "on",
    });
  }

  return (
    <form use:customFormHandler={onEmailFormSubmit}>
      <div class="modal is-active">
        <div class="modal-background"></div>
        <div class="modal-card" use:clickOutside={props.onClose}>
          <header class="modal-card-head">
            <p class="modal-card-title">Send Emails</p>
            <a onClick={props.onClose}>
              <FaSolidTimes />
            </a>
          </header>
          <section class="modal-card-body">
            <div class="box">
              <h2 class="subtitle">Send Emails To</h2>
              <ul>
                <For each={props.selectedParticipants()}>
                  {(participant: any) => <li>{participant.email}</li>}
                </For>
              </ul>
            </div>
            <div class="box">
              <h2 class="subtitle">Options</h2>
              <div class="field">
                <div class="control">
                  <label class="checkbox">
                    <input type="checkbox" name="dry_run" checked />
                    Dry Run
                  </label>
                </div>
              </div>
            </div>
          </section>
          <footer class="modal-card-foot">
            <button class="button">Send Emails</button>
          </footer>
        </div>
      </div>
    </form>
  );
}
