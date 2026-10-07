import { createTheme } from "@mui/material/styles";

// Single home for the MUI theme; no ad-hoc inline colours elsewhere.
export const theme = createTheme({
  palette: { mode: "light" },
});
