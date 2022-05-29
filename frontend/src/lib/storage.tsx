import { createContext, useContext } from "solid-js";
import { createLocalStorage } from '@solid-primitives/storage';
import type { StorageObject, StorageSetter } from '@solid-primitives/storage';

const StorageContext = createContext();

export function StorageProvider(props) {
  const [storage, setStorage, {clear: clearStorage}] = createLocalStorage();
  return(
    <StorageContext.Provider value={[storage, setStorage, clearStorage]}>
      {props.children}
    </StorageContext.Provider>
  )
}

export function useStorage(): [StorageObject<string>, StorageSetter<string, unknown>, () => void] { return useContext(StorageContext) as [StorageObject<string>, StorageSetter<string, unknown>, () => void]; }
