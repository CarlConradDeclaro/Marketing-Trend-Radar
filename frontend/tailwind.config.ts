import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          950: "#07111f",
          900: "#0b1629",
          800: "#12213a",
        },
      },
      boxShadow: {
        glow: "0 24px 80px rgba(56, 189, 248, 0.18)",
      },
    },
  },
  plugins: [],
};

export default config;
