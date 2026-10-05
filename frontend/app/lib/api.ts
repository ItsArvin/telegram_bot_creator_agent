const API_URL = process.env.NEXT_PUBLIC_API_URL!;
export async function api<T>(path:string, init:RequestInit={}):Promise<T>{
 const r=await fetch(API_URL+path,{...init,credentials:"include",headers:{"Content-Type":"application/json",...(init.headers??{})}});
 if(!r.ok){const b=await r.json().catch(()=>({}));throw new Error(b.detail??"Request failed")}
 if(r.status===204)return undefined as T;
 return r.json();
}
export type User={id:string;email:string;created_at:string};
