// Install dependencies before running:
// npm install next react react-dom tailwindcss

// tailwind.config.js
module.exports = {
  content: ["./pages/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
};

// styles/globals.css
@tailwind base;
@tailwind components;
@tailwind utilities;

// pages/_app.js
import '../styles/globals.css';

function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />;
}

export default MyApp;

// pages/index.js
import Link from 'next/link';

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <nav className="bg-white shadow-md p-4 flex space-x-4">
        <button className="p-2 bg-gray-200 rounded">Menu 1</button>
        <button className="p-2 bg-gray-200 rounded">Menu 2</button>
        <Link href="/anomaly">
          <button className="p-2 bg-blue-500 text-white rounded">Anomaly</button>
        </Link>
      </nav>
    </div>
  );
}

// pages/anomaly.js
import { useState } from 'react';
import { useRouter } from 'next/router';

export default function Anomaly() {
  const router = useRouter();
  const [country, setCountry] = useState('');
  const [goal, setGoal] = useState('');
  const [kpi, setKpi] = useState('');

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <button className="p-2 bg-gray-500 text-white rounded mb-4" onClick={() => router.push('/')}>Back</button>
      <div className="bg-white p-6 shadow-md rounded w-96">
        <label className="block mb-2">Country</label>
        <select className="w-full p-2 border rounded mb-4" onChange={(e) => setCountry(e.target.value)}>
          <option value="">Select Country</option>
          <option value="USA">USA</option>
          <option value="India">India</option>
        </select>

        <label className="block mb-2">Goal</label>
        <select className="w-full p-2 border rounded mb-4" onChange={(e) => setGoal(e.target.value)}>
          <option value="">Select Goal</option>
          <option value="Growth">Growth</option>
          <option value="Stability">Stability</option>
        </select>

        <label className="block mb-2">KPI</label>
        <select className="w-full p-2 border rounded mb-4" onChange={(e) => setKpi(e.target.value)}>
          <option value="">Select KPI</option>
          <option value="Revenue">Revenue</option>
          <option value="Customer Satisfaction">Customer Satisfaction</option>
        </select>
      </div>
    </div>
  );
}
