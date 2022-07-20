import { createEffect, createSelector, createSignal, For } from "solid-js";
import { FaSolidAngleDown, FaSolidFilter } from "solid-icons/fa";

import Dropdown from "@/components/dropdown";

const FILTERS = [
  {name: "All", filter: (p) => true},
  {name: "Submitted", filter: (p) => p.status === "Y"},
  {name: "Not Submitted", filter: (p) => p.status === "N"}
];

export default function FilterDropdown(props) {
  const [selectedFilter, setSelectedFilter] = createSignal(0);
  const isSelected = createSelector(selectedFilter);

  createEffect(() => {
    props.setFilter(() => FILTERS[selectedFilter()].filter);
  });

  return (
    <Dropdown
      title={
        <>
          <FaSolidFilter />
          <FaSolidAngleDown />
        </>
      }
      right={props.right}
    >
      <For each={FILTERS}>{
        ({name}, index) => 
          <a class="dropdown-item" classList={{"is-active": isSelected(index())}} onClick={() => setSelectedFilter(index())}>
            {name}
          </a>
      }</For>
      
    </Dropdown>
  );
}
