import nextConfig from "eslint-config-next";
import tsParser from "@typescript-eslint/parser";

const eslintConfig = [
  // Replace babel parser (incompatible with ESLint 10) with @typescript-eslint/parser for JS/JSX files,
  // and fix react.version setting to avoid context.getFilename() call removed in ESLint 10.
  ...nextConfig.map((config) => {
    let updated = config;

    // Replace babel parser with @typescript-eslint/parser (babel parser lacks addGlobals for ESLint 10)
    if (config.languageOptions?.parser?.meta?.name === "eslint-config-next/parser") {
      updated = {
        ...updated,
        languageOptions: {
          ...updated.languageOptions,
          parser: tsParser,
        },
      };
    }

    // Override react.version from 'detect' to '19' to avoid context.getFilename() which was removed in ESLint 10
    if (config.settings?.react?.version === "detect") {
      updated = {
        ...updated,
        settings: {
          ...updated.settings,
          react: {
            ...updated.settings.react,
            version: "19",
          },
        },
      };
    }

    return updated;
  }),
];

export default eslintConfig;
