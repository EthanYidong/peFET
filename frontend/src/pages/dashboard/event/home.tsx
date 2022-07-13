import {
  For,
  Show,
  createSignal,
  createResource,
  createSelector,
  createMemo,
  runWithOwner,
  createEffect,
  getOwner,
} from "solid-js";
import { createStore } from "solid-js/store";
import { useRouteData } from "solid-app-router";

import { FaSolidEdit, FaSolidPlusCircle } from "solid-icons/fa";

import { customFormHandler } from "@/lib/directives";
import { steps } from "@/lib/tour";
import { useEvent } from "@/lib/event";
import { withOwner } from "@/lib/helpers";
import { API_URL, useToken } from "@/lib/api";
import ParticipantTableRow from "@/components/participant-table-row";
import EmailDropdown from "@/components/email-dropdown";
import UploadDropdown from "@/components/upload-dropdown";
import EmailModal from "@/components/email-modal";
import ParticipantModal from "@/components/participant-modal";
import SetTour from "@/components/set-tour";
import Errors from "@/components/errors";
import Success from "@/components/success";

async function submitReq(data, { owner }) {
  const [token, _setToken, _eraseToken] = useToken(owner);
  const routeData: any = runWithOwner(owner, useRouteData);
  const event: any = runWithOwner(owner, useEvent);

  const fetchResp = await fetch(
    `${API_URL}/api/event/${event().id}/participants/create`,
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
    routeData.refetchEvents();
    routeData.refetchEvent();
    return fetchJSON;
  } else {
    return Promise.reject(fetchJSON);
  }
}

async function completeTutorial(owner) {
  const [token, _setToken, _eraseToken] = useToken(owner);

  const fetchResp = await fetch(
    `${API_URL}/api/account/complete_tutorial`,
    {
      method: "POST",
      headers: {
        Authorization: "Bearer " + token(),
        "Content-Type": "application/json",
      },
    }
  );

  const fetchJSON = await fetchResp.json();
  if (fetchResp.ok) {
    return fetchJSON;
  } else {
    return Promise.reject(fetchJSON);
  }
}

export default function Home() {
  const routeData: any = useRouteData();
  const event = useEvent();

  const [formData, setFormData] = createSignal(null);
  const [fetchData] = createResource(formData, withOwner(submitReq));

  const [editing, setEditing] = createSignal(null);
  const isEditing = createSelector(editing);

  const [selected, setSelected] = createStore({} as any);

  const [emailModal, setEmailModal] = createSignal(false);
  const [participantModal, setParticipantModal] = createSignal(null);
  const [sentEmails, setSentEmails] = createSignal(false);

  const [editErrors, setEditErrors] = createSignal([]);
  const [uploadErrors, setUploadErrors] = createSignal([]);

  const allErrors = createMemo(() => [...(fetchData.error?.errors ?? []), ...editErrors(), ...uploadErrors()]);

  const owner = getOwner();

  const filteredParticipants = createMemo(
    () => routeData.event()?.participants
  );

  const allSelected = createMemo(() => {
    if (filteredParticipants()) {
      for (const participant of filteredParticipants()) {
        if (!selected[participant.id]) {
          return false;
        }
      }
      return true;
    }
  });

  const selectedParticipants = createMemo(() => {
    const filteredList = [];
    if (routeData.event()) {
      for (const participant of routeData.event().participants) {
        if (selected[participant.id]) {
          filteredList.push(participant);
        }
      }
    }
    return filteredList;
  });

  function onAllCheckboxClick(e) {
    const checked = (e.target as HTMLInputElement).checked;
    setSelected(
      filteredParticipants().map((p) => p.id),
      checked
    );
  }

  function onFormSubmit(data, { form }) {
    form.reset();
    setFormData({ ...data });
  }

  return (
    <>
      <SetTour steps={steps.dashboard} onComplete={() => completeTutorial(owner)}/>
      <Errors errors={allErrors()}></Errors>
      <Show when={sentEmails()}>
        <Success success={["Successfully sent emails"]}/>
      </Show>
      <Show when={participantModal()}>
        <ParticipantModal onClose={() => setParticipantModal(null)} participant={participantModal}/>
      </Show>
      <Show when={emailModal()}>
        <EmailModal
          onClose={(v) => {setEmailModal(false); setSentEmails(v);}}
          selectedParticipants={selectedParticipants}
        />
      </Show>
      <h1 class="title">{event().name}</h1>
      <div class="level">
        <div class="level-left">
          <div class="level-item tour-send-emails">
            <EmailDropdown openEmailModal={() => {setEmailModal(true); setSentEmails(false);}} />
          </div>
          <div class="level-item tour-upload-csv">
            <UploadDropdown onError={setUploadErrors} refetchEvent={routeData.refetchEvent}/>
          </div>
        </div>
        <div class="level-right"></div>
      </div>
      <form id="createForm" use:customFormHandler={onFormSubmit} />
      <Show when={routeData.event()}>
        <div class="is-flex">
          <table class="table is-flex-grow-1">
            <thead>
              <tr>
                <th>
                  <input
                    type="checkbox"
                    class="tour-select"
                    onClick={onAllCheckboxClick}
                    checked={allSelected()}
                  />
                </th>
                <th></th>
                <th>Name</th>
                <th>Email</th>
                <th>Status</th>
              </tr>
              <tr class="tour-manual-create">
                <td></td>
                <td>
                  <button
                    class="button is-small is-text"
                    type="submit"
                    form="createForm"
                  >
                    <FaSolidPlusCircle />
                  </button>
                </td>
                <td>
                  <input
                    class="input is-small"
                    type="text"
                    name="name"
                    form="createForm"
                  />
                </td>
                <td>
                  <input
                    class="input is-small"
                    type="text"
                    name="email"
                    form="createForm"
                  />
                </td>
                <td></td>
              </tr>
            </thead>
            <tbody>
              <For each={routeData.event().participants}>
                {(participant: any, index) => (
                  <ParticipantTableRow
                    participant={participant}
                    editing={isEditing(participant.id)}
                    selected={selected[participant.id]}
                    onEdit={() => setEditing(participant.id)}
                    onSave={() => setEditing(null)}
                    onSelect={(e) =>
                      setSelected(
                        participant.id,
                        (e.target as HTMLInputElement).checked
                      )
                    }
                    onOpen={
                      () => setParticipantModal(participant)
                    }
                    onError={setEditErrors}
                  />
                )}
              </For>
            </tbody>
          </table>
        </div>
      </Show>
    </>
  );
}
