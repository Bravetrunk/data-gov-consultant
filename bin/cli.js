#!/usr/bin/env node

/**
 * data-gov-consultant CLI
 * Node.js executable wrapper for the AI-Native Data & AI Governance Consulting Engine.
 */

const { spawn, execSync } = require("child_process");
const path = require("path");
const fs = require("fs");

const PROJECT_ROOT = path.resolve(__dirname, "..");
const VENV_PYTHON = path.join(PROJECT_ROOT, ".venv", "bin", "python");

function getPythonPath() {
  if (fs.existsSync(VENV_PYTHON)) {
    return VENV_PYTHON;
  }
  try {
    const sysPy = execSync("which python3 || which python").toString().trim();
    if (sysPy) return sysPy;
  } catch (e) {}
  return "python3";
}

function printBanner() {
  console.log(`
================================================================================
🏛️  DATA-GOV-CONSULTANT CLI (Node Package Edition)
    AI-Native Big Data, Data Governance & AI Transformation Practice
================================================================================
  `);
}

function printHelp() {
  printBanner();
  console.log(`Usage:
  data-gov-consultant <command> [options]

Commands:
  run                  Run the 4-Sprint Consulting Pipeline and generate deliverables
  list-industries      Display pre-baked industry knowledge accelerators
  init-client          Scaffold a new client configuration template file
  help                 Display this help information

Options for 'run':
  --name <string>      Client organization name (e.g., "Bangkok Smart Healthcare")
  --industry <type>    Target industry: healthcare, retail, manufacturing, public_sector, bfsi
  --size <string>      Organization size: SME, Medium, Large Enterprise, Ministry
  --budget <number>    Annual revenue or budget in THB (e.g., 500000000)
  --output <dir>       Directory for output deliverables (default: output)

Examples:
  # Run standard pilot engagement:
  npx data-gov-consultant run

  # Run custom enterprise engagement:
  npx data-gov-consultant run --name "Siam Retail Group" --industry retail --budget 2500000000

  # Run for public sector / government agency:
  npx data-gov-consultant run --name "กรมบริการดิจิทัลภาครัฐ" --industry public_sector
`);
}

function listIndustries() {
  printBanner();
  console.log(`Pre-baked Industry Knowledge Accelerators:
  1. [healthcare]     การแพทย์และโรงพยาบาล (PDPA ม.26, HL7 FHIR, ICD-10, Bed Analytics, Claim Optimization)
  2. [retail]         ค้าปลีกและสินค้าอุปโภคบริโภค (FMCG, Customer 360, LTV, Inventory AI, Omnichannel)
  3. [manufacturing]  โรงงานผลิตและห่วงโซ่อุปทาน (Predictive Maintenance, IoT Sensors, OEE, Supply Chain)
  4. [public_sector]  หน่วยงานภาครัฐและรัฐวิสาหกิจ (มาตรฐาน สพร. DGA, GD Catalog, Open Data data.go.th)
  5. [bfsi]           การเงินและการประกันภัย (ธปท./คปภ., Fraud Detection, Credit Scoring, Claims)
  `);
}

function initClient() {
  printBanner();
  const templatePath = path.join(process.cwd(), "client_profile.json");
  const template = {
    name: "ชื่อองค์กรลูกค้าตัวอย่าง",
    industry: "healthcare",
    organization_size: "Large Enterprise",
    annual_revenue_thb: 1000000000.0,
    current_systems: [
      "ระบบสารสนเทศหลัก (Core Transactional System)",
      "ระบบบัญชีและการเงิน (ERP / Accounting)",
      "ไฟล์ Excel รายงานประจำเดือน (Shadow IT)"
    ],
    primary_pain_points: [
      "ข้อมูลแต่ละแผนกไม่เชื่อมโยงกัน รายงานตัวเลขขัดแย้งกัน",
      "ยังไม่มีการจัดทำ Data Catalog และขาด Data Steward ที่ชัดเจน",
      "ความกังวลด้านกฎหมายคุ้มครองข้อมูลส่วนบุคคล (PDPA)"
    ],
    target_objectives: [
      "จัดตั้งสภาธรรมาภิบาลข้อมูล (Data Governance Council)",
      "จัดทำ Data Catalog 14 ฟิลด์ตามมาตรฐาน สพร.",
      "วางสถาปัตยกรรม Modern Data Lakehouse และประยุกต์ใช้ AI"
    ]
  };

  fs.writeFileSync(templatePath, JSON.stringify(template, null, 2), "utf-8");
  console.log(`✅ Created client template at: ${templatePath}`);
  console.log(`You can customize this file and pass it to data-gov-consultant.`);
}

function runPipeline(args) {
  printBanner();
  const pyPath = getPythonPath();
  const mainScript = path.join(PROJECT_ROOT, "main.py");

  const pyArgs = [mainScript, ...args];
  console.log(`[EXEC] Spawning Python Engine: ${pyPath}\n`);

  const child = spawn(pyPath, pyArgs, {
    cwd: PROJECT_ROOT,
    stdio: "inherit",
    env: process.env
  });

  child.on("close", (code) => {
    if (code === 0) {
      console.log("\n✅ Consulting engagement successfully finished.");
      console.log(`📁 View deliverables in: ${path.join(PROJECT_ROOT, "output")}\n`);
    } else {
      console.error(`\n❌ Execution failed with exit code ${code}`);
      process.exit(code);
    }
  });
}

// CLI Router
const args = process.argv.slice(2);
const command = args[0] || "help";
const remainingArgs = args.slice(1);

switch (command) {
  case "run":
    runPipeline(remainingArgs);
    break;
  case "list-industries":
    listIndustries();
    break;
  case "init-client":
    initClient();
    break;
  case "help":
  case "--help":
  case "-h":
    printHelp();
    break;
  default:
    // If user passed options directly like `data-gov-consultant --name ...`
    if (command.startsWith("--")) {
      runPipeline(args);
    } else {
      console.error(`Unknown command: ${command}`);
      printHelp();
      process.exit(1);
    }
}
