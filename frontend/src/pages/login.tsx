import { createSignal, createResource, createEffect, untrack } from 'solid-js';
import { useNavigate } from 'solid-app-router';

import { customFormHandler } from '@/lib/custom-form-handler';
import { API_URL, useToken } from '@/lib/api';
import Errors from '@/components/errors';

async function loginReq(data) {
  let fetchResp = await fetch(API_URL + '/api/account/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data) 
  });

  let fetchJSON = await fetchResp.json();

  if (fetchResp.ok) {
    return fetchJSON;
  } else {
    return Promise.reject(fetchJSON);
  }
}

export default function Login() {
  const [formData, setFormData] = createSignal(null);
  const [loginData] = createResource(formData, loginReq);
  const [token, setToken, _clearToken] = useToken();
  const navigate = useNavigate();

  function onLoginFormSubmit(data) {
    setFormData(data);
  }

  createEffect(() => {
    if(loginData()){
      setToken(loginData().token);
    }
  });

  createEffect(() => {
    if(token()) {
      navigate('/create');
    }
  });

  return (
    <div class="w-screen h-screen flex flex-col justify-center items-center">
      <div class="w-1/2 flex flex-col gap-2 border-2 rounded-md p-2">
        <h1 class="text-2xl font-bold">Login</h1>
        <Errors errors={loginData.error?.errors}></Errors>
        <form use:customFormHandler={onLoginFormSubmit}>
          <div class="flex flex-col gap-2">
          <div class="flex gap-2 h-8">
            <p class="w-1/5">Email: </p>
            <input class="account-form" type="text" name="email"></input>
          </div>
          <div class="flex gap-2 h-8">
            <p class="w-1/5">Password: </p>
            <input class="account-form" type="password" name="password"></input>
          </div>
          <button class="account-btn" type="submit">Login</button>
          </div>
        </form>
      </div>
    </div>
  );
};
