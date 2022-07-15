import { createSignal, createContext, useContext, runWithOwner, createEffect, on } from "solid-js";

import Shepherd from "shepherd.js";

const ShepherdContext = createContext();

const addSteps = (steps, tour, def) => {
  // Return nothing if there are no steps
  if (!steps.length) {
    return [];
  }

  const parsedStepsforAction = steps.map((step) => {
    const { buttons } = step;

    if (buttons) {
      step.buttons = buttons.map((button) => {
        const { action, type, actionFunc } = button;
        return {
          action: type ? tour[type] : (actionFunc ? actionFunc(tour) : action),
          type,
          ...button
        };
      });
    }

    return {...def, ...step};
  });

  parsedStepsforAction.forEach((step: any) => tour.addStep(step));
};

export function ShepherdProvider(props) {
  const [steps, setSteps] = createSignal([]);
  const [onComplete, setOnComplete] = createSignal(null);

  const tourObject = new Shepherd.Tour(props.tourOptions);

  tourObject.on("complete", () => {
    if (onComplete()) {
      onComplete()();
    }
  });

  const clear = () => {
    tourObject.show(0);
    const prevSteps = tourObject.steps.map(step => step.id);
    for(const step of prevSteps) {
      tourObject.removeStep(step);
    }
  }

  createEffect(on(steps, () => {
    clear();
    addSteps(steps(), tourObject, props.tourOptions);
    tourObject.start();
  }));

  return (
    <ShepherdContext.Provider value={[tourObject, setSteps, setOnComplete, clear]}>
      {props.children}
    </ShepherdContext.Provider>
  );
}

export function useShepherd(
  owner?
): [Shepherd.Tour, (steps: Array<Shepherd.Step>) => void, (onComplete: any) => void, () => void] {
  if (owner) {
    return runWithOwner(owner, useShepherd);
  }
  return useContext(ShepherdContext) as  [Shepherd.Tour, (steps: Array<Shepherd.Step>) => void, (onComplete: any) => void, () => void];
}
