import {
  Button as MuiButton,
  ButtonProps as MuiButtonProps,
} from "@mui/material";
import { styled } from "@mui/material/styles";

interface ButtonProps extends MuiButtonProps {
  variant?: "primary" | "secondary" | "danger";
  size?: "sm" | "md" | "lg";
}

const StyledButton = styled(MuiButton)<ButtonProps>(({ theme, variant }) => ({
  borderRadius: theme.shape.borderRadius,
  textTransform: "none",
  ...(variant === "primary" && {
    backgroundColor: theme.palette.primary.main,
    color: theme.palette.primary.contrastText,
    "&:hover": {
      backgroundColor: theme.palette.primary.dark,
    },
  }),
  ...(variant === "danger" && {
    backgroundColor: theme.palette.error.main,
    color: theme.palette.error.contrastText,
    "&:hover": {
      backgroundColor: theme.palette.error.dark,
    },
  }),
}));

export const Button: React.FC<ButtonProps> = (props) => {
  return <StyledButton {...props} />;
};
