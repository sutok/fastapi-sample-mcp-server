import { TextField, TextFieldProps } from "@mui/material";
import { styled } from "@mui/material/styles";

interface InputProps extends Omit<TextFieldProps, "variant"> {
  label: string;
  error?: string;
}

const StyledTextField = styled(TextField)(({ theme }) => ({
  "& .MuiOutlinedInput-root": {
    borderRadius: theme.shape.borderRadius,
    "&.Mui-focused": {
      "& .MuiOutlinedInput-notchedOutline": {
        borderColor: theme.palette.primary.main,
      },
    },
  },
}));

export const Input: React.FC<InputProps> = ({ error, ...props }) => {
  return (
    <StyledTextField
      variant="outlined"
      fullWidth
      error={!!error}
      helperText={error}
      {...props}
    />
  );
};
