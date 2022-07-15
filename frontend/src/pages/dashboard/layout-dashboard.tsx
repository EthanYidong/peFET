import { createEffect, For, Show } from "solid-js";
import { Outlet, useRouteData } from "solid-app-router";
import { FaSolidAngleLeft } from "solid-icons/fa";

import MenuLink from "@/components/menu-link";
import EventMenu from "@/components/event-menu";
import { EventContextProvider } from "@/lib/event";
import type { RouteData } from "@/lib/route-data";

export default function LayoutBase() {
  const routeData: RouteData = useRouteData();
  createEffect(() => console.log(routeData.events()));
  return (
    <EventContextProvider>
      <div class="is-flex is-flex-direction-column fullheight">
        <section class="hero is-small">
          <div class="hero-body">
            <h1 class="title">Dashboard</h1>
          </div>
        </section>
        <section
          class="section is-flex-shrink-1 is-flex-grow-1"
          style={{ "min-height": "0" }}
        >
          <div class="columns" style={{ height: "100%" }}>
            <div class="column is-2">
              <aside class="menu">
                <ul class="menu-list">
                  <li>
                    <MenuLink href="/">
                      <FaSolidAngleLeft
                        style={{ "vertical-align": "middle" }}
                      />
                      Exit
                    </MenuLink>
                  </li>
                  <li>
                    <MenuLink href="/dashboard">Dashboard</MenuLink>
                  </li>
                </ul>
                <Show when={routeData.events()}>
                  <p class="menu-label">Events</p>
                  <ul class="menu-list">
                    <For each={routeData.events().events}>
                      {(event) => <EventMenu event={event} />}
                    </For>
                  </ul>
                </Show>
              </aside>
            </div>
            <div class="column is-10" style={{ "overflow-y": "scroll" }}>
              <Outlet />
            </div>
          </div>
        </section>
      </div>
    </EventContextProvider>
  );
}
