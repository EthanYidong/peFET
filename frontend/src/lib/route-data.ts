import { createEffect, createResource } from "solid-js";
import { API_URL, useToken } from "@/lib/api";
import { withOwner } from "@/lib/helpers";

async function fetchEventsData(_, {owner}) {
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

export function EventsData({ params, location, navigate, data }) {
  const [token, _setToken, clearToken] = useToken();
  if (token()) {
    const [fetchData, { refetch }] = createResource(withOwner(fetchEventsData));
    createEffect(() => {
      if (fetchData.error) {
        clearToken();
        navigate("/login");
      }
    });
    return { events: fetchData, refetchEvents: refetch, ...data };
  } else {
    navigate("/login");
  }
}
