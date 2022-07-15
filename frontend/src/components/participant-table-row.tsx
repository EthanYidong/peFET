import {
  Show,
  createRenderEffect,
  createSignal,
  createResource,
  runWithOwner,
  createEffect,
} from "solid-js";
import { useRouteData } from "solid-app-router";
import { FaSolidEdit, FaSolidSave } from "solid-icons/fa";

import { withOwner } from "@/lib/helpers";
import { useEvent } from "@/lib/event";
import { API_URL, useToken } from "@/lib/api";

async function submitReq(data, { owner }) {
  const [token, _setToken, _eraseToken] = useToken(owner);
  const routeData: any = runWithOwner(owner, useRouteData);
  const event: any = runWithOwner(owner, useEvent);

  const fetchResp = await fetch(
    `${API_URL}/api/event/${event().id}/participants/${data.id}/update`,
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

export default function ParticipantTableRow(props) {
  const [formData, setFormData] = createSignal(null);
  const [fetchData] = createResource(formData, withOwner(submitReq));
  
  createEffect(() => props.onError(fetchData.error?.errors ?? []));
  
  let editForm;

  createRenderEffect((prev) => {
    if (prev && !props.editing) {
      const formData = new FormData(editForm);
      const data = {};
      for (const field of formData) {
        const [key, value] = field;
        data[key] = value;
      }
      data["id"] = props.participant.id;

      setFormData(data);
    }
    return props.editing;
  });

  return (
    <Show
      when={props.editing}
      fallback={
        <tr>
          <td>
            <input
              type="checkbox"
              onClick={props.onSelect}
              checked={props.selected}
            />
          </td>
          <td>
            <button
              class="button is-small is-text"
              classList={{ "is-loading": fetchData.loading }}
              onClick={props.onEdit}
            >
              <FaSolidEdit />
            </button>
          </td>
          <td>{props.participant.name}</td>
          <td>{props.participant.email}</td>
          <td>
            <Show when={props.participant.status === "Y"} fallback={"Not Submitted"}>
              Submitted (<a onClick={props.onOpen}>view</a>)
            </Show>
          </td>
        </tr>
      }
    >
      <tr>
        <td>
          <input
            type="checkbox"
            onClick={props.onSelect}
            checked={props.selected}
          />
        </td>
        <td>
          <form ref={editForm} id="editParticipantForm" />
          <button class="button is-small is-text" onClick={props.onSave}>
            <FaSolidSave />
          </button>
        </td>
        <td>
          <input
            class="input is-small"
            type="text"
            name="name"
            value={props.participant.name}
            form="editParticipantForm"
          />
        </td>
        <td>
          <input
            class="input is-small"
            type="text"
            name="email"
            value={props.participant.email}
            form="editParticipantForm"
          />
        </td>
        <td>
          <Show when={props.participant.status === "Y"} fallback={"Not Submitted"}>
            Submitted (<a onClick={props.onOpen}>view</a>)
          </Show>
        </td>
      </tr>
    </Show>
  );
}
