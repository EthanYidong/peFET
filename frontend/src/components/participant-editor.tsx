// TODO: support deletion
// TODO: validate input client side
import { untrack } from 'solid-js';

import type { Participant } from '@/models/participant';

export default function ParticipantEditor(props: {participant: Participant, edit: (propName: keyof Participant, value: any) => void}) {
  function inputHandler(propName, e) {
    props.edit(propName, e.target.value);
  }
  
  return (
    <div class="flex gap-x-2">
      <p>Name:</p>
      <input class="border-b-2 border-black focus:border-blue-600 outline-none" type="text" value={untrack(() => props.participant.name ?? '')} onInput={(e) => inputHandler('name', e)}></input>
      <p>Email:</p>
      <input class="border-b-2 border-black focus:border-blue-600 outline-none" type="text" value={untrack(() => props.participant.email ?? '')} onInput={(e) => inputHandler('email', e)}></input>
    </div>
  );
}
