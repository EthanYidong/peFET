import {
  For,
  createSignal,
  createResource,
  createEffect,
  on,
  untrack,
} from "solid-js";
import { FaSolidTimes } from "solid-icons/fa";

import { API_URL, useToken } from "@/lib/api";
import { withOwner, onButton } from "@/lib/helpers";
import { useEvent } from "@/lib/event";
import { clickOutside, customFormHandler } from "@/lib/directives";

async function submitReq(data, { owner }) {
  const event = useEvent();

  const [token, _setToken, _eraseToken] = useToken(owner);
  const fetchResp = await fetch(`${API_URL}/api/event/${event().id}/send_emails`, 
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
  const event = useEvent();

  const [formData, setFormData] = createSignal(null);
  const [fetchData] = createResource(formData, withOwner(submitReq));

  createEffect(on(fetchData, props.onClose, {defer: true}));
  onButton("Escape", props.onClose);

  function onFormSubmit(data) {
    setFormData({
      participants: props
        .selectedParticipants()
        .map((participant) => participant.id),
      ...data
    });
  }

  return (
    <form use:customFormHandler={onFormSubmit}>
      <div class="modal is-active">
        <div class="modal-background" />
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
                  <label class="label">
                    Subject
                  </label>
                  <input class="input" type="text" name="subject" value={`FET test required for ${untrack(() => event().name)}`}/>
                </div>
              </div>
              <div class="field">
                <div class="control">
                  <label class="label">
                    Body
                  </label>
                  <textarea class="textarea" name="body" rows="5"/>
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
