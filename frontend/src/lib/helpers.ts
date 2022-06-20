import { onMount, onCleanup } from "solid-js";
import { getOwner } from "solid-js/web";

export function withOwner(f) {
  const owner = getOwner();
  return (source, { value, refetching }) =>
    f(source, { value, refetching, owner });
}

export function onButton(button, f) {
  function onKeyDown(e) {
    if(e.code == button) {
      f(e);
    }
  }

  onMount(() => {
    document.addEventListener('keydown', onKeyDown);
  });

  onCleanup(() => {
    document.removeEventListener('keydown', onKeyDown);
  });
}
