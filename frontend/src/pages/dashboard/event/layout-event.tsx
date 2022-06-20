import { Show, createEffect } from "solid-js";
import { Outlet, useRouteData } from "solid-app-router";

import { useEvent } from "@/lib/event";

export default function LayoutEvent() {
  const routeData: any = useRouteData();
  const event = useEvent();

  createEffect(() => console.log(routeData.event()));

  return (
    <Show when={event()}>
      <Outlet />
    </Show>
  );
}
