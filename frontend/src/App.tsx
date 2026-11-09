import {useEffect,useState} from "react";
import {fetchStatement} from "./api";
import type {Statement,StatementSection} from "./types";

const DEFAULT_START="2026-01-01";
const DEFAULT_END="2026-03-31";

function formatMoney(amount:string,currency:string):string {
 const number=Number(amount);
 const formatted=new Intl.NumberFormat("en-US",{minimumFractionDigits:2,maximumFractionDigits:2}).format(Math.abs(number));
 const prefix=currency==="USD"?"$":currency+" ";
 return number<0?"("+prefix+formatted+")":prefix+formatted;
}

function Section({title,data,currency}:{title:string;data:StatementSection;currency:string}){
 return <tbody>
  <tr className="section-heading"><th colSpan={2} scope="rowgroup">{title}</th></tr>
  {data.accounts.map(row=><tr key={row.number}><td className="account"><span className="account-number">{row.number}</span>{row.name}</td><td className="amount">{formatMoney(row.amount,currency)}</td></tr>)}
  <tr className="subtotal"><th scope="row">Total {title}</th><td className="amount">{formatMoney(data.total,currency)}</td></tr>
 </tbody>;
}
function ResultRow({title,amount,currency,final=false}:{title:string;amount:string;currency:string;final?:boolean}){
 return <tbody><tr className={final?"net-income":"result-row"}><th scope="row">{title}</th><td className="amount">{formatMoney(amount,currency)}</td></tr></tbody>;
}

export default function App(){
 const [start,setStart]=useState(DEFAULT_START);
 const [end,setEnd]=useState(DEFAULT_END);
 const [requested,setRequested]=useState({start:DEFAULT_START,end:DEFAULT_END});
 const [statement,setStatement]=useState<Statement|null>(null);
 const [loading,setLoading]=useState(true);
 const [error,setError]=useState("");
 const invalid=!start||!end||start>end;

 useEffect(()=>{
  const controller=new AbortController();
  setLoading(true);setError("");
  fetchStatement(requested.start,requested.end,controller.signal)
   .then(setStatement)
   .catch((err:unknown)=>{if(!controller.signal.aborted){setError(err instanceof Error?err.message:"Unexpected error");}})
   .finally(()=>{if(!controller.signal.aborted)setLoading(false);});
  return ()=>controller.abort();
 },[requested]);

 function generate(event:React.FormEvent<HTMLFormElement>){
  event.preventDefault();
  if(!invalid)setRequested({start,end});
 }
 return <div className="app">
  <header className="topbar"><div className="topbar-inner"><div className="brand-mark" aria-hidden="true">N</div><div><div className="brand-name">{statement?.company??"Northwind Coffee Roasters"}</div><div className="brand-subtitle">FINANCIAL REPORTING</div></div><span className="currency-chip">{statement?.currency??"USD"}</span></div></header>
  <main className="container">
   <div className="page-heading"><div><p className="eyebrow">FINANCIAL STATEMENTS</p><h1>Income Statement</h1><p className="intro">Review revenue, expenses and profitability across any reporting period.</p></div></div>
   <form className="filters" onSubmit={generate}>
    <div className="filters-title"><h2>Reporting period</h2><button className="button button-secondary" type="button" onClick={()=>{setStart(DEFAULT_START);setEnd(DEFAULT_END);}}>↺ Reset to Q1 2026</button></div>
    <div className="date-grid"><label>Start date<input aria-label="Start date" type="date" required value={start} onChange={e=>setStart(e.target.value)}/></label><label>End date<input aria-label="End date" type="date" required value={end} onChange={e=>setEnd(e.target.value)}/></label></div>
    {start&&end&&start>end&&<p className="validation" role="alert">End date must be on or after the start date.</p>}
    <button className="button button-primary" type="submit" disabled={invalid||loading}>{loading?"Generating…":"Generate Statement"}</button>
   </form>
   {error&&<div className="error" role="alert">{error} <button className="button button-secondary" onClick={()=>setRequested({...requested})}>Retry</button></div>}
   {loading&&<p className="status" role="status">Loading income statement…</p>}
   {!loading&&statement&&<section className="report" aria-label="Income statement report">
    <div className="report-heading"><div><p className="eyebrow">PROFIT &amp; LOSS</p><h2>{statement.company}</h2><p>Income Statement · {statement.start} to {statement.end}</p></div><span className="report-currency">{statement.currency}</span></div>
    <div className="metrics"><div className="metric"><span>Total Revenue</span><strong>{formatMoney(statement.sections.revenue.total,statement.currency)}</strong></div><div className="metric"><span>Gross Profit</span><strong>{formatMoney(statement.gross_profit,statement.currency)}</strong></div><div className="metric"><span>Net Income</span><strong className={Number(statement.net_income)<0?"negative":""}>{formatMoney(statement.net_income,statement.currency)}</strong></div></div>
    <div className="table-scroll"><table><thead><tr><th scope="col">Account / Description</th><th scope="col" className="amount">Amount ({statement.currency})</th></tr></thead>
     <Section title="Revenue" data={statement.sections.revenue} currency={statement.currency}/>
     <Section title="Cost of Goods Sold" data={statement.sections.cogs} currency={statement.currency}/>
     <ResultRow title="Gross Profit" amount={statement.gross_profit} currency={statement.currency}/>
     <Section title="Operating Expenses" data={statement.sections.operating_expenses} currency={statement.currency}/>
     <ResultRow title="Operating Income" amount={statement.operating_income} currency={statement.currency}/>
     <Section title="Other Income" data={statement.sections.other_income} currency={statement.currency}/>
     <ResultRow title="Net Income" amount={statement.net_income} currency={statement.currency} final/>
    </table></div><p className="report-note">Amounts reflect posted journal entries within the selected dates, inclusive. Negative amounts are shown in parentheses.</p>
   </section>}
  </main>
 </div>;
}
