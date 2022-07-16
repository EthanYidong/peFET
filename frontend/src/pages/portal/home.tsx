import { Show, createEffect, createSignal } from "solid-js";
import { Portal } from "solid-js/web";
import { useLocation } from "solid-app-router";

import Qr from "@/components/portal/qr";
import Picture from "@/components/portal/picture";
import Success from "@/components/success";
import exampleImgUrl from '@/static/example.jpg';

export default function Home() {
  const location = useLocation();

  const [qr, setQr] = createSignal(false);
  const [picture, setPicture] = createSignal(false);
  const [submitted, setSubmitted] = createSignal(false);

  createEffect(() => console.log(location.query.token));

  return (
    <>
      <Portal mount={document.getElementById("portal")}>
        <Show when={qr()}>
          <Qr onClose={() => setQr(false)}/>
        </Show>
      </Portal>
      <Show when={picture()}>
        <Picture onClose={(v) => {setPicture(false); setSubmitted(v);}}/>
      </Show>
      <Show when={!qr()}>
        <Show when={submitted()}>
          <Success success={["Successfully submitted!"]}/>
        </Show>
        <section class="section">
          <h1 class="title">
            peFET submission portal
          </h1>
        </section>
        <section class="section">
          <div class="columns">
            <div class="column is-narrow">
              <button class="button is-large is-primary" onClick={() => setQr(true)}>Show QR Code</button>
            </div>
            <div class="column is-narrow">
              <button class="button is-large is-info" onClick={() => {setPicture(true); setSubmitted(false);}}>Take Picture</button>
            </div>
          </div>
        </section>

        <section class="section">
          <div class="content">
            <h5 class="subtitle is-5">Directions</h5>
            <p>On a laptop (recommended), desktop, tablet, or any device with a sufficently large screen, click the Show QR Code button and position your completed test such that the QR code and test can be in the same picture, with both of them being fully visible.</p>
            <p>On a phone (recommended), tablet, or any device with an easily positionable camera, click the Take Picture button to upload a photo of the QR code and the completed test.</p>
          </div>
          <div class="content">
            <h5 class="subtitle is-5">Example</h5>
            <img class="is-half" src={exampleImgUrl} style={{"width": "50vw"}}/>
          </div>
        </section>
      </Show>
    </>
  );
}
