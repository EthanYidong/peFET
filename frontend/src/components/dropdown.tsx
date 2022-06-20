import { createSignal, children } from "solid-js";
import { FaSolidAngleDown, FaSolidEnvelope } from "solid-icons/fa";

import { clickOutside } from "@/lib/directives";

export default function Dropdown(props) {
  const [toggled, setToggled] = createSignal(false);

  const c = children(() => props.children);

  return (
    <div
      class="dropdown"
      classList={{ "is-active": toggled(), "is-right": props.right }}
    >
      <div class="dropdown-trigger">
        <button
          class="button"
          onClick={() => setToggled(!toggled())}
          use:clickOutside={() => setToggled(false)}
        >
          {props.title}
        </button>
      </div>
      <div class="dropdown-menu" role="menu">
        <div class="dropdown-content">{c()}</div>
      </div>
    </div>
  );
}
