import { Show, For, createEffect } from 'solid-js';

export default function Errors(props) {
  return(
    <Show when={props.errors && props.errors.length}>
        <div class="m-2 p-2 bg-red-600 text-white">
          <ul>
            <For each={props.errors}>
              {(error: string) => <li>{error}</li>}
            </For>
          </ul>
        </div>
    </Show>
  );
}
