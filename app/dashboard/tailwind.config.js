/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'aria-bg': '#0B1120',
        'aria-card': '#111827',
        'aria-border': '#1F2937',
        'aria-cyan': '#22d3ee',
        'aria-green': '#10b981',
        'aria-amber': '#f59e0b',
        'aria-red': '#ef4444',
      }
    },
  },
  plugins: [],
}
