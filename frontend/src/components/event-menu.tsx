import { Show } from "solid-js";

import { useEvent } from "@/lib/event";
import MenuLink from "@/components/menu-link";

export default function EventMenu(props) {
  const event = useEvent();
  return (
    <li>
      <MenuLink href={`/dashboard/event/${props.event.id}`}>
        {props.event.name}
      </MenuLink>
      <Show when={event()?.id == props.event.id}>
        <ul>
          <li>
            <MenuLink href={`/dashboard/event/${props.event.id}/settings`}>
              Settings
            </MenuLink>
          </li>
        </ul>
      </Show>
    </li>
  );
}
