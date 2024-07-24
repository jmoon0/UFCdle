import { createContext, useContext, useEffect, useState } from "react";

// Define the possible theme values as a constant
const THEMES = {
  DARK: "dark",
  LIGHT: "light",
  SYSTEM: "system",
};

// Create the initial state with default values
const initialState = {
  theme: THEMES.SYSTEM,
  setTheme: () => null,
};

// Create the context with the initial state
const ThemeProviderContext = createContext(initialState);

// ThemeProvider component definition
export function ThemeProvider({ children, defaultTheme = THEMES.SYSTEM, storageKey = "vite-ui-theme", ...props }) {
  const [theme, setTheme] = useState(() => {
    // Retrieve the theme from localStorage or use the defaultTheme
    const storedTheme = localStorage.getItem(storageKey);
    return storedTheme || defaultTheme;
  });

  useEffect(() => {
    const root = document.documentElement;

    // Remove existing theme classes
    root.classList.remove(THEMES.LIGHT, THEMES.DARK);

    if (theme === THEMES.SYSTEM) {
      // Apply the system theme based on the user's system preferences
      const systemTheme = window.matchMedia("(prefers-color-scheme: dark)").matches ? THEMES.DARK : THEMES.LIGHT;
      root.classList.add(systemTheme);
      return;
    }

    // Apply the selected theme
    root.classList.add(theme);
  }, [theme]);

  const value = {
    theme,
    setTheme: (newTheme) => {
      localStorage.setItem(storageKey, newTheme);
      setTheme(newTheme);
    },
  };

  return (
    <ThemeProviderContext.Provider value={value} {...props}>
      {children}
    </ThemeProviderContext.Provider>
  );
}

// Custom hook to use the theme context
export const useTheme = () => {
  const context = useContext(ThemeProviderContext);

  if (context === undefined) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }

  return context;
};
