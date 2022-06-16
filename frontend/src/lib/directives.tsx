import { onCleanup } from "solid-js";

declare module "solid-js" {
  namespace JSX {
    interface Directives {
      customFormHandler: (v: any, {form: any}) => any;
    }
  }
}

export function customFormHandler(el, accessor) {
  const onSubmit = (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = {};
    for (let field of formData) {
      const [key, value] = field;
      data[key] = value;
    }
    accessor()?.(data, {form: el});
  };
  el.addEventListener("submit", onSubmit);

  onCleanup(() => el.removeEventListener("submit", onSubmit, false));
}
