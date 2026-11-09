import type {Statement} from "./types";
export async function fetchStatement(start:string,end:string,signal?:AbortSignal):Promise<Statement>{
 const params=new URLSearchParams({start,end});
 const response=await fetch(`/income-statement?${params}`,{signal});
 if(!response.ok){throw new Error(response.status===422?"Please select a valid date range.":"Unable to load the statement. Check that the backend is running.");}
 return response.json() as Promise<Statement>;
}
