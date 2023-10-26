import { BuildOptions, build } from "esbuild";
import { sassPlugin } from "esbuild-sass-plugin";
import * as fs from "node:fs/promises";

const outDir = "../shiny/www/shared/py-shiny";

async function bundle_helper(
  options: BuildOptions
): Promise<ReturnType<typeof build>> {
  try {
    const result = await build({
      format: "esm",
      bundle: true,
      minify: true,
      sourcemap: true,
      metafile: false,
      outdir: outDir,
      ...options,
    });

    Object.entries(options.entryPoints as Record<string, string>).forEach(
      ([output_file_stub, input_path]) => {
        console.log(
          "Building " + output_file_stub + ".js completed successfully!"
        );
      }
    );
    return result;
  } catch (error) {
    console.error("Build failed:", error);
  }
}

const opts: Array<BuildOptions> = [
  {
    entryPoints: { "dataframe/dataframe": "dataframe/index.tsx" },
    plugins: [sassPlugin({ type: "css-text", sourceMap: false })],
    metafile: true,
  },
  {
    entryPoints: {
      "text-area/textarea-autoresize": "text-area/textarea-autoresize.ts",
      "value-box/value-box-icon-gradient":
        "value-box/value-box-icon-gradient.ts",
    },
    minify: false,
    sourcemap: false,
  },
];

// Run function to avoid top level await
async function main(): Promise<void> {
  const results = await Promise.all(opts.map(bundle_helper));

  // Save metafile
  const dataframe_results = results[0];
  await fs.writeFile(
    "esbuild-metadata.json",
    JSON.stringify(dataframe_results.metafile)
  );
}
main();
