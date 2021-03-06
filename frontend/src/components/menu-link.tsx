import { useMatch } from "solid-app-router";

export default function MenuLink(props) {
  const match = useMatch(() => props.href);

  return (
    <a class={props.class} classList={{ "is-active": Boolean(match()) }} href={props.href}>
      {props.children}
    </a>
  );
}
