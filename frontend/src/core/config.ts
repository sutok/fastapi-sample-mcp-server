export const config = {
  api: {
    baseUrl:
      process.env.NODE_ENV === "development"
        ? "http://localhost:8000/api/v1"
        : `https://${window.location.host}/api/v1`,
  },
};
