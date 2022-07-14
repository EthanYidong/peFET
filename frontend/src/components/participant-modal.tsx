import {
  Show,
  For,
  createSignal,
  createResource,
  runWithOwner,
  createEffect,
  on,
} from "solid-js";
import { useRouteData } from "solid-app-router";
import { FaSolidTimes, FaSolidAngleLeft, FaSolidAngleRight, } from "solid-icons/fa";

import { API_URL, useToken } from "@/lib/api";
import { withOwner, onButton } from "@/lib/helpers";
import { useEvent } from "@/lib/event";
import { clickOutside } from "@/lib/directives";

async function fetchReq(data, { owner }) {
  const routeData: any = runWithOwner(owner, () => useRouteData());
  const [token, _setToken, _eraseToken] = useToken(owner);
  const event: any = runWithOwner(owner, useEvent);

  const fetchResp = await fetch(
    `${API_URL}/api/event/${event().id}/participants/${data.id}/get_submission`,
    {
      method: "GET",
      headers: {
        Authorization: "Bearer " + token(),
        "Content-Type": "application/json",
      },
    }
  );

  const fetchData = await fetchResp.json();

  if (fetchResp.ok) {
    return fetchData;
  } else {
    return Promise.reject(fetchData);
  }
}

export default function ParticipantModal(props) {
  const routeData: any = useRouteData();

  const [fetchData] = createResource(() => props.participant(), withOwner(fetchReq));

  onButton("Escape", props.onClose);

  let subImg;

  createEffect(() => {
    if(fetchData()) {
      subImg.src = `data:image/png;base64,${fetchData().original_image}`;
    }
  });

  return (
    <div class="modal is-active">
      <div class="modal-background"></div>
      <div class="modal-card" use:clickOutside={props.onClose}>
        <header class="modal-card-head">
          <p class="modal-card-title">
            {props.participant().name}
          </p>
          <a onClick={props.onClose}>
            <FaSolidTimes />
          </a>
        </header>
        <section class="modal-card-body">
          <img ref={subImg}></img>
        </section>
        <footer class="modal-card-foot">
          <div class="level fillwidth">
            <div class="level-left">
              <div class="level-item"><button class="button" onClick={props.onClose}>Close</button></div>
              
            </div>
            <div class="level-right">
              <div class="level-item"><button class="button" onClick={props.onPrev}><FaSolidAngleLeft/></button></div> 
              <div class="level-item"><button class="button" onClick={props.onNext}><FaSolidAngleRight/></button></div> 
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}
