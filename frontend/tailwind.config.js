module.exports = {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3D85C6',
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms')
  ],
}
