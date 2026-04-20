import { createBudget, createGoal, createRecurringItem, createTransaction, getSummary } from "./api.js";
import { currentMonth, formPayload, numberFields } from "./format.js";
import { renderSummary } from "./render.js";

const monthInput = document.getElementById("monthInput");
const forms = {
  transaction: document.getElementById("transactionForm"),
  budget: document.getElementById("budgetForm"),
  goal: document.getElementById("goalForm"),
  recurring: document.getElementById("recurringForm"),
};

monthInput.value = currentMonth();
forms.transaction.date.valueAsDate = new Date();

monthInput.addEventListener("change", refresh);

forms.transaction.addEventListener("submit", async (event) => {
  event.preventDefault();
  await createTransaction(numberFields(formPayload(forms.transaction), ["amount"]));
  forms.transaction.reset();
  forms.transaction.date.valueAsDate = new Date();
  await refresh();
});

forms.budget.addEventListener("submit", async (event) => {
  event.preventDefault();
  await createBudget(numberFields(formPayload(forms.budget), ["monthly_limit"]));
  forms.budget.reset();
  await refresh();
});

forms.goal.addEventListener("submit", async (event) => {
  event.preventDefault();
  await createGoal(numberFields(formPayload(forms.goal), ["target_amount", "saved_amount"]));
  forms.goal.reset();
  await refresh();
});

forms.recurring.addEventListener("submit", async (event) => {
  event.preventDefault();
  await createRecurringItem(numberFields(formPayload(forms.recurring), ["amount", "day_of_month"]));
  forms.recurring.reset();
  forms.recurring.day_of_month.value = 1;
  await refresh();
});

async function refresh() {
  try {
    renderSummary(await getSummary(monthInput.value));
  } catch (error) {
    console.error(error);
    alert("Something went wrong while loading your budget data.");
  }
}

refresh();
