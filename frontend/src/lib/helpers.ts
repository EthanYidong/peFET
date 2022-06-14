import { getOwner } from "solid-js/web";

export function withOwner(f) {
  const owner = getOwner();
  return (source, { value, refetching }) =>
    f(source, { value, refetching, owner });
}
