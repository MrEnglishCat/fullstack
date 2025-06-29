import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

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
        <p><strong>Скидка:</strong> {label}% </p>
        <p style={{ color: "#82ca9d" }}><strong>Рейтинг:</strong> {payload[0].value}</p>
      </div>
    );
  }

  return null;
};



const DiscountVsRatingLineChart = ({ data }) => {
  const chartData = data.map(product => ({
    discount: Math.round((product.price - product.sale_price) * 100 / product.price, 3),
    rating: product.rating,
  })).sort();

  return (
    <LineChart width={500} height={300} data={chartData}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="discount" label={{value: "Скидка (%)", position: "insideBottom", dy:20}} />
      <YAxis label={{value: "Рейтинг", position: "insideLeft", angle: -90, dx:10}} />
      <Tooltip  content={<CustomTooltip />} />
      <Legend align="right"/>
      <Line type="monotone" dataKey="rating" stroke="#82ca9d" />
    </LineChart>
  );
};

export default DiscountVsRatingLineChart;