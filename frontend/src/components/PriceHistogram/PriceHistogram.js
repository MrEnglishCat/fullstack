import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div style={{
        backgroundColor: '#fff',
        border: '1px solid #ccc',
        padding: '10px',
        borderRadius: '4px',
        color: '#000',
        boxShadow: '0 2px 6px rgba(0,0,0,0.2)',
      }}>
        <p><strong>Цена:</strong> {label} BYN</p>
        <p style={{ color: "#82ca9d" }}><strong>Количество:</strong> {payload[0].value}</p>
      </div>
    );
  }

  return null;
};

const PriceHistogram = ({ data }) => {
  const bins = [0, 200, 400, 600, 800, 1000, 2000, 3000, 4000];
  const histogramData = bins.map((bin, i) => {
    if (i === 0) return { range: `0-${bin}`, count: 0 };
    const start = bins[i - 1];
    const end = bin;
    const count = data.filter(p => p.price > start && p.price <= end).length;
    return { range: `${start}-${end}`, count };
  });

  return (
    <BarChart width={500} height={300} data={histogramData}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="range" />
      <YAxis />
      <Tooltip content={<CustomTooltip />} />
      <Legend  align="right"/>
      <Bar dataKey="count" fill="#8884d8" name="Количество товаров" />
    </BarChart>
  );
};

export default PriceHistogram;