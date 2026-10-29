import { parseScene, type Scene } from "./model";
let database: Promise<IDBDatabase> | undefined;
function db() {
  return (database ||= new Promise<IDBDatabase>((resolve, reject) => {
    const req = indexedDB.open("niji-simulation", 1);
    req.onupgradeneeded = () => {
      req.result.createObjectStore("scenes", { keyPath: "id" });
      req.result.createObjectStore("settings");
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  }));
}
export async function saveDraft(scene: Scene) {
  const connection = await db();
  return new Promise<void>((resolve, reject) => {
    const tx = connection.transaction(["scenes", "settings"], "readwrite");
    tx.objectStore("scenes").put(scene);
    tx.objectStore("settings").put(scene.id, "active");
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
    tx.onabort = () => reject(tx.error);
  });
}
export async function drafts(): Promise<Scene[]> {
  const connection = await db();
  return new Promise((resolve, reject) => {
    const req = connection.transaction("scenes").objectStore("scenes").getAll();
    req.onsuccess = () =>
      resolve(
        req.result
          .map(parseScene)
          .sort((a: Scene, b: Scene) => b.updatedAt.localeCompare(a.updatedAt)),
      );
    req.onerror = () => reject(req.error);
  });
}
export async function activeDraft(): Promise<Scene | undefined> {
  const connection = await db();
  return new Promise((resolve, reject) => {
    const tx = connection.transaction(["settings", "scenes"]);
    const key = tx.objectStore("settings").get("active");
    key.onsuccess = () => {
      if (!key.result) {
        resolve(undefined);
        return;
      }
      const req = tx.objectStore("scenes").get(key.result);
      req.onsuccess = () => {
        try {
          resolve(req.result ? parseScene(req.result) : undefined);
        } catch (error) {
          reject(error);
        }
      };
      req.onerror = () => reject(req.error);
    };
    key.onerror = () => reject(key.error);
  });
}
