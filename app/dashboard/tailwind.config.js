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
        'aria-bg-darker': '#050810',
        'aria-card': '#111827',
        'aria-card-hover': '#1F2937',
        'aria-border': '#1F2937',
        'aria-border-light': '#374151',
        'aria-cyan': '#22d3ee',
        'aria-cyan-dim': 'rgba(34, 211, 238, 0.15)',
        'aria-green': '#10b981',
        'aria-amber': '#f59e0b',
        'aria-red': '#ef4444',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 3s ease-in-out infinite',
        'spin-slow': 'spin 8s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        }
      }
    },
  },
  plugins: [],
}
