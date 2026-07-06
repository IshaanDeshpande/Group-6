/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './templates/**/*.html',
    './apps/**/*.html',
    './apps/**/*.py',
    './static/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        'nav-bg': '#1F452D',
        'button-bg': '#ADD6C5',
      },
      fontFamily: {
        'heading': ['Inter', '-apple-system', 'Roboto', 'Helvetica', 'sans-serif'],
        'subtitle': ['Oswald', '-apple-system', 'Roboto', 'Helvetica', 'sans-serif'],
      },
    },
  },
  plugins: [require('daisyui')],
  daisyui: {
    themes: ['light'],
  },
}
