import {
  For,
  createSignal,
  createResource,
  runWithOwner,
  createEffect,
  on,
  untrack,
} from "solid-js";
import { useRouteData, useLocation } from "solid-app-router";
import { FaSolidTimes, FaSolidUpload } from "solid-icons/fa";

import { API_URL, useToken } from "@/lib/api";
import { withOwner, onButton } from "@/lib/helpers";
import { useEvent } from "@/lib/event";
import { clickOutside, customFormHandlerRaw } from "@/lib/directives";

import Errors from "@/components/errors";

async function submitReq(data, { owner }) {
  const location = runWithOwner(owner, useLocation);

  const fetchResp = await fetch(`${API_URL}/api/portal/upload_image`, 
    {
      method: "POST",
      headers: {
        Authorization: "Bearer " + location.query.token,
      },
      body: data,
    }
  );

  const fetchJSON = await fetchResp.json();

  if (fetchResp.ok) {
    return fetchJSON;
  } else {
    return Promise.reject(fetchJSON);
  }
}


export default function Picture(props) {
  const [formData, setFormData] = createSignal(null);
  const [fetchData] = createResource(formData, withOwner(submitReq));

  createEffect(on(fetchData, () => props.onClose(true), {defer: true}));
  onButton("Escape", () => props.onClose(false));

  function onFormSubmit(data) {
    setFormData(data);
  }

  return (
    <form use:customFormHandlerRaw={onFormSubmit}>
      <div class="modal is-active">
        <div class="modal-background"></div>
        <div class="modal-card" use:clickOutside={() => props.onClose(false)}>
          <header class="modal-card-head">
            <p class="modal-card-title">Upload Image</p>
            <a onClick={() => props.onClose(false)}>
              <FaSolidTimes />
            </a>
          </header>
          <section class="modal-card-body">
          <Errors errors={fetchData.error?.errors}></Errors>
            <div class="box">
              <h2 class="subtitle">Choose / Take Picture</h2>
              <div class="file">
                <label class="file-label">
                  <input class="file-input" type="file" accept="image/*" name="image"/>
                  <span class="file-cta">
                    <span class="file-icon">
                      <FaSolidUpload/>
                    </span>
                    <span class="file-label">
                      Choose a file…
                    </span>
                  </span>
                </label>
              </div>
            </div>
          </section>
          <footer class="modal-card-foot">
            <button class="button" classList={{ "is-loading": fetchData.loading }} disabled={fetchData.loading}>Upload</button>
          </footer>
        </div>
      </div>
    </form>
  );
}
