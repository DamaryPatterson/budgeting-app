import { money } from "./format.js";

export function renderSummary(summary) {
  setText("incomeValue", money.format(summary.total_income));
  setText("expenseValue", money.format(summary.total_expenses));
  setText("cashflowValue", money.format(summary.net_cashflow));
  setText("budgetedValue", money.format(summary.total_budgeted));

  renderBudgets(summary.budget_status);
  renderGoals(summary.goals);
  renderRecurring(summary.upcoming_recurring);
  renderTransactions(summary.recent_transactions);
}

function renderBudgets(items) {
  const html = items
    .map((item) => {
      const spentPercent = item.monthly_limit === 0 ? 0 : Math.min((item.spent / item.monthly_limit) * 100, 100);
      const remainingClass = item.remaining < 0 ? "over" : "";
      return `
        <div class="item">
          <div class="item-row">
            <span class="item-title">${escapeHtml(item.category)}</span>
            <strong class="${remainingClass}">${money.format(item.remaining)}</strong>
          </div>
          <p class="item-meta">${money.format(item.spent)} spent of ${money.format(item.monthly_limit)}</p>
          <div class="progress"><span style="width: ${spentPercent}%"></span></div>
        </div>
      `;
    })
    .join("");
  setHtml("budgetList", html || empty("No category budgets yet."));
}

function renderGoals(items) {
  const html = items
    .map(
      (item) => `
        <div class="item">
          <div class="item-row">
            <span class="item-title">${escapeHtml(item.name)}</span>
            <strong>${item.progress}%</strong>
          </div>
          <p class="item-meta">${money.format(item.saved_amount)} saved of ${money.format(item.target_amount)}</p>
          <div class="progress"><span style="width: ${item.progress}%"></span></div>
        </div>
      `,
    )
    .join("");
  setHtml("goalList", html || empty("No savings goals yet."));
}

function renderRecurring(items) {
  const html = items
    .map(
      (item) => `
        <div class="item">
          <div class="item-row">
            <span class="item-title">${escapeHtml(item.description)}</span>
            <strong class="amount ${item.kind}">${money.format(item.amount)}</strong>
          </div>
          <p class="item-meta">${escapeHtml(item.category)} on day ${item.day_of_month}</p>
        </div>
      `,
    )
    .join("");
  setHtml("recurringList", html || empty("No recurring items yet."));
}

function renderTransactions(items) {
  const html = items
    .map(
      (item) => `
        <div class="item">
          <div class="item-row">
            <span class="item-title">${escapeHtml(item.description)}</span>
            <strong class="amount ${item.kind}">${item.kind === "income" ? "+" : "-"}${money.format(item.amount)}</strong>
          </div>
          <p class="item-meta">${item.date} · ${escapeHtml(item.category)}</p>
        </div>
      `,
    )
    .join("");
  setHtml("transactionList", html || empty("No transactions this month."));
}

function setText(id, value) {
  document.getElementById(id).textContent = value;
}

function setHtml(id, value) {
  document.getElementById(id).innerHTML = value;
}

function empty(message) {
  return `<p class="empty">${message}</p>`;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
