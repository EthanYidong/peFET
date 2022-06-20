import { FaSolidAngleDown, FaSolidEnvelope } from "solid-icons/fa";

import Dropdown from "@/components/dropdown";

export default function EmailDropdown(props) {
  return (
    <Dropdown
      title={
        <>
          <FaSolidEnvelope />
          <FaSolidAngleDown />
        </>
      }
      right={props.right}
    >
      <a class="dropdown-item" onClick={() => props.openEmailModal(true)}>
        Send to Selected
      </a>
    </Dropdown>
  );
}
