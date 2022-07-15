import { createSignal, createResource, createEffect } from "solid-js";

import { useToken } from "@/lib/api";
import { withOwner } from "@/lib/helpers";

async function submitReq(data, url, onFinished, { owner }) {
  const [token, _setToken, _clearToken] = useToken(owner);
  const fetchResp = await fetch(
    url(),
    {
      method: "POST",
      headers: {
        Authorization: "Bearer " + token(),
      },
      body: data,
    }
  );

  const fetchJSON = await fetchResp.json();

  onFinished()();
  if (fetchResp.ok) {
    return fetchJSON;
  } else {
    return Promise.reject(fetchJSON);
  }
}

export default function UploadDropdownElement(props) {
  const [formData, setFormData] = createSignal(null);
  const [fetchData] = createResource(formData, withOwner(((data, { owner }) => submitReq(data, () => props.url, () => props.onFinished, {owner}))));

  let fileUploadInput;
  let fileUploadForm;

  function onButtonClick() {
    fileUploadInput.click();
  }

  function onFormSubmit() {
    setFormData(new FormData(fileUploadForm));
    fileUploadForm.reset();
  }

  createEffect(() => props.onError(fetchData.error?.errors ?? []));

  return (
    <>
      <a class="dropdown-item" onClick={onButtonClick}>
        {props.title}
        <form ref={fileUploadForm}>
          <input
            ref={fileUploadInput}
            type="file"
            style={{"display":"none"}}
            name={props.name}
            accept={props.accept}
            onChange={onFormSubmit}
          />
        </form>
      </a>
    </>
  );
}
