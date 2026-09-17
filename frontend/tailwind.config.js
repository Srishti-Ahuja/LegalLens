/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        slate: require('tailwindcss/colors').slate,
        amber: require('tailwindcss/colors').amber,
        red: require('tailwindcss/colors').red,
        emerald: require('tailwindcss/colors').emerald,
        charcoal: '#2D2D2D',
        plum: '#7D3C98',
        beige: '#F5F5DC',
        magenta: '#FF00FF',
      }
    },
  },
  plugins: [],
};
