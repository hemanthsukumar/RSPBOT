import defaultTheme from 'tailwindcss/defaultTheme';

export default {
  darkMode: 'class', // or 'media' if you want system-based
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', ...defaultTheme.fontFamily.sans],
      },
      colors: {
        neon: {
          purple: "#9333ea",
          violet: "#6366f1",
        },
      },
      boxShadow: {
        neon: "0 0 10px #6366f1, 0 0 20px #9333ea",
      },
      animation: {
        throw: "throwSequence 1.5s ease-in-out forwards",
      },
      keyframes: {
        throwSequence: {
          "0%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-10px)" },
          "100%": { transform: "translateY(0)" },
        },
      },
    },
  },
  plugins: [],
};