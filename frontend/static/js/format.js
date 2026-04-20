export const money = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
});

export function currentMonth() {
  const now = new Date();
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}`;
}

export function formPayload(form) {
  const data = new FormData(form);
  return Object.fromEntries(data.entries());
}

export function numberFields(payload, fields) {
  return fields.reduce(
    (result, field) => ({
      ...result,
      [field]: Number(payload[field]),
    }),
    payload,
  );
}
