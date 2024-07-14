/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,j2}"],
  theme: {
    extend: {
      letterSpacing: {
        '5': '0.05em',
        '10': '0.1em',
      },
      fontFamily: {
        roundark: ['Roundark', 'sans-serif']
      }
    },
  },
  plugins: [],
}
