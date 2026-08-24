import { createTheme } from "@mui/material/styles";

// The single source of brand color/type — components style through these tokens, never raw hex.
const serif = '"Iowan Old Style","Palatino Linotype",Palatino,Georgia,Cambria,serif';
const mono = 'ui-monospace,"SF Mono","JetBrains Mono",Menlo,Consolas,monospace';

export const theme = createTheme({
  palette: {
    mode: "dark",
    background: { default: "#0f1620", paper: "#18212e" },
    primary: { main: "#6ba3c9" },
    secondary: { main: "#d99a5c" },
    success: { main: "#7fc99b" },
    text: { primary: "#eae3d6", secondary: "#9aa6b6" },
    divider: "#293546",
  },
  typography: {
    fontFamily: serif,
    h1: { fontFamily: serif, fontWeight: 700, letterSpacing: "-0.02em" },
    h3: { fontFamily: serif, fontWeight: 700, letterSpacing: "-0.01em" },
    h5: { fontFamily: serif, fontWeight: 700 },
    h6: { fontFamily: serif, fontWeight: 700 },
    button: { fontFamily: mono, textTransform: "none" },
    caption: { fontFamily: mono, letterSpacing: "0.02em" },
  },
  shape: { borderRadius: 10 },
});
