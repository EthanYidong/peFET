import { createEffect, For } from 'solid-js';
import { createStore } from 'solid-js/store';

import ParticipantEditor from '@/components/participant-editor';
import type { Participant } from '@/models/participant';

export default function Create() {
  
  const [participants, setParticipants] = createStore<Participant[]>([]);

  function addButtonOnClick(_e) {
    setParticipants([...participants, {}]);
  }

  function saveButtonOnClick(_e) {
    console.log(participants);
  }

  return (
    <div class="flex flex-col p-8">
      <h1 class="text-2xl">Create New Event Listing</h1>
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
