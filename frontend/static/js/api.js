const headers = {
  "Content-Type": "application/json",
};

export async function getSummary(month) {
  const query = month ? `?month=${encodeURIComponent(month)}` : "";
  return request(`/api/summary${query}`);
}

export async function createTransaction(payload) {
  return request("/api/transactions", {
    method: "POST",
    headers,
    body: JSON.stringify(payload),
  });
}

export async function deleteTransaction(id) {
  return request(`/api/transactions/${encodeURIComponent(id)}`, {
    method: "DELETE",
  });
}

export async function createBudget(payload) {
  return request("/api/budgets", {
    method: "POST",
    headers,
    body: JSON.stringify(payload),
  });
}

export async function deleteBudget(id) {
  return request(`/api/budgets/${encodeURIComponent(id)}`, {
    method: "DELETE",
  });
}

export async function createGoal(payload) {
  return request("/api/goals", {
    method: "POST",
    headers,
    body: JSON.stringify(payload),
  });
}

export async function deleteGoal(id) {
  return request(`/api/goals/${encodeURIComponent(id)}`, {
    method: "DELETE",
  });
}

export async function createRecurringItem(payload) {
  return request("/api/recurring-items", {
    method: "POST",
    headers,
    body: JSON.stringify(payload),
  });
}

export async function deleteRecurringItem(id) {
  return request(`/api/recurring-items/${encodeURIComponent(id)}`, {
    method: "DELETE",
  });
}

async function request(path, options = {}) {
  const response = await fetch(path, options);

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || "Request failed");
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}
