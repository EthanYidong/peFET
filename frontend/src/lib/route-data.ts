import { createEffect, createResource } from "solid-js";
import { API_URL, useToken } from "@/lib/api";
import { withOwner } from "@/lib/helpers";

export interface RouteData {
  events: any,
  mutateEvents: (any) => void,
  refetchEvents: () => void,
  event: any,
  mutateEvent: (any) => void,
  refetchEvent: () => void,
}

async function fetchEventsData(_, { owner }) {
  const [token, _setToken, _clearToken] = useToken(owner);
  const fetchResp = await fetch(`${API_URL}/api/event/all`, {
    method: "GET",
    headers: {
      Authorization: "Bearer " + token(),
    },
  });

  const fetchJSON = await fetchResp.json();

  if (fetchResp.ok) {
    return fetchJSON;
  } else {
    return Promise.reject(fetchJSON);
  }
}

export function EventsData({ _params, _location, navigate, data }) {
  const [token, _setToken, clearToken] = useToken();
  if (token()) {
    const [fetchData, { mutate, refetch }] = createResource(
      withOwner(fetchEventsData)
    );
    createEffect(() => {
      if (fetchData.error) {
        clearToken();
        navigate("/login");
      }
    });
    return {
      events: fetchData,
      mutateEvents: mutate,
      refetchEvents: refetch,
      ...data,
    };
  } else {
    navigate("/login");
  }
}

async function fetchEventData(id, { owner }) {
  const [token, _setToken, _clearToken] = useToken(owner);
  const fetchResp = await fetch(`${API_URL}/api/event/${id}/participants`, {
    method: "GET",
    headers: {
      Authorization: "Bearer " + token(),
    },
  });

  const fetchJSON = await fetchResp.json();

  if (fetchResp.ok) {
    return fetchJSON;
  } else {
    return Promise.reject(fetchJSON);
  }
}

export function EventData({ params, _location, navigate, data }) {
  const [token, _setToken, _clearToken] = useToken();
  if (token()) {
    const [fetchData, { mutate, refetch }] = createResource(
      () => params.id,
      withOwner(fetchEventData)
    );
    createEffect(() => {
      if (fetchData.error) {
        navigate("/dashboard");
      }
    });
    return {
      event: fetchData,
      mutateEvent: mutate,
      refetchEvent: refetch,
      ...data,
    };
  } else {
    navigate("/dashboard");
  }
}
