import {
  For,
  Show,
  createSignal,
  createResource,
  createSelector,
  createMemo,
  runWithOwner,
} from "solid-js";
import { createStore } from "solid-js/store";
import { useRouteData } from "solid-app-router";

import { FaSolidEdit, FaSolidPlusCircle } from "solid-icons/fa";

import { customFormHandler } from "@/lib/directives";
import { useEvent } from "@/lib/event";
import { withOwner } from "@/lib/helpers";
import { API_URL, useToken } from "@/lib/api";
import ParticipantTableRow from "@/components/participant-table-row";

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

export default function Home() {
  const routeData: any = useRouteData();
  const event = useEvent();

  const [formData, setFormData] = createSignal(null);
  const [fetchData] = createResource(formData, withOwner(submitReq));

  const [editing, setEditing] = createSignal(null);
  const isEditing = createSelector(editing);

  const [selected, setSelected] = createStore({} as any);

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
      <h1 class="title">{event().name}</h1>
      <form id="createForm" use:customFormHandler={onFormSubmit} />
      <Show when={routeData.event()}>
        <div class="is-flex">
          <table class="table is-flex-grow-1">
            <thead>
              <tr>
                <th>
                  <input
                    type="checkbox"
                    onClick={onAllCheckboxClick}
                    checked={allSelected()}
                  />
                </th>
                <th></th>
                <th>Name</th>
                <th>Email</th>
                <th>Status</th>
              </tr>
              <tr>
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
                {(participant: any) => (
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
