import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const header = fs.readFileSync(path.join(root, "header.html"), "utf8").trim();
const footer = fs.readFileSync(path.join(root, "footer.html"), "utf8").trim();

const headerMount = '<div id="site-header-mount"></div>';
const footerMount = '<div id="site-footer-mount"></div>';

const pages = fs
  .readdirSync(root)
  .filter((name) => name.endsWith(".html") && name !== "header.html" && name !== "footer.html");

for (const page of pages) {
  const filePath = path.join(root, page);
  let html = fs.readFileSync(filePath, "utf8");

  if (!html.includes(headerMount) || !html.includes(footerMount)) {
    console.warn(`Skipping ${page}: include mount points not found`);
    continue;
  }

  html = html.replace(headerMount, header).replace(footerMount, footer);
  fs.writeFileSync(filePath, html);
  console.log(`Built ${page}`);
}
