import { Show, For } from "solid-js";

export default function Success(props) {
  return (
    <Show when={props.success && props.success.length}>
      <section class="section">
        <article class="message is-success">
          <div class="message-body">
            <ul>
              <For each={props.success}>
                {(success: string) => <li>{success}</li>}
              </For>
            </ul>
          </div>
        </article>
      </section>
    </Show>
  );
}
