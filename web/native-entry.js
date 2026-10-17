import { Capacitor } from '@capacitor/core';
import { Filesystem, Directory } from '@capacitor/filesystem';
import { Share } from '@capacitor/share';
globalThis.MarcoNative = {
  isNative: () => Capacitor.isNativePlatform(),
  async save(blob,name) {
    const bytes=new Uint8Array(await blob.arrayBuffer());
    let binary='';for(let i=0;i<bytes.length;i+=32768) binary+=String.fromCharCode(...bytes.subarray(i,i+32768));
    const result=await Filesystem.writeFile({path:name,data:btoa(binary),directory:Directory.Cache});
    await Share.share({title:name,files:[result.uri]});
  }
};
