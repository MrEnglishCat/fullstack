
export async function fetchRangeValues(setter, value) {
    try {
        const response = await fetch(`http://localhost:8000/api/products/rangeValue?value=${value}`);

        if (!response.ok) {
            throw new Error("Ошибка запроса к API.");
        }

        const data = await response.json();
        setter(data);
    } catch (error) {
        console.error("Ошибка при загрузке данных:", error);
    }
}
