/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      animation: {
        "bounce": "bounce 1s infinite",
      },
    },
  },
  plugins: [],
};
