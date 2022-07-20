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
  on,
} from "solid-js";
import { createStore } from "solid-js/store";
import { useRouteData } from "solid-app-router";

import { FaSolidPlusCircle } from "solid-icons/fa";

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
import FilterDropdown from "@/components/filter-dropdown";
import SetTour from "@/components/set-tour";
import Errors from "@/components/errors";
import Success from "@/components/success";
import type { PefetEvent } from "@/lib/event";
import type { RouteData } from "@/lib/route-data";

async function submitReq(data, { owner }) {
  const [token, _setToken, _eraseToken] = useToken(owner);
  const routeData: RouteData = runWithOwner<RouteData>(owner, useRouteData);
  const event: PefetEvent = runWithOwner<PefetEvent>(owner, useEvent);

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
  const routeData: RouteData = useRouteData();
  const event = useEvent();

  const [formData, setFormData] = createSignal(null);
  const [fetchData] = createResource(formData, withOwner(submitReq));

  const [editing, setEditing] = createSignal(null);
  const isEditing = createSelector(editing);

  const [selected, setSelected] = createStore<any>({});

  const [filter, setFilter] = createSignal((p) => true);

  const [emailModal, setEmailModal] = createSignal(false);
  const [participantModal, setParticipantModal] = createSignal(null);
  const [sentEmails, setSentEmails] = createSignal(false);

  const [editErrors, setEditErrors] = createSignal([]);
  const [uploadErrors, setUploadErrors] = createSignal([]);

  const allErrors = createMemo(() => [...(fetchData.error?.errors ?? []), ...editErrors(), ...uploadErrors()]);

  let createForm;

  const owner = getOwner();

  const filteredParticipants = createMemo(
    () => routeData.event()?.participants.filter(filter())
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

  function onFormSubmit(data) {
    setFormData({ ...data });
  }

  createEffect(on(fetchData, () => {
    createForm.reset();
  }, {defer: true}))

  function nextSubmission() {
    const cur = participantModal();
    let check = cur + 1;
    while (check < routeData.event().participants.length) {
      if(routeData.event().participants[check].status === "Y") {
        return check;
      }
      check ++;
    }
    return cur;
  }

  function prevSubmission() {
    const cur = participantModal();
    let check = cur - 1;
    while (check >= 0) {
      if(routeData.event().participants[check].status === "Y") {
        return check;
      }
      check --;
    }
    return cur;
  }

  return (
    <>
      <SetTour steps={steps.dashboard} onComplete={() => completeTutorial(owner)}/>
      <Errors errors={allErrors()} />
      <Show when={sentEmails()}>
        <Success success={["Successfully sent emails"]}/>
      </Show>
      <Show when={participantModal() !== null}>
        <ParticipantModal
          onClose={() => setParticipantModal(null)}
          participant={() => routeData.event().participants[participantModal()]}
          onNext={() => setParticipantModal(nextSubmission())}
          onPrev={() => setParticipantModal(prevSubmission())}
        />
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
          <div class="level-item">
            <FilterDropdown setFilter={setFilter} />
          </div>
          <div class="level-item tour-upload-csv">
            <UploadDropdown onError={setUploadErrors} refetchEvent={routeData.refetchEvent}/>
          </div>
        </div>
        <div class="level-right" />
      </div>
      <form ref={createForm} id="createForm" use:customFormHandler={onFormSubmit} />
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
                <th />
                <th>Name</th>
                <th>Email</th>
                <th>Status</th>
              </tr>
              <tr class="tour-manual-create">
                <td />
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
                <td />
              </tr>
            </thead>
            <tbody>
              <For each={filteredParticipants()}>
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
                      () => setParticipantModal(index())
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
