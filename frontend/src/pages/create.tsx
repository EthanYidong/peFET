import { createResource, For } from 'solid-js';
import { createStore } from 'solid-js/store';
import { useNavigate, Link } from 'solid-app-router';

import ParticipantEditor from '@/components/participant-editor';
import type { Participant } from '@/lib/models/participant';
import { API_URL, useToken } from '@/lib/api';

export default function Create() {
  const [token, _setToken, clearToken] = useToken(); 
  const [participants, setParticipants] = createStore<Participant[]>([]);
  const navigate = useNavigate();

  async function validateToken() {
    if(!token()) navigate('/login');
    let fetchResp = await fetch(API_URL + '/api/account/validate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({token: token()}) 
    });


    if (!fetchResp.ok) {
      clearToken();
      navigate('/login');
    }
  }

  function addButtonOnClick(_e) {
    setParticipants([...participants, {}]);
  }

  function saveButtonOnClick(_e) {
    console.log(participants);
  }

  createResource(validateToken);

  return (
    <div class="flex flex-col p-8 gap-2">
      <div><Link class="bg-blue-600 text-white p-2 rounded-md" href='/'>&lt; Home</Link></div>
      <h1 class="text-2xl">Create New Event Listing</h1>
      <h2 class="text-xl">If you're seeing this, that means you have successfully logged in. This page does not affect anything. It is only to demonstrate that the user is logged in, and serve as a prototype for event creation.</h2>
      <div>
        <ul>
        <For each={participants}>
          {(pt, idx) => (
            <li class="my-2">
              <ParticipantEditor participant={pt} edit={(propName, value) => setParticipants(idx(), propName, value)}/>
            </li>
          )}
        </For>
        </ul>
      </div>
      <div class="flex">
        <button class="button bg-blue-600 rounded-md w-16 text-white m-2" onClick={addButtonOnClick}>+</button>
        <button class="button bg-green-600 rounded-md w-16 text-white m-2" onClick={saveButtonOnClick}>Save</button>
      </div>
    </div>
  );
};
