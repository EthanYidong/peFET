import {
  createSignal,
  createResource,
  runWithOwner,
  createEffect,
  onMount,
} from "solid-js";
import { useLocation } from "solid-app-router";

import { FaSolidTimes } from "solid-icons/fa";

import { API_URL } from "@/lib/api";
import { withOwner, onButton } from "@/lib/helpers";

async function dataReq(_, { owner }) {
  const location = runWithOwner(owner, useLocation);

  const fetchResp = await fetch(`${API_URL}/api/portal/qr_code`, 
    {
      method: "GET",
      headers: {
        Authorization: "Bearer " + location.query.token,
      },
    }
  );

  const fetchData = await fetchResp.blob();

  if (fetchResp.ok) {
    return fetchData;
  } else {
    return Promise.reject(fetchData);
  }
}

export default function Qr(props) {
  const [imgData] = createResource(withOwner(dataReq));

  onButton("Escape", props.onClose);

  let qrImg;

  createEffect(() => {
    if(imgData()) {
      const imgURL = URL.createObjectURL(imgData());
      qrImg.src = imgURL;
    }
  });

  return (
    <>
      <div class="fullscreen-fixed has-background-warning">
        <div class="p-2" style={{"position": "fixed", "right": "0", "top": "0"}}>
          <a onClick={props.onClose} >
            <FaSolidTimes />
          </a>
        </div>
        <img ref={qrImg} style={{"max-height": "100vh", "max-width": "100vw", "cursor": "none"}}/>
      </div>
    </>
  );
}
