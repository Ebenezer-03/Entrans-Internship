/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#7B5CFF",
        "gradient-pink": "#FF50C8",
        "accent-blue": "#4B92FF",
        "sidebar-purple": "#4B3AFF",
        background: "#F4F2FF",
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
