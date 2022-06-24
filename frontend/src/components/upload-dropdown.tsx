import { FaSolidAngleDown, FaSolidUpload } from "solid-icons/fa";

import { useEvent } from "@/lib/event";
import { API_URL } from "@/lib/api";
import Dropdown from "@/components/dropdown";
import UploadDropdownElement from "@/components/upload-dropdown-element";

export default function UploadDropdown(props) {
  const event = useEvent();
  return (
    <Dropdown
      title={
        <>
          <FaSolidUpload />
          <FaSolidAngleDown />
        </>
      }
      right={props.right}
    >
      <UploadDropdownElement
        title="Upload CSV Data"
        name="csv"
        accept=".csv"
        url={`${API_URL}/api/event/${event().id}/participants/create_csv`}
        onError={props.onError}
        onFinished={props.refetchEvent}
      />
    </Dropdown>
  );
}
