import { createEffect, createResource, on, onMount, onCleanup } from "solid-js";

import { useToken, API_URL } from "@/lib/api";
import { withOwner } from "@/lib/helpers";
import { useShepherd } from "@/lib/shepherd";

async function fetchReq(_data, {owner}) {
  const [token, _setToken, _eraseToken] = useToken(owner);

  const fetchResp = await fetch(
    `${API_URL}/api/account/me`,
    {
      method: "GET",
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

export default function SetTour(props) {
  const [fetchData] = createResource(withOwner(fetchReq));
  const [tour, setSteps, setOnComplete, clear] = useShepherd();
  
  createEffect(() => {
    if(fetchData() && !fetchData().tutorial_complete) {
      setSteps(props.steps);
    }
  });

  createEffect(() => {
    setOnComplete(() => props.onComplete);
  });

  onCleanup(() => {
    clear();
  });
  
  return <></>;
}
