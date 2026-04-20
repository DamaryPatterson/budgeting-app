import {
  createBudget,
  createGoal,
  createRecurringItem,
  createTransaction,
  deleteBudget,
  deleteGoal,
  deleteRecurringItem,
  deleteTransaction,
  getSummary,
} from "./api.js";
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
document.addEventListener("click", handleDelete);

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

async function handleDelete(event) {
  const button = event.target.closest("[data-delete-type][data-delete-id]");
  if (!button) {
    return;
  }

  const { deleteType, deleteId } = button.dataset;
  button.disabled = true;

  try {
    await deleteItem(deleteType, deleteId);
    await refresh();
  } catch (error) {
    console.error(error);
    alert("Something went wrong while deleting that item.");
    button.disabled = false;
  }
}

function deleteItem(type, id) {
  const actions = {
    budget: deleteBudget,
    goal: deleteGoal,
    recurring: deleteRecurringItem,
    transaction: deleteTransaction,
  };

  return actions[type](id);
}

refresh();
