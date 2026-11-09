export interface AccountRow {number:string;name:string;amount:string}
export interface StatementSection {accounts:AccountRow[];total:string}
export interface Statement {company:string;currency:string;start:string;end:string;sections:{revenue:StatementSection;cogs:StatementSection;operating_expenses:StatementSection;other_income:StatementSection};gross_profit:string;operating_income:string;net_income:string}
