module.exports = {
  content: ["./templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        overlay: "rgba(0, 0, 0, 0.5)",
      },
      zIndex: {
        9999: "9999",
      },
    },
  },
  plugins: [],
};
