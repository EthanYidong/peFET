import { createEffect, createMemo, Show, useContext } from "solid-js";
import { RouteContextObj } from "solid-app-router";

import MenuLink from "@/components/menu-link";

export default function EventMenu(props) {
  const route: any = useContext(RouteContextObj);
  const slug = createMemo(() => {
    let cur = route;
    let slug = cur.params.slug;
    while (!slug && cur.child) {
      cur = cur.child;
      slug = cur.params.slug;
    }
    return slug;
  });

  createEffect(() => console.log(slug()));

  return (
    <li>
      <MenuLink href={`/dashboard/event/${props.event.name}`}>
        {props.event.name}
      </MenuLink>
      <Show when={slug() == props.event.name}>
        <ul>
          <li>
            <MenuLink
              href={`/dashboard/event/${props.event.name}/settings`}
            >
              Settings
            </MenuLink>
          </li>
        </ul>
      </Show>
    </li>
  );
}
